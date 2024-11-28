from collections import defaultdict


class Log:
    def __init__(self, detailed=False):
        self.record_ = defaultdict(int)
        self.detailed = detailed

    def record(self, type: str, val: int):
        self.record_[type] += val

    def printReport(self):
        keys = sorted(self.record_.keys())
        for key in keys:
            print(f"{key} - {self.record_[key]}")

    def output(self, message):
        if self.detailed:
            print(message())


log = Log(detailed=False)
