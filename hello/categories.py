import re


class Category(object):
    def __init__(self):
        self.raw_str = None
        self.code = None
        self.name = None

    @classmethod
    def from_raw_str(cls, raw_str):
        ret = Category()
        ret.raw_str = raw_str
        m = re.search("(?P<code>.+) - '(?P<name>.+)'.*", ret.raw_str)
        if m:
            ret.code = m.group('code')
            ret.name = m.group('name')
        return ret

    def __repr__(self):
        return 'Category{' \
               + 'raw_str="' + self.raw_str + '"' \
               + ', ' + 'code="' + str(self.code) + '"' \
               + ', ' + 'name="' + str(self.name) + '"' \
               + '}'