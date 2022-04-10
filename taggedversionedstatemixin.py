from typing import List, Dict, Any

class TaggedVersionedStateMixin:
    def __init__(self, tag: str, initial_state=None):
        # class could operate fine without knowing its tag
        # this is for convenient reference by upper layer (TaggedVersionedSpace)
        self._tag: str = tag
        self._state = initial_state
        self._version: int = 0

    def get_tag(self) -> str:
        return self._tag

    def get_latest_version(self) -> int:
        return self._version

    def get_version_and_value(self, version: int) -> Dict[str, Any]:
        return {'version': self._version, 'value': self._state}

    def updated_versioned_state(self, new_state):
        self._state = new_state
        self._version += 1  # wraparound or cycling would be OK if Python did it

