class Response(object):

    """Docstring for Response. """

    def __init__(self, data, status="success"):
        """TODO: to be defined1. """
        self.data = data
        self.payload = {
            "data":  None,
            "status": status,
        }

    def serialize(self, data=None):
        if data is None:
            data = self.data
        return self._serialize(data)

    def _serialize(self, data):
        if isinstance(data, list):
            items = []
            for item in data:
                items.append(item.__json__())
            self.payload["data"] = items
        elif hasattr(data, "__json__"):
            self.payload["data"] = data.__json__()
        else:
            self.payload["data"] = None
        return self.payload
