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

    full_title_text = ' '.join([
        string
        for string in (
            link.find_previous('img', src='/images/play.gif')
            .find_previous('a')
            .find_previous('li')
            .stripped_strings
        )
        if string.lower() != 'mp3'
    ])

    title = re.split(time_reg, full_title_text)[0].strip()

    file_length = (re.search(time_reg, full_title_text)
                   .group()
                   .replace('(', '')
                   .replace(')', ''))

    event = ' '.join(link.find_previous('h2').stripped_strings)

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
