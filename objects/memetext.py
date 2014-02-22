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

    def __str__(self):
    	if self.top is not None and self.bottom is not None:
    		return "%s / %s" % (self.top, self.bottom)
    	if self.top is not None:
    		return self.top
    	if self.bottom is not None:
    		return self.bottom
    	return "nothing"

    def __repr__(self):
    	if _type is not None:
    		return "MemeText(%s, %s, %s)" % (self.top, self.bottom, self._type)
    	else:
	    	return "MemeText(%s, %s)" % (self.top, self.bottom)
