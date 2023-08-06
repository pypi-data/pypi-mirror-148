import json


class PrettyDict(dict):
    def __init__(self, data: dict = None):
        if data:
            for i in data:
                if isinstance(data[i], dict):
                    data[i] = PrettyDict(data[i])
                self[i] = data[i]
        super().__init__()

    def __str__(self):
        return json.dumps(self, indent=4, default=str)

    @property
    def self(self):
        return self
