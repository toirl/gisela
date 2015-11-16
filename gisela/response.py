import json

class Response(object):

    """Docstring for Response. """

    def __init__(self):
        """TODO: to be defined1. """
        self.data = {
            "status": None,
            "data": None
        }

    def serialize(self, data):
        if isinstance(data, list):
            items = []
            for item in data:
                items.append(item.__json__())
            self.data["data"] = items
        elif hasattr(data, "__json__"):
            self.data["data"] = data.__json__()
        else:
            self.data["data"] = None
        return json.dumps(self.data)

class Success(Response):

    def __init__(self):
        super(Success, self).__init__()
        self.data["status"] = "success"

class Fail(Response):

    def __init__(self):
        super(Fail, self).__init__()
        self.data["status"] = "fail"

class Error(Response):

    def __init__(self):
        super(Error, self).__init__()
        self.data["status"] = "error"
        self.data["message"] = None
        self.data["code"] = None
