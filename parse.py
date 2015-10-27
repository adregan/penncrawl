from bs4 import BeautifulSoup
import re

def parse_html(html):
    soup = BeautifulSoup(html, 'html5lib')
    recordings = [
        parse_link_element(link)
        for link in soup.find_all('a')
        if link.get('href') and link.get('href').endswith('mp3')
    ]

    print(recordings)

def parse_link_element(link):
    time_reg = r'\(([\d]*:)?([\d]*):([\d]*)\)'

    full_title_text = ' '.join([
        string
        for string in (
            link.find_previous('img', src='/images/play.gif')
            .find_previous()
            .find_previous()
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

    return {
        'title': title,
        'length': file_length,
        'link': link.get('href'),
        'event': event 
    }
