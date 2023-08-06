import logging

from pl_extension.loggers import logging_logger


def test_logginglogger(tmpdir):
    logger = logging_logger.LoggingLogger(
        tmpdir, prefix="ple", level=logging.INFO
    )
    logger.info("hello, pl-extension!")
