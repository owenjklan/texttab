"""
Formatter classes that can be applied to columns
"""


class ColumnFormatter(object):
    def __init__(self):
        return

    def format(self, value):
        raise NotImplemented


class ReadableBytesFormatter(object):
    @classmethod
    def format(cls, value, column):
        format_value = cls.human_readable_bytes(value)
        return "", format_value, False

    def human_readable_bytes(byteval):
        if byteval / 2**40 >= 1:
            return "{:>2.1f} TB ".format(byteval / 2**40)
        elif byteval / 2**30 >= 1:
            return "{:>2.1f} GB ".format(byteval / 2**30)
        elif byteval / 2**20 >= 1:
            return "{:>2.1f} MB ".format(byteval / 2**20)
        elif byteval / 2**10 >= 1:
            return "{:>2.1f} KB ".format(byteval / 2**10)
        else:
            return "{:>3.0f} Bytes".format(byteval)


class UnixPermissionsFormatter(ColumnFormatter):
    @classmethod
    def format(cls, value, column):
        d = {
            0: '---',
            1: '--x',
            2: '-w-',
            3: '-wx',
            4: 'r--',
            5: 'r-x',
            6: 'rw-',
            7: 'rwx',
        }
        mode_char = "-"
        ret_str = "{}{}{}{}".format(
            mode_char,
            d[(value & 0o0700) >> 6],
            d[(value & 0o0070) >> 3],
            d[value & 0o0007]
        )
        return "", ret_str, False
