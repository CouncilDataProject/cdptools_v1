from bs4 import BeautifulSoup as bs
from pprint import pprint
import Levenshtein
import datetime
import requests

def _get_parse_page(url):
    r = requests.get(url)
    return bs(r.content, 'html.parser')

def _collect_all(soup,
                tags=None,
                classes=None,
                store_by=None,
                label=False,
                label_by='text'):


    if tags is None and classes is None:
        raise ValueError('Provide a list of tags and/ or classes to find content by.')

    if label:
        found = dict()
    else:
        found = list()

    if tags is not None and classes is None:
        loop_with = tags
        find_with = 'tags'
    if tags is None and classes is not None:
        loop_with = classes
        find_with = 'classes'
    if tags is not None and classes is not None:
        combine = list()
        for t in tags:
            for c in classes:
                combine.append([t, c])

        loop_with = combine
        find_with = 'both'

    for find in loop_with:
        if find_with == 'tags':
            found_i = soup.find_all(find)
        elif find_with == 'classes':
            found_i = soup.find_all(class_=find)
        elif find_with == 'both':
            found_i = soup.find_all(find[0], class_=find[1])

        for item in found_i:
            if label:
                if store_by is None:
                    found[getattr(item, label_by)] = item
                else:
                    store = getattr(item, store_by)
                    if store is None:
                        store = item[store_by]
                    if store is None:
                        store = item

                    found[getattr(item, label_by)] = store
            else:
                if store_by is None:
                    found.append(item)
                else:
                    store = getattr(item, store_by)
                    if store is None:
                        store = item[store_by]
                    if store is None:
                        store = item

                    found.append(store)

    return found

def _compare_distance(a, b):
    if len(a) > len(b):
        divide_by = len(a)
    else:
        divide_by = len(b)

    return float(Levenshtein.distance(a, b)) / float(divide_by)

def _reduce_dict(d):
    distances = dict()

    for a in d:
        distances[a] = dict()
        for b in d:
            if a != b:
                dist = _compare_distance(a, b)
                distances[a][b] = dist

    pprint(distances)

    # for a_key, a_item in a.items():
    #     for b_key in b:


def get_all_video():
    base_url = 'http://www.seattlechannel.org/'
    landing = _get_parse_page(base_url + 'CityCouncil')
    committee_div_classes = ['col-md-6 col-xs-12 twoColLeft',
                            'col-md-6col-xs-12 twoColRight']
    committee_divs = _collect_all(landing, classes=committee_div_classes)

    committee_tags = ['a']

    remove_committee_labels = ['seattle']
    all_committees = dict()
    for c_div in committee_divs:
        committees_in_div = _collect_all(c_div,
                                        tags=committee_tags,
                                        store_by='href',
                                        label=True)

        full_copy = dict(committees_in_div)

        for committee, url in full_copy.items():
            split_committee = committee.lower().split(' ')
            for label in remove_committee_labels:
                split_committee = [word for word in split_committee if word != label.lower()]

            joined = ' '.join(split_committee)
            del committees_in_div[committee]

            if base_url not in url:
                url = base_url + url

            all_committees[joined.lower()] = url

    need_to_reduce = dict()
    for commit, url in all_committees.items():
        current_year = datetime.datetime.now().year
        years_active = ['2014', '2015', '2016', '2017', '2018', '2019']
        if any()

    _reduce_dict(all_committees)
