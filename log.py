from collections import defaultdict


class Log:
    def __init__(self, detailed = False):
        self.record_ = defaultdict(int)
        self.detailed = detailed

    def record(self, type, val):
        self.record_[type] += val

    def printReport(self):
        for key in self.record_:
            print(f"Type: {key} Value: {self.record_[key]}")

    def output(self, message):
        if (self.detailed):
            print(message)

log = Log(detailed=False)
