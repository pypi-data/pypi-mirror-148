from time import perf_counter
from contextlib import contextmanager
import logging.config


logger = logging.getLogger("entityscan")
logger.setLevel("INFO")


@contextmanager
def timelog(
    msg: str,
    on_start=logging.DEBUG,
    on_done=logging.DEBUG,
    warn_threshold=1.0,
):
    pc = perf_counter()
    logger.log(msg=f"Start: {msg}", level=on_start)

    yield

    time = perf_counter() - pc
    on_done = on_done if time < warn_threshold else logging.WARN
    logger.log(msg=f"Done : {msg} [{time:.3f}s]", level=on_done)
