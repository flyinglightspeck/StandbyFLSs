import multiprocessing
import queue
import time

import state
from .network import NetworkThread
from .handler import HandlerThread
from .worker_socket import WorkerSocket
from .context import WorkerContext
from .history import History
from .metrics import Metrics
from utils import logger

import resource

class WorkerProcess(multiprocessing.Process):
    def __init__(self, fid, gtl, el, dir_meta,
                 start_time, is_standby=False, standby_id=None, group_id=None, radio_range=2000, fail_timeout=None):
        super(WorkerProcess, self).__init__()
        self.history = History(4)
        self.metrics = Metrics(self.history, dir_meta, start_time)
        self.context = WorkerContext(fid=fid, gtl=gtl, el=el, metrics=self.metrics,
                                     is_standby=is_standby, standby_id=standby_id, group_id=group_id,
                                     radio_range=radio_range)

        logger.info("Socket Created")
        self.sock = WorkerSocket()
        self.default_failure_timeout = fail_timeout if fail_timeout is not None else None

    def run(self):

        # Set the soft and hard limits
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (4096, hard))

        logger.debug(f"STARTING_PROCESS fid={self.context.fid} time={time.time()}")
        event_queue = queue.Queue()
        state_machine = state.StateMachine(self.context, self.sock, self.metrics, event_queue, self.default_failure_timeout)

        network_thread = NetworkThread(event_queue, self.context, self.sock, state_machine)
        handler_thread = HandlerThread(event_queue, state_machine, self.context)
        network_thread.start()
        handler_thread.start()

        handler_thread.join()

        logger.debug(f"STOP MESSAGE RECEIVE: {self.context.fid}, {self.sock}")
        network_thread.stop()
        network_thread.join()
        logger.info(f"Socket Closed: {network_thread.sock}")

        logger.debug(f"SOCKET CLOSE: {self.context.fid}, {self.sock}")
        self.sock.close()
        while not event_queue.empty():
            try:
                event_queue.get(False)
            except queue.Empty:
                continue
            event_queue.task_done()
