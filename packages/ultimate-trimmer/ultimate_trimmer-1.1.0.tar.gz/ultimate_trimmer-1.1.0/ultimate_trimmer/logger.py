class Logger:
    log = " ---- log ---- \n"

    @classmethod
    def write(cls, *args, end="\n"):
        cls.log += " ".join(map(str, args)) + end

    @classmethod
    def getLog(cls):
        return cls.log
