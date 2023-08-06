import pytest
from logzero import logger

__version__ = "0.8.2"
logger.error(__name__)

pytest.register_assert_rewrite("pytest_kexi.helper")
