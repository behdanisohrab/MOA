import json
import difflib

from flask_babel import gettext


keywords = ['املا', 'مترادف', 'متضاد', 'معنی', 'واژه', 'معادل']

def spellcheck(wrong_spelling):
    with open("dicts/emlaei.json", "w") as json_file:
        correct_spellings = json.load(json_file)

    closest_spellings = difflib.get_close_matches(wrong_spelling, correct_spellings, n=1)

    if closest_spellings:
        closest_spelling = closest_spellings[0]
        return str(f"املا صحیح: {closest_spelling}")
    else:
        return str("هیچ املا صحیحی یافت نشد.")


# required answerer function
# can return a list of results (any result type) for a given query
def answer(query):
    parts = query.query.split()

    if len(parts) < 2:
        return []

    func = parts[0]

    match func:
        case 'املا' | 'املای':
            answer = spellcheck(parts[1])
        case _:
            answer = None
        
    if answer is None:
        return []

    return [{'answer': str(answer)}]


# required answerer function
# returns information about the answerer
def self_info():
    return {
        'name': gettext('لغت‌نامه پارسی'),
        'description': gettext('Compute {functions} of the arguments').format(functions='/'.join(keywords)),
        'examples': ['avg 123 548 2.04 24.2'],
    }
