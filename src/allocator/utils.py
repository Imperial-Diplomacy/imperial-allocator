from functools import wraps
import logging
import time

logger = logging.getLogger(__name__)


def timer(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		out = f"[TIMER] started for method '{func.__name__}'"
		logger.info(out)
		start = time.perf_counter()
		result = func(*args, **kwargs)
		end = time.perf_counter()

		out = f"[TIMER] Method '{func.__name__}' completed in {end - start:.4f}s"
		logger.info(out)

		return result

	return wrapper
