from logging import DEBUG, INFO, ERROR, Logger, getLogger, root


class Loggable:

    logger: Logger = None

    @classmethod
    def _init_logger(cls):
        cls.logger = getLogger(f'{cls.__module__}.{cls.__name__}')

    def __init__(self):
        self._init_logger()

    @classmethod
    def debug(cls, *args, **kwargs):
        if root.level <= DEBUG:
            if not cls.logger:
                cls._init_logger()
            cls.logger.debug(*args, **kwargs)

    @classmethod
    def info(cls, *args, **kwargs):
        if root.level <= INFO:
            if not cls.logger:
                cls._init_logger()
            cls.logger.info(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        if root.level <= ERROR:
            if not cls.logger:
                cls._init_logger()
            cls.logger.exception(*args, **kwargs)
            # cls.logger.error(*args, **kwargs)
