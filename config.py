class Config:
    INITIAL_RANGE = 2000
    MAX_RANGE = 2000
    DROP_PROB_SENDER = 0
    DROP_PROB_RECEIVER = 0
    DEAD_RECKONING_ANGLE = 0
    FAILURE_TIMEOUT = 60 * 0.5
    FAILURE_MODEL = 0  # 0 for random, 1 for exponential
    FAILURE_PROB = 0
    ACCELERATION = 1
    DECELERATION = 1
    MAX_SPEED = 3
    DISPLAY_CELL_SIZE = 0.05
    BUSY_WAITING = False
    DURATION = 60
    K = 3 # if k = 0 no standbys are deployed
    SHAPE = 'chess'
    RESULTS_PATH = 'results'
    DEBUG = True
    FILE_NAME_KEYS = [('DISPATCHERS', 'D'), ('DISPATCH_RATE', 'R'), ('FAILURE_TIMEOUT', 'T'), ('MAX_SPEED', 'S'),
                      ('SANITY_TEST', 'test')]
    DIR_KEYS = ['K']
    SERVER_TIMEOUT = 120
    PROCESS_JOIN_TIMEOUT = 120
    DISPATCHERS = 1  # valid values 1 3 5
    DISPATCH_RATE = "100"  # valid values 'inf' or a non-zero number
    MULTICAST = False  # should be False for cloudlab and True for AWS
    INPUT = 'chess_K3'  # place the file int the results directory
    RESET_AFTER_INITIAL_DEPLOY = True  # flag that if reset all metrics after intial FLSs are all deployed
    SANITY_TEST = 0  # 0 for not test, 1 for normal test with hub and no standby, 2 for standby test with no hub
    SANITY_TEST_CONFIG = [('NUMBER_OF_FLS', 10), ('DIST_TO_POINT', 10), ('CHECK_TIME_RANGE', 60 * 0.5, 60 * 1)]
    STANDBY_TEST_CONFIG = [('RADIUS', 5), ('DEPLOY_DIST', 20), ('FAILURE_TIMEOUT_GAP', 2), ('CHECK_TIME_RANGE', 0, 60 * 1)]
    DISPATCHER_ASSIGN_POLICY = "Random"
    PRIORITIZE_ILLUMINATING_FLS = True
    CEDED_POLICY = 0  # 0 for put into a group, 1 for each into a group with standby, 2 for no shandby, 3 for merge to closest group
