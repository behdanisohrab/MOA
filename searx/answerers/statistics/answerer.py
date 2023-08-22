from functools import reduce
from operator import mul, sub, truediv

from flask_babel import gettext


keywords = ('min', 'max', 'avg', 'sum', 'prod', 'sub', 'div', 'کمینه', 'حداقل', 'بیشینه', 'حداکثر', 'میانگین', 'جمع', 'ضرب', 'تفریق', 'تقسیم')


# required answerer function
# can return a list of results (any result type) for a given query
def answer(query):
    parts = query.query.split()

    if len(parts) < 2:
        return []

    try:
        args = list(map(float, parts[1:]))
    except:
        return []

    func = parts[0]

    match func:
        case 'min' | 'حداقل' | 'کمینه':
            answer = min(args)
        case 'max' | 'بیشینه' | 'حداکثر':
            answer = max(args)
        case 'svg' | 'میانگین':
            answer = sum(args) / len(args)
        case 'sum' | 'جمع':
            answer = sum(args)
        case 'prod' | 'ضرب':
            answer = reduce(mul, args)
        case 'sub' | 'تفریق':
            answer = reduce(sub, args)
        case 'div' | 'تقسیم':
            answer = reduce(truediv, args)
        case _:
            answer = None
        
    if answer is None:
        return []

    return [{'answer': str(answer)}]


# required answerer function
# returns information about the answerer
def self_info():
    return {
        'name': gettext('Statistics functions'),
        'description': gettext('Compute {functions} of the arguments').format(functions='/'.join(keywords)),
        'examples': ['avg 123 548 2.04 24.2'],
    }
