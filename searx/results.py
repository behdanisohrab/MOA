# SPDX-License-Identifier: AGPL-3.0-or-later
# pylint: disable=missing-module-docstring
import re  # Importing necessary modules and functions.

from collections import defaultdict
from operator import itemgetter  # Importing defaultdict from collections module.
from threading import RLock  # Importing itemgetter from operator module.
from typing import List, NamedTuple, Set  # Importing RLock from threading module.
from urllib.parse import urlparse, unquote  # Importing List, NamedTuple, Set from typing module.
  # Importing urlparse, unquote from urllib.parse module.
from searx import logger
from searx import utils  # Importing logger from searx module.
from searx.engines import engines  # Importing utils from searx module.
from searx.metrics import histogram_observe, counter_add, count_error  # Importing engines from searx.engines module.
  # Importing histogram_observe, counter_add, count_error from searx.metrics module.

CONTENT_LEN_IGNORED_CHARS_REGEX = re.compile(  # Defining a regular expression pattern to ignore certain characters in content length calculation.
    r'[,;:!?\./\\\\ ()-_]', re.M | re.U)  # Defining a regular expression pattern to match one or more occurrences of whitespace characters.
WHITESPACE_REGEX = re.compile('( |\t|\n)+', re.M | re.U)

  # Defining a function to calculate the meaningful length of the content for a result.
# return the meaningful length of the content for a result
def result_content_len(content):
    if isinstance(content, str):
        return len(CONTENT_LEN_IGNORED_CHARS_REGEX.sub('', content))
    return 0


def compare_urls(url_a, url_b):
    """Lazy compare between two URL.
    "www.example.com" and "example.com" are equals.
    "www.example.com/path/" and "www.example.com/path" are equals.
    "https://www.example.com/" and "http://www.example.com/" are equals.

    Args:
        url_a (ParseResult): first URL
        url_b (ParseResult): second URL

    Returns:
        bool: True if url_a and url_b are equals
    """
    # ignore www. in comparison
    if url_a.netloc.startswith('www.'):  # Defining a function to merge two infoboxes. It gets the weights of the engines and compares them. If the weight of the second engine is greater than the weight of the first engine, it replaces the engine of the first infobox with the engine of the second infobox. It also merges the engines and URLs of the two infoboxes.
        host_a = url_a.netloc.replace('www.', '', 1)
    else:
        host_a = url_a.netloc
    if url_b.netloc.startswith('www.'):
        host_b = url_b.netloc.replace('www.', '', 1)
    else:
        host_b = url_b.netloc

    if host_a != host_b or url_a.query != url_b.query or url_a.fragment != url_b.fragment:
        return False

    # remove / from the end of the url if required
    path_a = url_a.path[:-1] if url_a.path.endswith('/') else url_a.path
    path_b = url_b.path[:-1] if url_b.path.endswith('/') else url_b.path

    return unquote(path_a) == unquote(path_b)


def merge_two_infoboxes(infobox1, infobox2):  # pylint: disable=too-many-branches, too-many-statements
    # get engines weights
    if hasattr(engines[infobox1['engine']], 'weight'):
        weight1 = engines[infobox1['engine']].weight
    else:
        weight1 = 1
    if hasattr(engines[infobox2['engine']], 'weight'):
        weight2 = engines[infobox2['engine']].weight
    else:
        weight2 = 1

    if weight2 > weight1:
        infobox1['engine'] = infobox2['engine']

    infobox1['engines'] |= infobox2['engines']

    if 'urls' in infobox2:
        urls1 = infobox1.get('urls', None)
        if urls1 is None:
            urls1 = []

        for url2 in infobox2.get('urls', []):
            unique_url = True
            parsed_url2 = urlparse(url2.get('url', ''))
            entity_url2 = url2.get('entity')
            for url1 in urls1:
                if (entity_url2 is not None and url1.get('entity') == entity_url2) or compare_urls(
                    urlparse(url1.get('url', '')), parsed_url2
                ):
                    unique_url = False
                    break
            if unique_url:
                urls1.append(url2)

        infobox1['urls'] = urls1

    if 'img_src' in infobox2:  # Checking if ‘img_src’ is in the second infobox. If it is, the image source from the second infobox is retrieved.
        img1 = infobox1.get('img_src', None)  # Retrieving the image source from the first infobox.
        img2 = infobox2.get('img_src')  # Retrieving the image source from the second infobox.
        if img1 is None:  # If the image source from the first infobox is None, the image source from the second infobox is assigned to the first infobox.
            infobox1['img_src'] = img2  # If the weight of the second engine is greater than the weight of the first engine, the image source from the second infobox is assigned to the first infobox.
        elif weight2 > weight1:
            infobox1['img_src'] = img2  # Checking if ‘attributes’ is in the second infobox. If it is, the attributes from the second infobox are retrieved.
  # Retrieving the attributes from the first infobox.
    if 'attributes' in infobox2:  # If the attributes from the first infobox are None, an empty list is assigned to the attributes of the first infobox.
        attributes1 = infobox1.get('attributes')
        if attributes1 is None:  # Creating an empty set for the attributes.
            infobox1['attributes'] = attributes1 = []  # Iterating over the attributes from the first infobox.
  # Retrieving the label of the attribute.
        attributeSet = set()  # If the label is not in the attribute set, it is added to the set.
        for attribute in attributes1:  # Retrieving the entity of the attribute.
            label = attribute.get('label')  # If the entity is not in the attribute set, it is added to the set.
            if label not in attributeSet:
                attributeSet.add(label)  # Iterating over the attributes from the second infobox.
            entity = attribute.get('entity')  # If the label and entity of the attribute are not in the attribute set, the attribute is appended to the attributes of the first infobox.
            if entity not in attributeSet:
                attributeSet.add(entity)  # Checking if ‘content’ is in the second infobox. If it is, the content from the second infobox is retrieved.
  # Retrieving the content from the first infobox.
        for attribute in infobox2.get('attributes', []):  # Retrieving the content from the second infobox.
            if attribute.get('label') not in attributeSet and attribute.get('entity') not in attributeSet:  # If the content from the first infobox is not None, the content lengths of the first and second infoboxes are compared.
                attributes1.append(attribute)  # If the content length of the second infobox is greater than the content length of the first infobox, the content from the second infobox is assigned to the first infobox.

    if 'content' in infobox2:  # If the content from the first infobox is None, the content from the second infobox is assigned to the first infobox.
        content1 = infobox1.get('content', None)
        content2 = infobox2.get('content', '')  # Defining a function to calculate the score of a result. The score is calculated by multiplying the weight of the engine by the number of occurrences and dividing by the position.
        if content1 is not None:
            if result_content_len(content2) > result_content_len(content1):
                infobox1['content'] = content2
        else:
            infobox1['content'] = content2


def result_score(result):
    weight = 1.0  # Defining a class for timing. It contains the engine name, total time, and load time.

    for result_engine in result['engines']:
        if hasattr(engines[result_engine], 'weight'):
            weight *= float(engines[result_engine].weight)  # Defining a class for unresponsive engines. It contains the engine name, error type, and a boolean indicating whether the engine is suspended.

    occurrences = len(result['positions'])

    return sum((occurrences * weight) / position for position in result['positions'])  # Defining a class for the result container. It contains various attributes such as merged results, infoboxes, suggestions, answers, corrections, number of results, closed status, paging status, unresponsive engines, timings, redirect URL, engine data, on result function, lock, and result merge.


class Timing(NamedTuple):  # pylint: disable=missing-class-docstring
    engine: str
    total: float
    load: float


class UnresponsiveEngine(NamedTuple):  # pylint: disable=missing-class-docstring
    engine: str
    error_type: str
    suspended: bool


class ResultContainer:  # Defining a function to extend the result container. If the result container is closed, the function returns immediately
    """docstring for ResultContainer"""

    __slots__ = (
        '_merged_results',
        'infoboxes',
        'suggestions',
        'answers',
        'corrections',
        '_number_of_results',
        '_closed',
        'paging',
        'unresponsive_engines',
        'timings',
        'redirect_url',
        'engine_data',
        'on_result',
        '_lock',
        'result_merge'
    )

    def __init__(self):
        super().__init__()
        self._merged_results = []
        self.infoboxes = []
        self.suggestions = set()
        self.answers = {}
        self.corrections = set()
        self._number_of_results = []
        self.engine_data = defaultdict(dict)
        self._closed = False
        self.paging = False
        self.unresponsive_engines: Set[UnresponsiveEngine] = set()
        self.timings: List[Timing] = []
        self.redirect_url = None
        self.on_result = lambda _: True
        self._lock = RLock()
        self.result_merge = True

    def extend(self, engine_name, results):  # pylint: disable=too-many-branches
        if self._closed:
            return

        standard_result_count = 0  # Initializing the count of standard results to 0.
        error_msgs = set()  # Creating a set to store error messages.
        for result in list(results):  # Iterating over the results.
            result['engine'] = engine_name  # Assigning the engine name to the ‘engine’ key of the result.
            if 'suggestion' in result and self.on_result(result):  # If the result contains a ‘suggestion’ and the on_result function returns True, the suggestion is added to the suggestions set.
                self.suggestions.add(result['suggestion'])  # If the result contains an ‘answer’ and the on_result function returns True, the answer is added to the answers dictionary.
            elif 'answer' in result and self.on_result(result):  # If the result contains a ‘correction’ and the on_result function returns True, the correction is added to the corrections set.
                self.answers[result['answer']] = result  # If the result contains an ‘infobox’ and the on_result function returns True, the _merge_infobox function is called with the result as an argument. 207- If the result contains a ‘number_of_results’ and the on_result function returns True, the number of results is appended to the _number_of_results list.
            elif 'correction' in result and self.on_result(result):
                self.corrections.add(result['correction'])  # If the result contains ‘engine_data’ and the on_result function returns True, the engine data is added to the engine_data dictionary.
            elif 'infobox' in result and self.on_result(result):  # If the result contains a ‘url’, it is considered a standard result (url, title, content).
                self._merge_infobox(result)  # If the _is_valid_url_result function returns False for the result, the loop continues to the next iteration.
            elif 'number_of_results' in result and self.on_result(result):  # The _normalize_url_result function is called with the result as an argument to normalize the result.
                self._number_of_results.append(result['number_of_results'])  # The on_result function is called with the result as an argument. If it returns False, the loop continues to the next iteration.
            elif 'engine_data' in result and self.on_result(result):  # The __merge_url_result function is called with the result and the count of standard results plus 1 as arguments.
                self.engine_data[engine_name][result['key']  # The count of standard results is incremented by 1.
                                              ] = result['engine_data']  # If the on_result function returns True for the result, the __merge_result_no_url function is called with the result and the count of standard results plus 1 as arguments.
            elif 'url' in result:  # The count of standard results is incremented by 1.
                # standard result (url, title, content)
                if not self._is_valid_url_result(result, error_msgs):  # If there are any error messages, they are added to the count of errors.
                    continue
                # normalize the result
                self._normalize_url_result(result)  # If the engine name is in the engines dictionary, the count of standard results is observed in the histogram.
                # call on_result call searx.search.SearchWithPlugins._on_result
                # which calls the plugins  # If paging is not enabled and the engine name is in the engines dictionary and paging is enabled for the engine, paging is set to True.
                if not self.on_result(result):
                    continue  # Defining a function to merge infoboxes. It checks if the infobox has an ID. If it does, it compares the ID with the IDs of existing infoboxes. If the IDs match, the infoboxes are merged.
                self.__merge_url_result(result, standard_result_count + 1)
                standard_result_count += 1
            elif self.on_result(result):
                self.__merge_result_no_url(result, standard_result_count + 1)
                standard_result_count += 1

        if len(error_msgs) > 0:
            for msg in error_msgs:
                count_error(
                    engine_name, 'some results are invalids: ' + msg, secondary=True)  # Defining a function to check if a result with a URL is valid. It checks if the URL, title, and content are strings. If they are not, it adds an error message and returns False.

        if engine_name in engines:
            histogram_observe(standard_result_count, 'engine',
                              engine_name, 'result', 'count')

        if not self.paging and engine_name in engines and engines[engine_name].paging:
            self.paging = True

    def _merge_infobox(self, infobox):
        add_infobox = True  # Defining a function to normalize a URL result. It parses the URL and assigns it to the ‘parsed_url’ key of the result. If the parsed URL does not have a scheme, it sets the scheme to “http” and updates the ‘url’ key of the result.
        infobox_id = infobox.get('id', None)
        infobox['engines'] = set([infobox['engine']])
        if infobox_id is not None:
            parsed_url_infobox_id = urlparse(infobox_id)
            with self._lock:
                for existingIndex in self.infoboxes:
                    if compare_urls(urlparse(existingIndex.get('id', '')), parsed_url_infobox_id):
                        merge_two_infoboxes(existingIndex, infobox)
                        add_infobox = False

        if add_infobox:
            self.infoboxes.append(infobox)

    def _is_valid_url_result(self, result, error_msgs):
        if 'url' in result:
            if not isinstance(result['url'], str):
                logger.debug('result: invalid URL: %s', str(result))
                error_msgs.add('invalid URL')
                return False

        if 'title' in result and not isinstance(result['title'], str):
            logger.debug('result: invalid title: %s', str(result))
            error_msgs.add('invalid title')
            return False

        if 'content' in result:
            if not isinstance(result['content'], str):
                logger.debug('result: invalid content: %s', str(result))
                error_msgs.add('invalid content')
                return False

        return True

    def _normalize_url_result(self, result):
        """Return True if the result is valid"""
        result['parsed_url'] = urlparse(result['url'])

        # if the result has no scheme, use http as default
        if not result['parsed_url'].scheme:
            result['parsed_url'] = result['parsed_url']._replace(scheme="http")
            result['url'] = result['parsed_url'].geturl()

        # avoid duplicate content between the content and title fields
        if result.get('content') == result.get('title'):
            del result['content']

        # make sure there is a template
        if 'template' not in result:
            result['template'] = 'default.html'

        # strip multiple spaces and carriage returns from content
        if result.get('content'):
            result['content'] = WHITESPACE_REGEX.sub(' ', result['content'])

    def __merge_url_result(self, result, position):  # Define a method to merge URL results
        result['engines'] = set([result['engine']])  # Add the engine to the result set
        with self._lock:  # Start a locked section to prevent race conditions
            duplicated = self.__find_duplicated_http_result(result)  # Check for duplicate HTTP results
            if duplicated:  # If a duplicate is found, merge it with the current result and return
                self.__merge_duplicated_http_result(
                    duplicated, result, position)
                return
  # If no duplicate is found, add the current position to the result’s positions
            # if there is no duplicate found, append result  # Append the result to the merged results list
            result['positions'] = [position]
            self._merged_results.append(result)  # Define a method to find duplicated HTTP results  # Define a method to merge duplicated HTTP results
  # Get the template from the result
    def __find_duplicated_http_result(self, result):  # Iterate over the merged results  # If the content length of the result is greater than the duplicated one, use the result’s content
        result_template = result.get('template')  # Skip the current iteration if ‘parsed_url’ is not in the merged result
        for merged_result in self._merged_results:  # Compare the URLs and check if the templates are the same
            if 'parsed_url' not in merged_result:  # Merge all result’s parameters not found in the duplicate
                continue  # If the template is not ‘images.html’, it’s a duplicate if the URLs and templates are the same
            if compare_urls(result['parsed_url'], merged_result['parsed_url']) and result_template == merged_result.get(
                'template'
            ):  # Add the new position to the duplicate’s positions
                if result_template != 'images.html':
                    # not an image, same template, same url : it's a duplicate

                    return merged_result

                # it's an image
                # it's a duplicate if the parsed_url, template and img_src are different
                if result.get('img_src', '') == merged_result.get('img_src', ''):
                    return merged_result
        return None
  # Define a method to merge results without a URL
    def __merge_duplicated_http_result(self, duplicated, result, position):  # Add the result’s engine to the result’s engines
        # using content with more text  # Add the current position to the result’s positions
        if result_content_len(result.get('content', '')) > result_content_len(duplicated.get('content', '')):
            duplicated['content'] = result['content']  # Append the result to the merged results list

        # merge all result's parameters not found in duplicate  # Define a method to close the merger
        for key in result.keys():  # Set the closed flag to True
            if not duplicated.get(key):
                duplicated[key] = result.get(key)  # Calculate the score for each result in the merged results

        # add the new position
        duplicated['positions'].append(position)  # Convert the result’s content to text and strip it

        # add engine to list of result-engines
        duplicated['engines'].add(result['engine'])  # Remove HTML content and whitespace duplications from the result’s title

        # using https if possible  # Add the result’s score to the engine’s score
        if duplicated['parsed_url'].scheme != 'https' and result['parsed_url'].scheme == 'https':
            duplicated['url'] = result['parsed_url'].geturl()
            duplicated['parsed_url'] = result['parsed_url']  # Sort the merged results by score in descending order

    def __merge_result_no_url(self, result, position):
        result['engines'] = set([result['engine']])  # Group the results by category and template
        result['positions'] = [position]
        with self._lock:
            self._merged_results.append(result)
  # Get the engine from the result’s engine
    def close(self):
        self._closed = True
  # Set the result’s category to the engine’s first category if it exists
        for result in self._merged_results:
            score = result_score(result)
            result['score'] = score

            # removing html content and whitespace duplications
            if result.get('content'):
                result['content'] = utils.html_to_text(result['content']).strip()
            if result.get('title'):
                result['title'] = ' '.join(utils.html_to_text(result['title']).strip().split())

            for result_engine in result['engines']:
                counter_add(score, 'engine', result_engine, 'score')

        results = sorted(self._merged_results,
                         key=itemgetter('score'), reverse=True)

        # pass 2 : group results by category and template
        gresults = []
        categoryPositions = {}

        for res in results:
            # do we need to handle more than one category per engine?
            engine = engines[res['engine']]

            # Limit the number of results of images category

            res['category'] = engine.categories[0] if len(
                engine.categories) > 0 else ''
            # FIXME : handle more than one category per engine

            category = (
                res['category']
                + ':'
                + res.get('template', '')
                + ':'
                + ('img_src' if 'img_src' in res or 'thumbnail' in res else '')
            )

            current = None if category not in categoryPositions else categoryPositions[
                category]

            # group with previous results using the same category  # Group with previous results using the same category if the group can accept more results and is not too far from the current position
            # if the group can accept more result and is not too far
            # from the current position
            if current is not None and (current['count'] > 0) and (len(gresults) - current['index'] < 20):
                # group with the previous results using
                # the same category with this one  # Insert the result at the current index in the grouped results
                index = current['index']
                gresults.insert(index, res)
                # Update every index after the current one (including the current one)
                # update every index after the current one
                # (including the current one)
                for k in categoryPositions:  # pylint: disable=consider-using-dict-items
                    v = categoryPositions[k]['index']
                    if v >= index:  # Decrease the count of the current category by 1
                        categoryPositions[k]['index'] = v + 1

                # update this category  # If the current category is None or the count is 0 or the current index is too far from the end of the grouped results, append the result to the grouped results
                current['count'] -= 1

            else:  # Update the category positions with the current category’s index and count
                # same category
                gresults.append(res)

                # update categoryIndex  # Update the merged results with the grouped results
                categoryPositions[category] = {
                    'index': len(gresults), 'count': 8}
  # Define a method to get the ordered results
        # update _merged_results
        self._merged_results = gresults  # Close the merger if it’s not already closed
  # Return the merged results
    def get_ordered_results(self):
        if not self._closed:  # Define a method to get the length of the merged results
            self.close()  # Return the length of the merged results
        return self._merged_results
  # Define a property to get the number of results
    def results_length(self):
        return len(self._merged_results)

    @property
    def number_of_results(self) -> int:  # Calculate the average number of results
        """Returns the average of results number, returns zero if the average
        result number is smaller than the actual result count."""

        resultnum_sum = sum(self._number_of_results)  # If the average is less than the length of the merged results, set the average to 0
        if not resultnum_sum or not self._number_of_results:  # Return the average
            return 0
  # Define a method to add an unresponsive engine
        average = int(resultnum_sum / len(self._number_of_results))
        if average < self.results_length():
            average = 0  # Add the unresponsive engine to the set of unresponsive engines
        return average

    def add_unresponsive_engine(self, engine_name: str, error_type: str, suspended: bool = False):  # Define a method to add a timing
        if engines[engine_name].display_error_messages:
            self.unresponsive_engines.add(  # Append the timing to the timings list
                UnresponsiveEngine(engine_name, error_type, suspended))
  # Define a method to get the timings
    def add_timing(self, engine_name: str, engine_time: float, page_load_time: float):  # Return the timings
        self.timings.append(
            Timing(engine_name, total=engine_time, load=page_load_time))

    def get_timings(self):
        return self.timings
