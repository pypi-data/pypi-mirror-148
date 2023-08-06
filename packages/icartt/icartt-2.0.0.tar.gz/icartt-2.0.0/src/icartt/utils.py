# -*- coding: utf-8 -*-


class FilehandleWithLinecounter:
    """a file handle that counts the number of files that were read"""

    def __init__(self, f, delimiter):
        self.f = f
        self.line = 0
        self.delimiter = delimiter

    def readline(self, doSplit=True):
        self.line += 1
        dmp = self.f.readline().replace("\n", "").replace("\r", "")
        if doSplit:
            dmp = [word.strip(" ") for word in dmp.split(self.delimiter)]
        return dmp


def extractVardesc(line_parts: list) -> str:
    """extract variable description from ict header line parts (splitted line)"""
    shortname, units, standardname, longname, *_ = line_parts + [None] * 3
    return shortname, units, standardname, longname
