from requests import get
from bs4 import BeautifulSoup
from re import compile
from sys import argv

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
             'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']


def console():
    print("Hello, you're welcome to the translator. Translator supports:")
    for i, language in enumerate(languages, 1):
        print(f'{i}. {language}')

    while True:
        source_language = int(input('Type the number of your source language: '))
        if source_language not in range(1, 14):
            print('Wrong number!')
        else:
            break
    source_language = languages[source_language - 1]

    while True:
        destination_language = int(input("Type the number of language you want to translate to"
                                         " or '0' to translate to all languages: "))
        if destination_language not in range(14):
            print('Wrong number!')
        else:
            break
    if destination_language != 0:
        destination_language = languages[destination_language - 1]

    word_to_translate = input('Type the word you want to translate: ').lower()

    file = open(f'{word_to_translate}.txt', 'w', encoding='utf-8')

    if destination_language == 0:
        for language in languages:
            if language != source_language:
                translate(source_language, language, word_to_translate, file)
    else:
        translate(source_language, destination_language, word_to_translate, file)

    file.close()


def arguments():
    source_language = argv[1].capitalize()
    destination_language = argv[2].capitalize()
    if destination_language != 'All':
        if source_language not in languages:
            print(f"Sorry, the program doesn't support {source_language}")
            exit()
        if destination_language not in languages:
            print(f"Sorry, the program doesn't support {destination_language}")
            exit()
    word_to_translate = argv[3].lower()
    file = open(f'{word_to_translate}.txt', 'w', encoding='utf-8')

    if destination_language == 'All':
        for language in languages:
            if language != source_language:
                translate(source_language, language, word_to_translate, file)
    else:
        translate(source_language, destination_language, word_to_translate, file)

    file.close()


def translate(source_language, destination_language, word_to_translate, file):
    request = get(f'https://context.reverso.net/translation/{source_language.lower()}-'
                  f'{destination_language.lower()}/{word_to_translate}', headers={'User-Agent': 'Mozilla/5.0'})
    if request:
        html_code = request.content
        soup = BeautifulSoup(html_code, 'html.parser')

        div_words = soup.find('div', id='translations-content')
        if div_words is None:
            print(f'Sorry, unable to find {word_to_translate} or this language pair is not supported')
            exit()
        words = div_words.find_all('a', limit=5)
        for i, word in enumerate(words):
            words[i] = word.get_text().strip()

        source_examples = soup.find_all('div', {'class': 'src ltr'}, limit=5)
        regex = compile(r"^trg [rtl]{3}")
        destination_examples = soup.find_all('div', {'class': regex}, limit=5)
        for i, example in enumerate(source_examples):
            source_examples[i] = example.get_text().strip()
        for i, example in enumerate(destination_examples):
            destination_examples[i] = example.get_text().strip()

        print(f'{destination_language} Translations:')
        file.write(f'{destination_language} Translations:\n')
        for i, word in enumerate(words):
            print(words[i])
            file.write(f'{words[i]}')
        print(f'\n{destination_language} Examples:')
        file.write(f'\n{destination_language} Examples:\n')
        for i, example in enumerate(source_examples):
            print(source_examples[i])
            file.write(f'{source_examples[i]}\n')
            print(f'{destination_examples[i]}\n')
            file.write(f'{destination_examples[i]}\n\n')

    elif request.status_code == 404:
        print(f'Not found error. Unable to find word {word_to_translate} or server problem')
    else:
        print('Something wrong with your internet connection')


if len(argv) == 4:
    arguments()
else:
    console()
