import json
import requests
from transliterate import translit


def get_google_sites(comp_name, triggers, page_index):
    """Function gets company name as an argument and returns response object
    from google search custom API.

    :param comp_name: company name query to search
    :type comp_name: str
    :param triggers: words sequence which should be existed in the response
    :type triggers: list
    :param page_index: parameter where we ne to start current search session
    :type page_index: int
    :return: response_json (dict)
    """
    api_key = r''
    search_engine_id = r''
    # Enter your serial data here

    search_url = r'https://www.googleapis.com/customsearch/v1?' \
        + r'key=' + api_key \
        + r'&cx=' + search_engine_id \
        + r'&q=' + '+OR+'.join(triggers) \
        + r'&hq=' + comp_name \
        + r'&start=' + str(page_index)

    response = requests.get(
        search_url,
        verify=None
    )
    response_json = json.loads(response.text)

    return response_json


def get_site_info(site_object):
    return '{site_title}, link: {site_link}'.format(
        site_title=site_object['title'],
        site_link=site_object['link']
    )


if __name__ == '__main__':
    WORDS: list = []

    company_name = translit(
        input('Enter your text query here: '),
        'ru',
        reversed=True
    )
    # Text query to search

    found_sites_list = []

    all_pages_counter = 0

    for start_index in range(1, 100, 10):
        google_sites = get_google_sites(
            company_name,
            WORDS,
            start_index
        )

        try:
            found_sites_list = google_sites['items']
        except KeyError as err:
            if start_index == 1 and 'error' in found_sites_list:
                print(
                    json.dumps(
                        google_sites,
                        ensure_ascii=False,
                        indent=4
                    )
                )
            else:
                break
        else:
            all_pages_counter += len(found_sites_list)
            for found_site in found_sites_list:
                print(
                    get_site_info(found_site)
                )

    print('All sites found: ' + str(all_pages_counter))
