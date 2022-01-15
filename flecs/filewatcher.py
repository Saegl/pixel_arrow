import time
import pathlib

from queue import Queue

import threading as th
from typing import Generator


WATCHER_SLEEP_TIME = 1  # seconds


def watcher(directory: pathlib.Path, updates: Queue, stop: th.Event):
    # snapshot mtime
    mtimes: dict[pathlib.Path, float] = {}
    for p in directory.rglob("*.py"):
        mtimes[p] = p.stat().st_mtime

    # Check for new mtime every WATCHER_SLEEP_TIME seconds
    while True:
        if stop.is_set():
            break
        time.sleep(WATCHER_SLEEP_TIME)
        for p, mtime in mtimes.items():
            new_mtime = p.stat().st_mtime
            if new_mtime != mtime:
                updates.put(p.stem)
                mtimes[p] = new_mtime


class FileWatcher:
    def __init__(self, dirname: str):
        self.path = pathlib.Path(dirname)
        self.updates_channel = Queue()
        self.stop_event = th.Event()
        self.watcher_proc = th.Thread(
            target=watcher, args=(self.path, self.updates_channel, self.stop_event)
        )
        self.watcher_proc.start()

    def get_updates(self) -> Generator[str, None, None]:
        qsize = self.updates_channel.qsize()
        for _ in range(qsize):
            yield self.updates_channel.get()

    def kill(self):
        self.stop_event.set()


if __name__ == "__main__":
    watcher = FileWatcher("pixel_arrow/systems")
