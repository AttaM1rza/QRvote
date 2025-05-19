import threading


class ThreadSafeList:
    def __init__(self):
        self._list = []
        self._lock = threading.Lock()

    def get_all(self):
        """Returns a shallow copy of the list (thread-safe)."""
        with self._lock:
            return list(self._list)

    def set_all(self, new_list):
        """Replaces the entire list (thread-safe)."""
        with self._lock:
            self._list = list(new_list)

    def __len__(self):
        with self._lock:
            return len(self._list)

    def clear(self):
        with self._lock:
            self._list.clear()
