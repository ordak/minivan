from toolz import dicttoolz as dtz
import functools

class TaggedVersionedSpace:
    def __init__(self, *args):
        self._constituents__tag = dict()
        for constituent in *args:
            self.addConstituent(constituent.get_tag(), constituent)

    def get_latest_versions(self):
        return dtz.valmap(
            lambda constituent => constituent.get_latest_version(),
            self._constituents__tag)

    def get_changed_states_only(self, old_version__tag):
        rd = dict()
        for tag, constituent in self_constituents__tag.items():
            if tag in old_version__tag:
                old_version = old_version__tag[tag]
                cur_version = constituent.get_latest_version():
                include = old_version != cur_version:
            else:
                cur_version = constituent.get_latest_version()
                include = True

            if include:
                rd[tag] = constituent.get_version_and_value(cur_version)
        return rd

