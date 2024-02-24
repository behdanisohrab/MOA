# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
SearXNG’s locale data
=====================

The variables :py:obj:`RTL_LOCALES` and :py:obj:`LOCALE_NAMES` are loaded from
:origin:`searx/data/locales.json` / see :py:obj:`locales_initialize` and
:ref:`update_locales.py`.

.. hint::

   Whenever the value of :py:obj:`ADDITIONAL_TRANSLATIONS` or
   :py:obj:`LOCALE_BEST_MATCH` is modified, the
   :origin:`searx/data/locales.json` needs to be rebuild::

     ./manage data.locales

SearXNG's locale codes
======================

.. automodule:: searx.sxng_locales
   :members:


SearXNG’s locale implementations
================================
"""

from __future__ import annotations

from pathlib import Path

import babel
from babel.support import Translations
import babel.languages
import babel.core
import flask_babel
import flask
from flask.ctx import has_request_context
from searx import (
    data,
    logger,
    searx_dir,
)


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

RTL_LOCALES: set[str] = set()
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
translation for.  By example: use Taiwan version of the translation for Hong
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


_TR_LOCALES: list[str] = []


def get_translation_locales() -> list[str]:
    """Returns the list of transaltion locales (*underscore*).  The list is
    generated from the translation folders in :origin:`searx/translations`"""

    global _TR_LOCALES  # pylint:disable=global-statement
    if _TR_LOCALES:
        return _TR_LOCALES

    tr_locales = []
    for folder in (Path(searx_dir) / 'translations').iterdir():
        if not folder.is_dir():
            continue
        if not (folder / 'LC_MESSAGES').is_dir():
            continue
        tr_locales.append(folder.name)
    _TR_LOCALES = sorted(tr_locales)
    return _TR_LOCALES


def locales_initialize():
    """Initialize locales environment of the SearXNG session.

    - monkey patch :py:obj:`flask_babel.get_translations` by :py:obj:`get_translations`
    - init global names :py:obj:`LOCALE_NAMES`, :py:obj:`RTL_LOCALES`
    """
    flask_babel.get_translations = get_translations
    LOCALE_NAMES.update(data.LOCALES["LOCALE_NAMES"])
    RTL_LOCALES.update(data.LOCALES["RTL_LOCALES"])


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


def get_locale(locale_tag: str) -> babel.Locale | None:
    """Returns a :py:obj:`babel.Locale` object parsed from argument
    ``locale_tag``"""
    try:
        locale = babel.Locale.parse(locale_tag, sep='-')
        return locale

    except babel.core.UnknownLocaleError:
        return None


def get_official_locales(
    territory: str, languages=None, regional: bool = False, de_facto: bool = True
) -> set[babel.Locale]:
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


def match_locale(searxng_locale: str, locale_tag_list: list[str], fallback: str | None = None) -> str | None:
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


def build_engine_locales(tag_list: list[str]):
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
