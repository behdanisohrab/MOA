import openai
from flask_babel import gettext
import requests
from urllib.parse import urlencode
from searx.utils import detect_language
import re


# import logging

# logger: logging.Logger

default_on = True
name = gettext("AI")
description = gettext(
    "پاسخ سریع هوش مصنوعی"
)

preference_section = 'query'
query_keywords = ['هوش:', 'AI', 'chatgpt', 'hava', 'حوا:', 'ChatGPT', 'ai']
query_examples = 'هوش مصنوعی موآ چیست؟'
parser_re = re.compile('(حوا:|هوش:|hava|ChatGPT|chatgpt|ai|AI) (.*)', re.I)


def spellcheck(wrong_spelling):
    query_lang = detect_language(wrong_spelling, threshold=0, only_search_languages= False)
    if query_lang == "fa" or query_lang == "fa-IR":
        base_url = "https://api.pamickweb.com/API/chat.php"
        server = "server1"
        params = {"server": server, "text": wrong_spelling}
        url = base_url + "?" + urlencode(params)

        response = requests.get(url)
        if response.status_code == 200:
            text_response = response.text
            return str(text_response)
        else:
            return str("خطا در اتصال به حوا")
    else:
        openai.api_key = "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"

        model_engine = "text-davinci-003"

        completion = openai.Completion.create(
            engine = model_engine,
            prompt = wrong_spelling,
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.5,
        )

        response = completion.choices[0].text
        return str(response)




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
        case 'chatgpt' | 'هوش مصنوعی':
            result = spellcheck(string)

    if result:
        search.result_container.answers["dict"] = {
            "answer": str(result)
        }

    return True
