import os
import requests
from lxml import html as lxml_html


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/60.0.3112.90 Safari/537.36'
HEADERS    = {'user-agent': USER_AGENT}
BASE_URL   = 'http://www.ldoceonline.com/dictionary/'
WORD       = 'example'


def fetch(prompt="Enter your word: "):
    input_word = input(prompt)
    if not isinstance(input_word, str) or len(input_word) == 0:
        return fetch(prompt="Please enter a word-like word: ")

    global WORD
    WORD = input_word
    fetch_url = BASE_URL + WORD
    resp = requests.get(fetch_url, headers=HEADERS)
    page = lxml_html.document_fromstring(resp.content)

    try:
        page.find_class('brefile')[0]
    except IndexError:
        return fetch(prompt="Not found, please try another word: ")

    return page


def parse():
    p = fetch()
    brefile = p.find_class('brefile')[0]
    amefile = p.find_class('amefile')[0]
    pronfile = p.find_class('PRON')[0]

    try:
        ame_pron = p.find_class("AMEVARPRON")[0].text_content()
    except IndexError:
        ame_pron = None

    pron = pronfile.text
    if ame_pron is not None:
        pron = pron + ame_pron
    bre_mp3 = brefile.get('data-src-mp3')
    ame_mp3 = amefile.get('data-src-mp3')

    result = '| ' + WORD + ' | ' + \
             '/' + pron + '/ | ' + \
             '[' + \
            u'\U0001F1EC\U0001F1E7' + \
             '](' + bre_mp3 + ') [' + \
            u'\U0001F1FA\U0001F1F8' + \
             '](' + ame_mp3 + ') |'

    return result


def parse_and_copy():
    r = parse()
    print('Result: ', r)
    try:
        os.system("echo '%s' | tr -d '\n' | pbcopy" % r)
        print('Result has been copied to pasteboard!')
    except:
        pass
    return parse_and_copy()


if __name__ == '__main__':
    parse_and_copy()

