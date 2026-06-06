import time
from kata_03_ctxmgr import timed, Timed


def test_timed_decorator():
    with timed():
        time.sleep(0.01)
    # just confirms no crash + prints elapsed


def test_timed_class_stores_elapsed():
    with Timed() as t:
        time.sleep(0.01)
    assert t.elapsed >= 0.01
    assert t.elapsed < 1.0
