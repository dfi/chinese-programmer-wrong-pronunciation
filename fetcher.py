import string

import os
import requests
from lxml import html as lxml_html


USER_AGENT      = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/60.0.3112.113 Safari/537.36'
HEADERS         = {'user-agent': USER_AGENT}
BASE_URL        = 'http://www.ldoceonline.com/dictionary/'
WORD            = 'example'
FILE_NAME       = 'README.md'
MP3_LINK_PREFIX = 'http://www.ldoceonline.com'


def get_input(prompt="Enter your word (or a space to exit): "):
    ipt = input(prompt)
    if ipt == ' ':
        print('You ended the fetch.')
        return None
    if len(ipt) == 0 or not all(c in string.ascii_letters for c in ipt):
        return get_input(prompt="Please enter a word (or a space to exit): ")
    return ipt


def fetch(word):
    global WORD
    WORD = word
    fetch_url = BASE_URL + WORD
    resp = requests.get(fetch_url, headers=HEADERS)
    page = lxml_html.document_fromstring(resp.text)

    try:
        page.find_class('brefile')[0]
    except IndexError:
        return -1

    return page


def parse(page):
    p = page
    brefile = p.find_class('brefile')[0]
    amefile = p.find_class('amefile')[0]
    pronfile = p.find_class('PronCodes')[0]
    pron = pronfile.text_content()
    bre_mp3 = brefile.get('data-src-mp3')
    if not MP3_LINK_PREFIX in bre_mp3:
        bre_mp3 = MP3_LINK_PREFIX + bre_mp3
    ame_mp3 = amefile.get('data-src-mp3')
    if not MP3_LINK_PREFIX in ame_mp3:
        ame_mp3 = MP3_LINK_PREFIX + ame_mp3

    result = '| ' + WORD + ' |' + pron + ' | ' + \
             '[' + u'\U0001F1EC\U0001F1E7' + '](' + bre_mp3 + ') [' + \
             u'\U0001F1FA\U0001F1F8' + '](' + ame_mp3 + ') |'

    return result


def copy_to_pasteboard(s):
    if not isinstance(s, str):
        print('Encountered strange characters!')
        return
    try:
        os.system("echo '%s' | tr -d '\n' | pbcopy" % s)
        print('Result has been copied to pasteboard!')
    except:
        print('Copy failed!')


def add_word(word, file):
    with open(file) as o:
        r = o.read()
        l = r.split('\n')
        i = l.index('')
        for word_line in l[2:i]:
            if word[:(word[1:].index('|'))].strip('| ').lower() == \
                    word_line[:(word_line[1:].index('|'))].strip('| ').lower():
                print('Word:\n{w}\nalready in {f}!'.format(w=word, f=FILE_NAME))
                print('Please add another word.')
                return
        l.insert(2, word)
        l[2:i] = sorted(l[2:i], key=lambda x: x.lower())
        s = '\n'.join(l)
        with open(file, 'w') as w:
            w.write(s)
            print('Finished!')


def start_over():
    ipt = get_input()
    if ipt == None:
        return
    fetch_result = fetch(ipt)
    if fetch_result == -1:
        print("Not found, please try another word.")
        return start_over()
    word = parse(fetch_result)
    print('Fetch result:')
    print(word)
    print('Trying to add your word to', FILE_NAME, '...')
    add_word(word, FILE_NAME)


if __name__ == '__main__':
    start_over()
