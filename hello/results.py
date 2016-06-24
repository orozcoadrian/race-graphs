import re


class Run(object):
    def __init__(self):
        self.raw_str = None
        self.id = None
        self.dnf = None
        self.time = None
        self.penalty_seconds = 0

    @classmethod
    def from_raw_str(cls, id, raw_str):
        ret = Run()
        ret.id = id
        ret.raw_str = raw_str
        ret.dnf = '+dnf' in ret.raw_str
        if not ret.dnf and '999.999' not in ret.raw_str and 'off' not in ret.raw_str:
            # ret.time = ret.raw_str.replace('+dnf', '')
            m = re.search("(?P<time>\d+\.\d+)(\+(?P<penalty>\d+))?", ret.raw_str)
            if m:
                ret.time = float(m.group('time'))
                if m.group('penalty'):
                    ret.penalty_seconds = int(m.group('penalty'))
        return ret

    def __repr__(self):
        return 'Run{' \
               + 'raw_str="' + self.raw_str + '"' \
               + ', ' + 'id="' + str(self.id) + '"' \
               + ', ' + 'dnf=' + str(self.dnf) \
               + ', ' + 'time="' + str(self.time) + '"' \
               + '}'

    def is_valid_for_chart(self):
        return self.time


class ResultsModel(object):
    def __init__(self, records, results_title, url):
        self.records = records
        self.results_title = results_title
        self.url = url