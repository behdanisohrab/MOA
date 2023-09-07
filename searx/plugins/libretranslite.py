from translate import Translator
from flask_babel import gettext
import re
from searx.utils import detect_language
from flask import Flask, request
# import logging

# logger: logging.Logger

default_on = True
name = gettext("libretranslite")
description = gettext(
    "مترجم لیبره ترنسلیت"
)

preference_section = 'query'

query_keywords = [ 'فارسی', 'انگلیسی', 'مترجم', 'ترجمه', 'معنی']

query_examples = 'ترجمه hi'

parser_re = re.compile('(انگلیسی|فارسی|ترجمه|مترجم) (.*)', re.I)




app = Flask(__name__)

@app.route('/')
def index():
    user_languages = request.accept_languages
    preferred_language = user_languages.best_match([ "fa-IR", "en", "ar", "az", "ca", "zh", "cs", "da", "nl", "eo", "fi", "fr", "de", "el", "he", "hu", "id", "ga", "it", "ja", "ko", "fa", "pl", "pt", "ru", "sk", "es", "sv", "tr", "uk"])
    return preferred_language

if __name__ == '__main__':
    app.run()




def spellcheck(wrong_spelling):
    query_lang = detect_language(wrong_spelling, threshold=0, only_search_languages= False)
    if query_lang != "None":
        translator = Translator(from_lang=query_lang, to_lang=index())
        translated_text = translator.translate(wrong_spelling)
        if translated_text:
            return str(f"ترجمه: {translated_text}")
        else:
            return str("خطا در ترجمه")
    else:
        return str("خطا در ترجمه")


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
        case 'ترجمه' | 'معنی':
            result = spellcheck(string)

    if result:
        search.result_container.answers["dict"] = {
            "answer": str(result)
        }

    return True


























