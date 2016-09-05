class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def log_normal(info):
        print ('[INFO]  ' + info )

    @staticmethod
    def log_high(info):
        print (Logger.OKGREEN + '  ~ [OK]  ' + info + Logger.ENDC)

    @staticmethod
    def log_fail(info):
        print (Logger.FAIL + '  ~ [FAIL]  '  + info + Logger.ENDC)
