import argparse
import io
import sys


def _wc(file):
    """Returns line count, word count, char count in that order"""
    linec = wordc = charc = 0
    for line in file:
        linec += 1
        words = line.split()
        wordc += len(words)
        charc += sum(len(w) for w in words)
    return linec, wordc, charc


def wc(fname):
    with open(fname) as f:
        return _wc(f)


def tests():
    f = io.StringIO('The quick brown fox jumps over the lazy dog')
    assert _wc(f) == (1, 9, 35)

    f = io.StringIO(
        '''
        The quick brown fox jumps over the lazy dog
    '''
    )
    assert _wc(f) == (3, 9, 35)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    count = wc(args.filename)
    print(count)
