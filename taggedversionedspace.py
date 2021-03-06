from typing import List, Dict, Any
import functools

from toolz import dicttoolz as dtz

from taggedversionedstatemixin import TaggedVersionedStateMixin

class TaggedVersionedSpace:
    def __init__(self, *args):
        self._constituents__tag: Dict[str, TaggedVerionedStateMixin] = dict()
        for constituent in args:
            self.add(constituent.get_tag(), constituent)

    def add(self, tag: str, constituent: TaggedVersionedStateMixin):
        self._constituents__tag[tag] = constituent

    def get_latest_versions(self):
        return dtz.valmap(
                lambda constituent: constituent.get_latest_version(),
            self._constituents__tag)

    def get_changed_states_only(self, old_version__tag: Dict[str, int]):
        rd = dict()
        for tag, constituent in self_constituents__tag.items():
            if tag in old_version__tag:
                old_version = old_version__tag[tag]
                cur_version = constituent.get_latest_version()
                include = old_version != cur_version
            else:
                cur_version = constituent.get_latest_version()
                include = True

            if include:
                rd[tag] = constituent.get_version_and_value(cur_version)
        return rd

