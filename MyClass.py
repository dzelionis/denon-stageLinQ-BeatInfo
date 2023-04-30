from dataclasses import dataclass, field, asdict,astuple
import json

@dataclass
class MyDataClass():
    def to_dict(self):
        return asdict(self)

    def to_tuple(self):
        return astuple(self)

    def to_json(self):
        return json.dumps(asdict(self))
