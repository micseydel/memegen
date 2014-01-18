from pymongo.son_manipulator import SONManipulator

"""
Potential attributes:
  position
  font
  color

Use JSON docs to specify custom types?
"""


class MemeText(object):
    def __init__(self, top, bottom, _type=None):
        self.top = top
        self.bottom = bottom
        self._type = _type

    def json(self):
        return {"_type": "MemeText", "top": self.top, "bottom": self.bottom}


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
