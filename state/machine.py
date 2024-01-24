import random
import time

import threading

import numpy as np

from message import Message, MessageTypes
from config import Config
from utils.distribution import left_half_exponential
from worker.metrics import TimelineEvents
from .types import StateTypes
from worker.network import PrioritizedItem
from utils import write_json, logger


class StateMachine:

    def __init__(self, context, sock, metrics, event_queue, default_failure_timeout):
        self.state = None
        self.context = context
        self.metrics = metrics
        self.sock = sock
        self.timer_failure = None
        self.event_queue = event_queue
        self.is_neighbors_processed = False
        self.handled_failure = dict()
        self.move_thread = None
        self.is_mid_flight = False
        self.is_terminating = False
        self.is_arrived = False
        self.unhandled_move = None
        self.move_time = 0
        self.default_failure_timeout = default_failure_timeout

    def start(self):
        logger.debug(f"STARTED {self.context} {time.time()}")
        self.enter(StateTypes.SINGLE)
        dur, dest, dist = self.context.deploy()

        # print(f"MOVE READY {time.time() - self.metrics.start_time} fid={self.context.fid}")
        self.move(dur, dest, TimelineEvents.STANDBY if self.context.is_standby else TimelineEvents.ILLUMINATE, dist)
        self.move_time = time.time()

        if self.context.is_standby:
            # send the id of the new standby to group members
            self.broadcast(Message(MessageTypes.ASSIGN_STANDBY).to_swarm(self.context))

    def move(self, dur, dest, arrival_event, dist):
        # print(f"MOVE dist={dist} fid={self.context.fid}")
        self.move_thread = threading.Timer(dur, self.change_move_state,
                                           (MessageTypes.MOVE, (dest, arrival_event, dist)))
        self.is_arrived = False
        logger.debug(f"START MOVING fid={self.context.fid}")
        self.is_mid_flight = True
        self.move_thread.start()

    def handle_stop(self, msg):
        if msg is not None and (msg.args is None or len(msg.args) == 0):
            stop_msg = Message(MessageTypes.STOP).to_all()
            self.broadcast(stop_msg)
            self.context.handler_stop_time = time.time()

        if self.move_thread is not None:
            self.move_thread.cancel()
            self.update_movement()
            self.move_thread = None

        self.cancel_timers()

        stop_time = self.context.handler_stop_time - self.context.network_stop_time

        try:
            write_json(self.context.fid, self.context.metrics.get_final_report_(stop_time, self.context.dist_traveled),
                       self.metrics.results_directory,
                       False)
        except Exception as e:
            logger.error(f"FLS Log Failed: fid={self.context.fid} INFO:{e}")
            self.send_to_server(Message(MessageTypes.ERROR))

    def fail(self, msg):
        if self.is_terminating:
            return

        self.context.metrics.log_failure_time(time.time(), self.context.is_standby, self.is_mid_flight)
        # self.put_state_in_q(MessageTypes.STOP, args=(False,))  # False for not broadcasting stop msg
        if self.context.is_standby:
            # notify group
            self.broadcast(Message(MessageTypes.STANDBY_FAILED).to_swarm(self.context))
            self.send_to_server(Message(MessageTypes.REPLICA_REQUEST_HUB, args=(False,)))
            logger.debug(f"REQUEST NEW STANDBY {self.context}")
        elif self.context.standby_id is None:
            # request an illuminating FLS from the hub, arg True is for illuminating FLS
            self.send_to_server(Message(MessageTypes.REPLICA_REQUEST_HUB, args=(True,)))
            logger.debug(f"RECOVER BY HUB {self.context} time={time.time()}")
        else:
            # notify group
            self.broadcast(Message(MessageTypes.REPLICA_REQUEST).to_swarm(self.context))
            # request standby from server
            self.send_to_server(Message(MessageTypes.REPLICA_REQUEST_HUB, args=(False,)))
            logger.debug(f"RECOVER BY STANDBY {self.context} standby fid={self.context.standby_id}")

        self.handle_stop(None)
        logger.debug(f"FAILED {self.context}")

    def assign_new_standby(self, msg):
        if not self.context.is_standby:
            self.context.standby_id = msg.fid
            self.context.metrics.log_standby_id(time.time(), self.context.standby_id)

            logger.debug(f"STANDBY ASSIGNED {self.context} standby={self.context.standby_id}")

    def replace_failed_fls(self, msg):

        if self.move_thread is not None:
            self.move_thread.cancel()
            self.move_thread = None
            self.is_mid_flight = True
            self.update_movement()
            logger.debug(f"PREEMPT MOVEMENT fid={self.context.fid}, mid_flight={self.is_mid_flight}")

        self.context.is_standby = False
        v = msg.gtl - self.context.el
        self.context.gtl = msg.gtl

        dist = np.linalg.norm(v)
        timestamp, dur, dest = self.context.move(v)

        if self.unhandled_move is not None:
            self.unhandled_move.stale = True
            mid_flight_state = True
            logger.debug(f"UNHANDLED MOVE CANCEL fid={self.context.fid}")
            self.unhandled_move = None
        else:
            mid_flight_state = self.is_mid_flight
            logger.debug(f"STANDBY MID_FLIGHT STATE {mid_flight_state} fid={self.context.fid}")

        self.move(dur, dest, TimelineEvents.ILLUMINATE_STANDBY, dist)

        self.context.log_replacement(timestamp, dur, msg.fid, msg.gtl, mid_flight_state)

        logger.debug(f"REPLACED {self.context} failed_fid={msg.fid} failed_el={msg.el} mid flight={mid_flight_state}")

    def handle_replica_request(self, msg):
        if self.context.is_standby:
            self.replace_failed_fls(msg)
        else:
            self.context.standby_id = None
            self.context.metrics.log_standby_id(time.time(), self.context.standby_id)

            logger.debug(f"STANDBY CHANGED {self.context} standby={self.context.standby_id}")

    def handle_standby_failure(self, msg):
        if self.context.standby_id == msg.fid:
            self.context.standby_id = None
            self.context.metrics.log_standby_id(time.time(), self.context.standby_id)

            logger.debug(f"STANDBY FAILED {self.context} standby={self.context.standby_id}")

    def set_timer_to_fail(self, failure_timeout=None):
        if failure_timeout is None:

            if Config.FAILURE_MODEL == 0:
                failure_timeout = random.random() * Config.FAILURE_TIMEOUT
            elif Config.FAILURE_MODEL == 1:
                failure_timeout = left_half_exponential(Config.FAILURE_TIMEOUT)
        self.timer_failure = threading.Timer(failure_timeout, self.put_state_in_q, (MessageTypes.FAILURE_DETECTED,))
        self.timer_failure.start()

    def handle_move(self, msg):
        # el, destination, dist
        prev_pos = self.context.el
        self.context.el = msg.args[0]
        self.context.dist_traveled += msg.args[2]
        logger.debug(f"DISTANCE TRAVELED {msg.args[2]} fid={self.context.fid} prev_pos={prev_pos} cur_pos={msg.args[0]}")
        self.context.metrics.log_arrival(time.time(), msg.args[1], self.context.gtl, msg.args[2])
        self.move_thread = None
        self.is_arrived = True
        self.unhandled_move = None

        logger.debug(f"MOVE HANDLED fid={self.context.fid}, delay_time={time.time() - self.metrics.start_time}")

    def enter(self, state):
        self.leave(self.state)
        self.state = state

        if self.state == StateTypes.SINGLE:
            self.set_timer_to_fail(self.default_failure_timeout)

    def change_move_state(self, event, args=()):
        self.is_mid_flight = False
        logger.debug(f"MOVE ENQUEUE fid={self.context.fid} time={time.time() - self.metrics.start_time}")
        self.unhandled_move = self.put_state_in_q(event, args=args)

    def put_state_in_q(self, event, args=()):
        msg = Message(event, args=args).to_fls(self.context)
        item = PrioritizedItem(1, msg, False)
        self.event_queue.put(item)
        return item

    def leave(self, state):
        pass

    def drive_failure_handling(self, msg):
        event = msg.type

        if event == MessageTypes.STOP:
            self.handle_stop(msg)
        elif event == MessageTypes.FAILURE_DETECTED:
            self.fail(msg)
        elif event == MessageTypes.REPLICA_REQUEST:
            self.handle_replica_request(msg)
        elif event == MessageTypes.ASSIGN_STANDBY:
            self.assign_new_standby(msg)
        elif event == MessageTypes.STANDBY_FAILED:
            self.handle_standby_failure(msg)
        elif event == MessageTypes.MOVE:
            self.handle_move(msg)

    def drive(self, msg):
        self.drive_failure_handling(msg)

    def broadcast(self, msg):
        msg.from_fls(self.context)
        length = self.sock.broadcast(msg)
        self.context.log_sent_message(msg, length)

    def send_to_server(self, msg):
        msg.from_fls(self.context).to_server(self.context.sid)
        length = self.sock.broadcast(msg)
        self.context.log_sent_message(msg, length)

    def cancel_timers(self):
        if self.timer_failure is not None:
            self.timer_failure.cancel()
            self.timer_failure = None

    def check_arrived(self):
        return self.is_arrived

    def cancel_fail(self):
        self.is_terminating = True

    def update_movement(self):
        prev_pos = self.context.el
        self.context.el = self.context.vm.get_location(time.time())
        # print(f"fid={self.context.fid} {np.linalg.norm(prev_pos - self.context.el)}")
        self.context.dist_traveled += np.linalg.norm(self.context.vm.x0 - self.context.el)
        logger.debug(f"MOVE CHANGE Dist: {np.linalg.norm(self.context.vm.x0 - self.context.el)} fid={self.context.fid} NewPos: {self.context.el}")
