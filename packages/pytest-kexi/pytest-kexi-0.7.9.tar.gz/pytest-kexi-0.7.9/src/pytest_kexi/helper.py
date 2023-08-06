from logzero import logger, logfile
logger.error(__name__)


def pytest_assertrepr_compare(op, left, right):
    logger.error('CALLED')
    return [
        'Hoge', 'Fuga'
    ]