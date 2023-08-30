'''
هنوز کامل نشده!
'''

import urllib.request
import json
import difflib

from flask_babel import gettext
import re

# import logging

# logger: logging.Logger

default_on = True

name = gettext("Dictionary")
description = gettext(
    "لغت‌نامه موآ برگرفته از داده‌های واژه‌یاب"
)

preference_section = 'query'

query_keywords = ['املا', 'مترادف', 'متضاد', 'معنی', 'واژه', 'معادل']

query_examples = 'واژه حصین'

parser_re = re.compile('(املا|املای|مترادف|متضاد|معنی|واژه|کلمه|معادل|برابر) (.*)', re.I)


def spellcheck(wrong_spelling):
    url = "https://raw.githubusercontent.com/moa-engine/cdn/main/dicts/emlaei.json"
    response = urllib.request.urlopen(url)
    correct_spellings = json.loads(response.read())

    closest_spellings = difflib.get_close_matches(wrong_spelling, correct_spellings, n=1)

    if closest_spellings:
        closest_spelling = closest_spellings[0]
        return str(f"املای صحیح: {closest_spelling}")
    else:
        return str("هیچ املای صحیحی یافت نشد.")


def post_search(request, search):
    # process only on first page
    if search.search_query.pageno > 1:
        return True
    m = parser_re.match(search.search_query.query)
    if not m:
        # wrong query
        return True
    
    func, string = m.groups()
    result = None

    match func:
        case 'املا' | 'املای':
            result = spellcheck(string)

    if result:    
        search.result_container.answers["dict"] = {
            "answer": str(result)
        }

    return True