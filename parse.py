from bs4 import BeautifulSoup
import re
import dateutil.parser as dparser

def parse_html(html):
    soup = BeautifulSoup(html, 'html5lib')
    recordings = [
        parse_link_element(link)
        for link in soup.find_all('a')
        if link.get('href') and link.get('href').endswith('mp3')
    ]

    return recordings

def parse_link_element(link):
    time_reg = r'\(([\d]*:)?([\d]*):([\d]*)\)'

    reading_elem = link.find_parent('li')
    if not reading_elem:
        reading_elem = link.previous_sibling

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

    file_length = (re.search(time_reg, full_title_text)
                   .group()
                   .replace('(', '')
                   .replace(')', ''))

    event = ' '.join(event_elem.stripped_strings)

    try:
        date = dparser.parse(event, fuzzy=True).isoformat()
    except ValueError as err:
        date = ''

    return {
        'title': title,
        'length': file_length,
        'link': link.get('href'),
        'event': event,
        'date': date
    }
