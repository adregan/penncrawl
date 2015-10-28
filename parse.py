from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
import dateutil.parser as dparser
from error import error_writer

def parse_html(html, link_to_page):
    soup = BeautifulSoup(html, 'html5lib')
    recordings = [
        parse_link_element(link, link_to_page)
        for link in soup.find_all('a')
        if link.get('href') and link.get('href').endswith('mp3')
    ]

    return recordings

def parse_link_element(link, link_to_page):
    time_reg = r'\(([\d]*:)?([\d]*):([\d]*)\)'

    reading_elem = link.find_parent('li')
    if not reading_elem:
        try: 
            reading_elem = [
                el
                for el in link.previous_siblings
                if isinstance(el, NavigableString) and el.strip()
            ][0]
        except IndexError as err:
            # Nothing more we can do
            error = {
                'error': 'Couldn\'t find the reading title', 
                'page': '{}'.format(link_to_page),
                'link': '{}'.format(link.get('href'))
            }
            error_writer(error)
            reading_elem = ''

    event_elem = link.find_previous(re.compile("^h"))

    try:
        full_title_text = ' '.join([
            string
            for string in reading_elem.stripped_strings
            if string.lower() != 'mp3'
        ])
    except AttributeError as err:
        full_title_text = reading_elem

    title = re.split(time_reg, full_title_text)[0].strip()

    try:
        file_length = (re.search(time_reg, full_title_text)
                       .group()
                       .replace('(', '')
                       .replace(')', ''))
    except AttributeError as err:
        error = {
            'error': 'Couldn\'t parse the recording length', 
            'page': '{}'.format(link_to_page),
            'link': '{}'.format(link.get('href'))
        }
        file_length = ''

    event = ' '.join(event_elem.stripped_strings)

    try:
        date = dparser.parse(event, fuzzy=True).isoformat()
    except ValueError as err:
        error = {
            'error': 'Couldn\'t parse the event date', 
            'page': '{}'.format(link_to_page),
            'link': '{}'.format(link.get('href'))
        }
        date = ''

    return {
        'title': title,
        'length': file_length,
        'link': link.get('href'),
        'event': event,
        'date': date
    }
