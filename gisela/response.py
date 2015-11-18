class Response(dict):

    """Docstring for Response. """

    def __init__(self, data, status="success"):
        """TODO: to be defined1. """
        self["status"] = status
        self["data"] = self._serialize(data)

    def _serialize(self, data):
        if isinstance(data, list):
            items = []
            for item in data:
                items.append(item.__json__())
            return items
        elif hasattr(data, "__json__"):
            return data.__json__()
        return None
