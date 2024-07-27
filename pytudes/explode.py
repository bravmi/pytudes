import itertools as it
import re
from typing import Iterable


def explode(pattern: str) -> Iterable[str]:
    """
    Expand the brace-delimited possibilities in a string.
    """
    seg_choices = []
    for segment in re.split(r'(\{.*?\})', pattern):
        if segment.startswith('{'):
            seg_choices.append(segment.strip('{}').split(','))
        else:
            seg_choices.append([segment])

    for parts in it.product(*seg_choices):
        yield ''.join(parts)


def tests():
    assert list(explode("{Alice,Bob} ate a {banana,donut}.")) == [
        'Alice ate a banana.',
        'Alice ate a donut.',
        'Bob ate a banana.',
        'Bob ate a donut.',
    ]


if __name__ == '__main__':
    tests()
