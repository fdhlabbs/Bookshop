# model/state.py

class State:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new State instance")
            cls._instance = super().__new__(cls)
            cls._instance._data = {}   # internal storage dict
        return cls._instance

    # Optional: allow dot-notation storage
    def __getattr__(self, key):
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"State has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key == "_data" or key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __delattr__(self, key):
        if key in self._data:
            del self._data[key]
        else:
            raise AttributeError(f"State has no attribute '{key}'")

    # Optional helpers
    def reset(self):
        self._data.clear()

    def dump(self):
        return dict(self._data)


#usage

#from model.state import State

#State().anything = 999

#anything = State().anything