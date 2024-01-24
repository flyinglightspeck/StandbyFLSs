import threading
from message import MessageTypes
from state import StateTypes
from utils import logger


class HandlerThread(threading.Thread):
    def __init__(self, event_queue, state_machine, context):
        super(HandlerThread, self).__init__()
        self.event_queue = event_queue
        self.state_machine = state_machine
        self.context = context

    def run(self):
        self.state_machine.start()
        stop_flag = False
        while True:
            item = self.event_queue.get()
            if item.stale:
                continue

            event = item.event
            self.context.log_received_message(event, 0)
            self.state_machine.drive(event)
            if event.type == MessageTypes.STOP or event.type == MessageTypes.FAILURE_DETECTED:
                logger.debug(f"HANDLER STOP fid={self.context.fid}")
                break

            # if event.type == MessageTypes.FAILURE_DETECTED:
            #     if not stop_flag:
            #         self.state_machine.drive(event)
            #         logger.debug(f"END HANDLER {self.context} by failure")
            #         break
            #     else:
            #         logger.debug(f"CANCEL FAILURE {self.context}")
            #
            # elif event.type == MessageTypes.STOP or stop_flag:
            #     if not stop_flag:
            #         logger.debug(f"STOP TRIGGERED {self.context}")
            #
            #     stop_flag = True
            #
            #     if event.type is MessageTypes.MOVE or (self.state_machine.check_arrived() and event.type is MessageTypes.STOP):
            #         self.state_machine.drive(event)
            #         logger.debug(f"END HANDLER {self.context} by stop message")
            #
            #         if event.type is not MessageTypes.STOP:
            #             self.state_machine.handle_stop(event, True)
            #         break
            #
            #     self.state_machine.cancel_fail()
            #     self.state_machine.drive(event)
            #
            # else:
            #     self.state_machine.drive(event)

    def flush_all(self):
        with self.event_queue.mutex:
            for item in self.event_queue.queue:
                item.stale = True
