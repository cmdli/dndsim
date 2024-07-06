from collections import defaultdict


class Log:
    def __init__(self):
        self.record_ = defaultdict(int)

    def record(self, type, val):
        self.record_[type] += val

    def printReport(self):
        for key in self.record_:
            print(f"Type: {key} Value: {self.record_[key]}")


log = Log()
