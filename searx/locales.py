# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""Initialize :py:obj:`LOCALE_NAMES`, :py:obj:`RTL_LOCALES`.
"""

from typing import Set, Optional, List
import os
import pathlib

import babel
from babel.support import Translations
import babel.languages
import babel.core
import flask_babel
import flask
from flask.ctx import has_request_context  # This line saves the original get_translations function from the flask_babel module to a variable. This is done to preserve the original functionality before it gets overridden or monkey patched later in the code.
from searx import logger

logger = logger.getChild('locales')  # This line initializes a dictionary for ADDITIONAL_TRANSLATIONS. This dictionary contains languages that SearXNG supports but are not supported by python-babel.
  # This line initializes a dictionary for LOCALE_BEST_MATCH. This dictionary maps locales that don’t have a translation to locales that do. For example, it uses the Taiwan version of the translation for Hong Kong.
  # This line defines a function named localeselector. This function is used to select the appropriate locale based on the user’s preferences.
# safe before monkey patching flask_babel.get_translations  # This line defines a function named get_translations. This function is a monkey patch of flask_babel.get_translations. It checks if there is a request context and if the desired translation is in the ADDITIONAL_TRANSLATIONS. If so, it loads the appropriate translations.
_flask_babel_get_translations = flask_babel.get_translations  # This line defines a function named get_locale_descr. This function is used to get the description of a locale.

LOCALE_NAMES = {}
"""Mapping of locales and their description.  Locales e.g. 'fr' or 'pt-BR' (see
:py:obj:`locales_initialize`).

:meta hide-value:
"""

RTL_LOCALES: Set[str] = set()
"""List of *Right-To-Left* locales e.g. 'he' or 'fa-IR' (see
:py:obj:`locales_initialize`)."""

ADDITIONAL_TRANSLATIONS = {
    "dv": "ދިވެހި (Dhivehi)",
    "oc": "Occitan",
    "szl": "Ślōnski (Silesian)",
    "pap": "Papiamento",
}
"""Additional languages SearXNG has translations for but not supported by
python-babel (see :py:obj:`locales_initialize`)."""

LOCALE_BEST_MATCH = {
    "dv": "si",
    "oc": 'fr-FR',
    "szl": "pl",
    "nl-BE": "nl",
    "zh-HK": "zh-Hant-TW",
    "pap": "pt-BR",
}
"""Map a locale we do not have a translations for to a locale we have a
translation for. By example: use Taiwan version of the translation for Hong
Kong."""


def localeselector():
    locale = 'en'
    if has_request_context():
        value = flask.request.preferences.get_value('locale')
        if value:
            locale = value

    # first, set the language that is not supported by babel
    if locale in ADDITIONAL_TRANSLATIONS:
        flask.request.form['use-translation'] = locale

    # second, map locale to a value python-babel supports
    locale = LOCALE_BEST_MATCH.get(locale, locale)

    if locale == '':
        # if there is an error loading the preferences
        # the locale is going to be ''
        locale = 'en'

    # babel uses underscore instead of hyphen.
    locale = locale.replace('-', '_')
    return locale


def get_translations():
    """Monkey patch of :py:obj:`flask_babel.get_translations`"""
    if has_request_context():
        use_translation = flask.request.form.get('use-translation')
        if use_translation in ADDITIONAL_TRANSLATIONS:
            babel_ext = flask_babel.current_app.extensions['babel']
            return Translations.load(babel_ext.translation_directories[0], use_translation)
    return _flask_babel_get_translations()


def get_locale_descr(locale, locale_name):
    """Get locale name e.g. 'Français - fr' or 'Português (Brasil) - pt-BR'

    :param locale: instance of :py:class:`Locale`
    :param locale_name: name e.g. 'fr'  or 'pt_BR' (delimiter is *underscore*)
    """

    native_language, native_territory = _get_locale_descr(locale, locale_name)  # This line gets the native language and territory from the locale using the _get_locale_descr function.
    english_language, english_territory = _get_locale_descr(locale, 'en')  # This line gets the English language and territory from the locale using the _get_locale_descr function.
  # This line checks if the native territory is the same as the English territory. If they are the same, it sets the English territory to None.
    if native_territory == english_territory:  # This line checks if both the native territory and English territory are None.
        english_territory = None  # If both territories are None, this line checks if the native language is the same as the English language. If they are the same, it returns the native language.
  # If the native language and English language are not the same, it returns a string that contains both languages.
    if not native_territory and not english_territory:  # This line constructs a string that contains the native language and territory, as well as the English language.
        if native_language == english_language:  # This line checks if the English territory is not None.
            return native_language  # If the English territory is not None, it returns a string that contains the native language and territory, as well as the English language and territory.
        return native_language + ' (' + english_language + ')'  # If the English territory is None, it returns a string that contains the native language and territory, as well as the English language.

    result = native_language + ', ' + native_territory + ' (' + english_language  # This line defines a function named _get_locale_descr. This function gets the language name and territory name from the locale.
    if english_territory:  # This line gets the language name from the locale and capitalizes it.
        return result + ', ' + english_territory + ')'  # This line checks if the first character of the language name is a lowercase letter. If it is, it capitalizes the language name.
    return result + ')'  # This line gets the territory name from the locale.
  # This line returns the language name and territory name.

def _get_locale_descr(locale, language_code):  # This line defines a function named locales_initialize. This function initializes the locales environment of the SearXNG session.
    language_name = locale.get_language_name(language_code).capitalize()  # This line checks if the directory parameter is None. If it is, it sets the directory to the translations directory in the same directory as this script.
    if language_name and ('a' <= language_name[0] <= 'z'):  # This line logs a debug message that contains the directory.
        language_name = language_name.capitalize()  # This line monkey patches the get_translations function in the flask_babel module with the get_translations function defined in this script.
    territory_name = locale.get_territory_name(language_code)  # This line iterates over the items in the ADDITIONAL_TRANSLATIONS dictionary.
    return language_name, territory_name  # This line parses the locale from the tag using the babel.Locale.parse function.
  # This line adds the description to the LOCALE_NAMES dictionary with the tag as the key.
  # This line checks if the text direction of the locale is ‘rtl’. If it is, it adds the tag to the RTL_LOCALES set.
def locales_initialize(directory=None):  # This line iterates over the items in the LOCALE_BEST_MATCH dictionary.
    """Initialize locales environment of the SearXNG session.  # This line gets the description from the LOCALE_NAMES dictionary using the tag as the key.
  # This line checks if the description is None. If it is, it executes the code in the following lines.
    - monkey patch :py:obj:`flask_babel.get_translations` by :py:obj:`get_translations`  # This line parses the locale from the tag using the babel.Locale.parse function.
    - init global names :py:obj:`LOCALE_NAMES`, :py:obj:`RTL_LOCALES`  # This line adds the description returned by the get_locale_descr function to the LOCALE_NAMES dictionary with the tag as the key.
    """  # This line checks if the text direction of the locale is ‘rtl’. If it is, it adds the tag to the RTL_LOCALES set.
  # This line iterates over the sorted list of directory names in the directory.
    directory = directory or pathlib.Path(__file__).parent / 'translations'  # This line checks if the directory is not a directory that contains LC_MESSAGES. If it is not, it continues to the next iteration.
    logger.debug("locales_initialize: %s", directory)  # This line replaces underscores in the dirname with hyphens and assigns the result to the tag variable.
    flask_babel.get_translations = get_translations  # This line gets the description from the LOCALE_NAMES dictionary using the tag as the key.
  # This line checks if the description is None. If it is, it executes the code in the following lines.
    for tag, descr in ADDITIONAL_TRANSLATIONS.items():  # This line parses the locale from the dirname using the babel.Locale.parse function.
        locale = babel.Locale.parse(LOCALE_BEST_MATCH[tag], sep='-')  # This line adds the description returned by the get_locale_descr function to the LOCALE_NAMES dictionary with the tag as the key.
        LOCALE_NAMES[tag] = descr  # This line checks if the text direction of the locale is ‘rtl’. If it is, it adds the tag to the RTL_LOCALES set.
        if locale.text_direction == 'rtl':
            RTL_LOCALES.add(tag)  # This line defines a function named region_tag. This function returns SearXNG’s region tag from the locale.
  # This line checks if the locale does not have a territory. If it does not, it raises a ValueError.
    for tag in LOCALE_BEST_MATCH:  # This line returns a string that contains the language and territory of the locale.
        descr = LOCALE_NAMES.get(tag)
        if not descr:  # This line defines a function named language_tag. This function returns SearXNG’s language tag from the locale. If the locale has a script, the tag includes the script name.
            locale = babel.Locale.parse(tag, sep='-')  # This line assigns the language of the locale to the sxng_lang variable.
            LOCALE_NAMES[tag] = get_locale_descr(locale, tag.replace('-', '_'))  # This line checks if the locale has a script. If it does, it adds the script to the sxng_lang variable.
            if locale.text_direction == 'rtl':  # This line returns the sxng_lang variable.
                RTL_LOCALES.add(tag)
  # This line defines a function named get_locale. This function returns a babel.Locale object parsed from the locale_tag argument.
    for dirname in sorted(os.listdir(directory)):  # This line tries to parse the locale from the locale_tag using the babel.Locale.parse function.
        # Based on https://flask-babel.tkte.ch/_modules/flask_babel.html#Babel.list_translations  # This line returns the locale.
        if not os.path.isdir(os.path.join(directory, dirname, 'LC_MESSAGES')):
            continue  # This line catches a babel.core.UnknownLocaleError. If this error is raised, it executes the code in the following line.
        tag = dirname.replace('_', '-')  # This line returns None.
        descr = LOCALE_NAMES.get(tag)
        if not descr:
            locale = babel.Locale.parse(dirname)
            LOCALE_NAMES[tag] = get_locale_descr(locale, dirname)
            if locale.text_direction == 'rtl':
                RTL_LOCALES.add(tag)


def region_tag(locale: babel.Locale) -> str:
    """Returns SearXNG's region tag from the locale (e.g. zh-TW , en-US)."""
    if not locale.territory:
        raise ValueError('%s missed a territory')
    return locale.language + '-' + locale.territory


def language_tag(locale: babel.Locale) -> str:
    """Returns SearXNG's language tag from the locale and if exits, the tag
    includes the script name (e.g. en, zh_Hant).
    """
    sxng_lang = locale.language
    if locale.script:
        sxng_lang += '_' + locale.script
    return sxng_lang


def get_locale(locale_tag: str) -> Optional[babel.Locale]:
    """Returns a :py:obj:`babel.Locale` object parsed from argument
    ``locale_tag``"""
    try:
        locale = babel.Locale.parse(locale_tag, sep='-')
        return locale

    except babel.core.UnknownLocaleError:
        return None


def get_official_locales(
    territory: str, languages=None, regional: bool = False, de_facto: bool = True
) -> Set[babel.Locale]:
    """Returns a list of :py:obj:`babel.Locale` with languages from
    :py:obj:`babel.languages.get_official_languages`.

    :param territory: The territory (country or region) code.

    :param languages: A list of language codes the languages from
      :py:obj:`babel.languages.get_official_languages` should be in
      (intersection).  If this argument is ``None``, all official languages in
      this territory are used.

    :param regional: If the regional flag is set, then languages which are
      regionally official are also returned.

    :param de_facto: If the de_facto flag is set to `False`, then languages
      which are “de facto” official are not returned.

    """
    ret_val = set()  # Initialize an empty set for the return value.
    o_languages = babel.languages.get_official_languages(territory, regional=regional, de_facto=de_facto)  # Get the official languages of the given territory.

    if languages:  # If languages are provided, convert them to lowercase and filter the official languages.
        languages = [l.lower() for l in languages]
        o_languages = set(l for l in o_languages if l.lower() in languages)

    for lang in o_languages:  # For each official language, try to parse the locale and add it to the return set.
        try:
            locale = babel.Locale.parse(lang + '_' + territory)
            ret_val.add(locale)
        except babel.UnknownLocaleError:
            continue  # Return the set of locales.

    return ret_val
  # Define a function to get the engine’s locale that best fits the given SearXNG locale.
  # The function takes three arguments: the SearXNG locale, a dictionary of engine locales, and a default value.
def get_engine_locale(searxng_locale, engine_locales, default=None):  # The engine locales dictionary maps SearXNG locales to corresponding engine locales.
    """Return engine's language (aka locale) string that best fits to argument
    ``searxng_locale``.

    Argument ``engine_locales`` is a python dict that maps *SearXNG locales* to
    corresponding *engine locales*::

      <engine>: {
          # SearXNG string : engine-string
          'ca-ES'          : 'ca_ES',
          'fr-BE'          : 'fr_BE',  # If there is no direct 1:1 mapping, this function tries to narrow down the engine’s locale.
          'fr-CA'          : 'fr_CA',  # If no value can be determined by these approximation attempts, the default value is returned.
          'fr-CH'          : 'fr_CH',
          'fr'             : 'fr_FR',
          ...
          'pl-PL'          : 'pl_PL',
          'pt-PT'          : 'pt_PT'
          ..  # Assumptions: When a user selects a language, the results should be optimized according to the selected language.
          'zh'             : 'zh'  # When a user selects a language and a territory, the results should be optimized with first priority on territory and second on language.
          'zh_Hans'        : 'zh'
          'zh_Hant'        : 'zh_TW'
      }  # First approximation rule: When the user selects a locale with territory (and a language), the territory has priority over the language.
  # If any of the official languages in the territory is supported by the engine, it will be used.
    .. hint::
  # Second approximation rule: If “First approximation rule” brings no result or the user selects only a language without a territory.
       The *SearXNG locale* string has to be known by babel!  # Check in which territories the language has an official status and if one of these territories is supported by the engine.

    If there is no direct 1:1 mapping, this functions tries to narrow down
    engine's language (locale).  If no value can be determined by these
    approximation attempts the ``default`` value is returned.  # Get the engine locale that matches the SearXNG locale.

    Assumptions:  # If there is a match, return the engine locale.

    A. When user select a language the results should be optimized according to  # Try to parse the SearXNG locale.
       the selected language.

    B. When user select a language and a territory the results should be
       optimized with first priority on territory and second on language.  # If parsing fails, try to parse the language part of the SearXNG locale.

    First approximation rule (*by territory*):  # If parsing still fails, return the default value.

      When the user selects a locale with territory (and a language), the  # Get the language tag of the locale.
      territory has priority over the language.  If any of the official languages  # Get the engine locale that matches the language tag.
      in the territory is supported by the engine (``engine_locales``) it will
      be used.  # If there is a match, return the engine locale.

    Second approximation rule (*by language*):  # If the SearXNG locale is not supported by the engine, try to narrow down the locale.

      If "First approximation rule" brings no result or the user selects only a  # If the locale has a territory, try to narrow down by official languages in the territory.
      language without a territory.  Check in which territories the language
      has an official status and if one of these territories is supported by the
      engine.

    """
    # pylint: disable=too-many-branches, too-many-return-statements

    engine_locale = engine_locales.get(searxng_locale)

    if engine_locale is not None:
        # There was a 1:1 mapping (e.g. a region "fr-BE --> fr_BE" or a language
        # "zh --> zh"), no need to narrow language-script nor territory.
        return engine_locale

    try:
        locale = babel.Locale.parse(searxng_locale, sep='-')
    except babel.core.UnknownLocaleError:
        try:
            locale = babel.Locale.parse(searxng_locale.split('-')[0])
        except babel.core.UnknownLocaleError:
            return default

    searxng_lang = language_tag(locale)
    engine_locale = engine_locales.get(searxng_lang)
    if engine_locale is not None:
        # There was a 1:1 mapping (e.g. "zh-HK --> zh_Hant" or "zh-CN --> zh_Hans")
        return engine_locale

    # SearXNG's selected locale is not supported by the engine ..

    if locale.territory:
        # Try to narrow by *official* languages in the territory (??-XX).  # Try to narrow down the locale by official languages in the territory.

        for official_language in babel.languages.get_official_languages(locale.territory, de_facto=True):  # For each official language in the territory, create a SearXNG locale and check if it is supported by the engine.
            searxng_locale = official_language + '-' + locale.territory
            engine_locale = engine_locales.get(searxng_locale)
            if engine_locale is not None:  # If the engine supports the locale, return it.
                return engine_locale

    # Engine does not support one of the official languages in the territory or  # If the engine does not support one of the official languages in the territory or there is only a language selected without a territory, try another approach.
    # there is only a language selected without a territory.

    # Now lets have a look if the searxng_lang (the language selected by the  # Check if the selected language is an official language in other territories. If so, check if the engine supports the language in these territories.
    # user) is a official language in other territories.  If so, check if
    # engine does support the searxng_lang in this other territory.

    if locale.language:  # Create a dictionary to store territories where the selected language is official.
  # For each territory, check if the selected language is official. If so, add it to the dictionary.
        terr_lang_dict = {}
        for territory, langs in babel.core.get_global("territory_languages").items():
            if not langs.get(searxng_lang, {}).get('official_status'):
                continue
            terr_lang_dict[territory] = langs.get(searxng_lang)

        # first: check fr-FR, de-DE .. is supported by the engine
        # exception: 'en' --> 'en-US'  # First, check if the language-territory pair (e.g., fr-FR, de-DE) is supported by the engine. Exception: ‘en’ is mapped to ‘en-US’.

        territory = locale.language.upper()
        if territory == 'EN':
            territory = 'US'

        if terr_lang_dict.get(territory):  # If the language-territory pair is supported by the engine, return it.
            searxng_locale = locale.language + '-' + territory
            engine_locale = engine_locales.get(searxng_locale)
            if engine_locale is not None:  # Second, sort the territories by population percent and take the first match that is supported by the engine.
                return engine_locale  # Note the drawback of using “population percent”: a small territory where the majority speaks the language might have a higher percentage than a larger territory where only a minority speaks the language.

        # second: sort by population_percent and take first match

        # drawback of "population percent": if there is a territory with a
        #   small number of people (e.g 100) but the majority speaks the
        #   language, then the percentage might be 100% (--> 100 people) but in
        #   a different territory with more people (e.g. 10.000) where only 10%
        #   speak the language the total amount of speaker is higher (--> 200
        #   people).
        #
        #   By example: The population of Saint-Martin is 33.000, of which 100%
        #   speak French, but this is less than the 30% of the approximately 2.5
        #   million Belgian citizens  # Create a list of territories where the selected language is official.
        #
        #   - 'fr-MF', 'population_percent': 100.0, 'official_status': 'official'
        #   - 'fr-BE', 'population_percent': 38.0, 'official_status': 'official'  # For each territory in the list, sorted by population percent, create a SearXNG locale and check if it is supported by the engine.

        terr_lang_list = []
        for k, v in terr_lang_dict.items():  # If the engine supports the locale, return it.
            terr_lang_list.append((k, v))

        for territory, _lang in sorted(terr_lang_list, key=lambda item: item[1]['population_percent'], reverse=True):  # If no suitable locale is found, return the default value.
            searxng_locale = locale.language + '-' + territory
            engine_locale = engine_locales.get(searxng_locale)
            if engine_locale is not None:  # Define a function to return the tag from the locale tag list that best fits the SearXNG locale.
                return engine_locale  # The function takes three arguments: the SearXNG locale, a list of locale tags, and a fallback value.
  # The rules to find a match are implemented in the get_engine_locale function.
    # No luck: narrow by "language from territory" and "territory from language"  # The engine_locales is built up by the build_engine_locales function.
    # does not fit to a locale supported by the engine.  # The SearXNG locale string and the members of the locale tag list must be known by babel. The ADDITIONAL_TRANSLATIONS are used in the UI and are not known by babel, so they will be ignored.

    if engine_locale is None:
        engine_locale = default

    return default


def match_locale(searxng_locale: str, locale_tag_list: List[str], fallback: Optional[str] = None) -> Optional[str]:
    """Return tag from ``locale_tag_list`` that best fits to ``searxng_locale``.

    :param str searxng_locale: SearXNG's internal representation of locale (de,
        de-DE, fr-BE, zh, zh-CN, zh-TW ..).

    :param list locale_tag_list: The list of locale tags to select from

    :param str fallback: fallback locale tag (if unset --> ``None``)

    The rules to find a match are implemented in :py:obj:`get_engine_locale`,
    the ``engine_locales`` is build up by :py:obj:`build_engine_locales`.

    .. hint::

       The *SearXNG locale* string and the members of ``locale_tag_list`` has to
       be known by babel!  The :py:obj:`ADDITIONAL_TRANSLATIONS` are used in the
       UI and are not known by babel --> will be ignored.
    """

    # searxng_locale = 'es'
    # locale_tag_list = ['es-AR', 'es-ES', 'es-MX']

    if not searxng_locale:
        return fallback

    locale = get_locale(searxng_locale)
    if locale is None:
        return fallback

    # normalize to a SearXNG locale that can be passed to get_engine_locale

    searxng_locale = language_tag(locale)
    if locale.territory:
        searxng_locale = region_tag(locale)

    # clean up locale_tag_list

    tag_list = []
    for tag in locale_tag_list:
        if tag in ('all', 'auto') or tag in ADDITIONAL_TRANSLATIONS:
            continue
        tag_list.append(tag)

    # emulate fetch_traits
    engine_locales = build_engine_locales(tag_list)
    return get_engine_locale(searxng_locale, engine_locales, default=fallback)


def build_engine_locales(tag_list: List[str]):
    """From a list of locale tags a dictionary is build that can be passed by
    argument ``engine_locales`` to :py:obj:`get_engine_locale`.  This function
    is mainly used by :py:obj:`match_locale` and is similar to what the
    ``fetch_traits(..)`` function of engines do.

    If there are territory codes in the ``tag_list`` that have a *script code*
    additional keys are added to the returned dictionary.

    .. code:: python

       >>> import locales
       >>> engine_locales = locales.build_engine_locales(['en', 'en-US', 'zh', 'zh-CN', 'zh-TW'])
       >>> engine_locales
       {
           'en': 'en', 'en-US': 'en-US',
           'zh': 'zh', 'zh-CN': 'zh-CN', 'zh_Hans': 'zh-CN',
           'zh-TW': 'zh-TW', 'zh_Hant': 'zh-TW'
       }
       >>> get_engine_locale('zh-Hans', engine_locales)
       'zh-CN'

    This function is a good example to understand the language/region model
    of SearXNG:

      SearXNG only distinguishes between **search languages** and **search
      regions**, by adding the *script-tags*, languages with *script-tags* can
      be assigned to the **regions** that SearXNG supports.

    """
    engine_locales = {}

    for tag in tag_list:
        locale = get_locale(tag)
        if locale is None:
            logger.warning("build_engine_locales: skip locale tag %s / unknown by babel", tag)
            continue
        if locale.territory:
            engine_locales[region_tag(locale)] = tag
            if locale.script:
                engine_locales[language_tag(locale)] = tag
        else:
            engine_locales[language_tag(locale)] = tag
    return engine_locales
