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
