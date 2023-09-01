from translate import Translator
from flask_babel import gettext

# required answerer attribute
# specifies which search query keywords triggers this answerer
keywords = ('Translation', 'انگلیسی', 'مترجم', 'ترجمه', 'Translator', 'translator', 'translation')

# required answerer function
# can return a list of results (any result type) for a given query

def answer(query):
    parts = query.query.split()
    if len(parts) != 2:
        return []
    translator = Translator(from_lang='en', to_lang='id')
    translated_text = translator.translate(query)
    return [{'answer': translated_text}]


# required answerer function
# returns information about the answerer
def self_info():
    return {
        'name': gettext('Multilingual translator'),
        'description': gettext('Translate the texts'),
        'examples': ['Translation {hello}'],
    }
