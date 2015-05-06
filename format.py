#!/usr/bin/env python

##
# Python script to tidy mediasession.bs
#
# adapted from: https://github.com/w3c/webvtt/blob/41cac9c211f9c581de466bb9b8b5dd11a160ffad/format.py
##

import re
import sys

# http://stackoverflow.com/q/1732348
pattern = re.compile(r'<(\w+).*?>|</(\w+)>|<!--(.*?)-->', re.DOTALL)

INDENT = '  '
COLUMNS = 80

def hasendtag(name):
    return name not in ['br', 'img', 'meta']

def tokenize(source):
    offset = 0

    for match in pattern.finditer(source):
        if match.start() > offset:
            yield ('text', offset, match.start(), None)
        index = match.lastindex
        token = ('open', 'close', 'comment')[index - 1]
        name = index < 3 and match.group(index) or None
        yield (token, match.start(), match.end(), name)
        offset = match.end()

    if offset < len(source):
        yield('text', offset, len(source), None)

def validate(path, source, tokens):
    stack = []

    def fail(reason, offset):
        lineno = source.count('\n', 0, offset) + 1
        print '%s:%s: error: %s' % (path, lineno, reason)
        print source.splitlines()[lineno - 1]
        sys.exit(1)

    for token, start, end, name in tokens:
        if token == 'open':
            if hasendtag(name):
                stack.append(name)
        elif token == 'close':
            if len(stack) == 0 or stack[-1] != name:
                fail("close tag '%s' with open tags '%s'" %
                     (name, ' > '.join(stack)), start)
            stack.pop()

    if len(stack) > 0:
        fail("end of file with open tags '%s'" %
             (' > '.join(stack)), len(source) - 1)

class LineWriter:
    def __init__(self, path):
        self._file = open(path, 'w')
        self._data = ''
        self._startdepth = 0

    def _writelines(self, depth):
        lines = [depth * INDENT]
        for word in self._data.strip().split():
            if lines[-1].isspace() or len(lines[-1]) + len(word) <= COLUMNS:
                lines[-1] += word + ' '
            else:
                lines.append(depth * INDENT + word + ' ')
        self._file.write('\n'.join((l.rstrip() for l in lines)))
        self._data = ''

    def append(self, data):
        self._data += data

    def verbatim(self, data, depth):
        if len(self._data) > 0:
            mindepth = min(self._startdepth, depth)
            self._writelines(mindepth)
            self._file.write(mindepth * INDENT)
        self._file.write(data)

    def newline(self, depth):
        self._writelines(min(self._startdepth, depth))
        self._file.write('\n')
        self._startdepth = depth

def normalize(path, source, tokens):
    lw = LineWriter(path)

    stack = []

    def depth():
        d = 0
        for name, merge in stack:
            if merge:
                break
            d += 1
        return d

    def merging():
        for name, merge in stack:
            if merge:
                return True
        return False

    def preservespace():
        for name, merge in stack:
            if name in ('script', 'style', 'pre'):
                return True
        return False

    for token, start, end, name in tokens:
        didpreservespace = preservespace()

        if token == 'open' and hasendtag(name):
            # treat children as single line if followed by non-whitespace
            merge = not source[end].isspace()
            stack.append((name, merge))
        elif token == 'close':
            stack.pop()

        data = source[start:end]

        if preservespace() or didpreservespace:
            lw.verbatim(data, depth())
        elif token == 'text' and not merging():
            # when merging() everything is mangled, but even when not merging(),
            # consecutive non-empty lines of text are merged together into as
            # few lines as possible.
            mergelines = False
            while len(data) > 0:
                line, ending, data = data.partition('\n')
                emptyline = len(line) == 0 or line.isspace()
                lastline = len(data) == 0
                if mergelines:
                    if emptyline:
                        lw.newline(depth())
                    else:
                        lw.append(' ')
                    mergelines = False
                if line:
                    lw.append(line)
                if ending:
                    if emptyline or lastline:
                        lw.newline(depth())
                    else:
                        mergelines = True
        else:
            lw.append(data)

    assert len(stack) == 0

def format(path):
    with open(path, 'r') as f:
        source = f.read().rstrip() + '\n'

    tokens = list(tokenize(source))
    assert source == ''.join((source[t[1]:t[2]] for t in tokens))

    validate(path, source, tokens)
    normalize(path, source, tokens)

if __name__ == '__main__':
    format(sys.argv[1])
