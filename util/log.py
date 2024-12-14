from collections import defaultdict


class Log:
    def __init__(self, detailed=False):
        self.record_ = defaultdict(int)
        self.detailed = detailed
        self.enabled = False

    def record(self, type: str, val: int):
        if self.enabled:
            self.record_[type] += val

    def printReport(self):
        keys = sorted(self.record_.keys())
        for key in keys:
            print(f"{key} - {self.record_[key]}")

    def output(self, message):
        if self.enabled and self.detailed:
            print(message())

    def enable(self):
        self.enabled = True


log = Log(detailed=False)
