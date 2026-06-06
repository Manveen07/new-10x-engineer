from contextlib import contextmanager
import time


@contextmanager
def timed():
    try:
        start = time.perf_counter()
        yield
    finally:
        print(f"elapsed: {time.perf_counter()-start:.4f}s")


class Timed:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, tb):
        self.elapsed = time.perf_counter() - self.start
