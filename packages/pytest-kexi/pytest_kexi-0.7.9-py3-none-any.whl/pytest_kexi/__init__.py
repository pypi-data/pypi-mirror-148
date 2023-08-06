import pytest
from logzero import logger
logger.error(__name__)

pytest.register_assert_rewrite("pytest_kexi.helper")