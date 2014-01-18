from pymongo.son_manipulator import SONManipulator

from memetext import MemeText


class Transform(SONManipulator):
    def transform_incoming(self, son, collection):
        for key, value in son.items():
            if isinstance(value, MemeText):
                son[key] = value.json()
            elif isinstance(value, dict):  # Make sure we recurse into sub-docs
                son[key] = self.transform_incoming(value, collection)

        return son

    def transform_outgoing(self, son, collection):
        for key, value in son.items():
            if isinstance(value, dict):
                _type = value.get("_type", "")
                if "MemeText" in _type:
                    son[key] = MemeText(**value)
                else:
                    son[key] = self.transform_outgoing(value, collection)

        return son
