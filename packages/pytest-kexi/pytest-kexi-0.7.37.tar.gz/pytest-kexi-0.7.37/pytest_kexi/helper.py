from logzero import logger

logger.error(__name__)


def pytest_assertrepr_compare(op, left, right):
    logger.info('CALLED')
    return [
        'Hoge', 'Fuga'
    ]
