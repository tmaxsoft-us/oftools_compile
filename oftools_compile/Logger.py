import logging


def singleton(myClass):
    instances = {}

    def getInstance(*args, **kwargs):
        if myClass not in instances:
            instances[myClass] = myClass(*args, **kwargs)
        return instances[myClass]

    return getInstance


@singleton
class Logger(object):
    # TODO Create Logger
    logger = logging.getLogger('oftools_compile')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('oftools_compile.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%asctime)s - %(name)s - %(levelname)s - %(messages)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
