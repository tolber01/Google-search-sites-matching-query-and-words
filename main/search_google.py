import json
import requests
from transliterate import translit


def get_google_sites(comp_name, page_index):
    """Function gets company name as an argument and returns response object
    from google search custom API.

    :param comp_name: company name query to search
    :type comp_name: str
    :param page_index: parameter where we ne to start current search session
    :type page_index: int
    :return: response_json (dict)
    """
    api_key = r''
    search_engine_id = r''
    # Enter your serial data here

    friends_url = r'https://www.googleapis.com/customsearch/v1?' \
        + r'key=' + api_key \
        + r'&cx=' + search_engine_id \
        + r'&q=' + comp_name \
        + r'&start=' + str(page_index)

    response = requests.get(
        friends_url,
        verify=None
    )
    response_json = json.loads(response.text)

    return response_json


if __name__ == '__main__':
    WORDS: list = []

    company_name = translit(
        'query',
        'ru',
        reversed=True
    )
    # Text query to search

    found_sites_list = []

    for start_index in range(1, 100, 10):
        google_sites = get_google_sites(
            company_name,
            start_index
        )
        print(google_sites)

        try:
            found_sites_list += google_sites['items']
        except KeyError:
            break

    print('All sites found:', len(found_sites_list))

    relevant_pages_counter = 0

    for found_site in found_sites_list:
        if any(
            keyword.lower() in found_site['snippet'].lower() for keyword in WORDS
        ) or any(
            keyword.lower() in keyword in found_site['title'].lower() for keyword in WORDS
        ):
            result_string = found_site['title'] \
                            + ', link: ' \
                            + found_site['link']
            print(result_string)

            relevant_pages_counter += 1

    print('Total need sites:', relevant_pages_counter)
