import json
import hashlib
import os
from datetime import datetime


def create_log_file(path):
    def decorator(function):
        def new_function(*args, **kwargs):
            start = datetime.now()
            result = function(*args, **kwargs)
            log = f"Время вызова: {start.strftime('%d/%m/%Y %H:%M:%S')} Функция: {function.__name__} " \
                  f"Аргументы: {args} {kwargs} Результат: {result}"
            write_mode = 'w' if os.path.isfile(path) else 'a'
            with open(path, write_mode, encoding='utf-8') as my_file:
                my_file.write(log + '\n')
            return result
        return new_function
    return decorator


class WikiLinkIter:
    wiki_link = 'https://en.wikipedia.org/wiki/'

    def __init__(self, countries_data):
        self.countries = countries_data

    def __iter__(self):
        return self

    def __next__(self):
        country = next(self.countries)
        return f"{country['name']['common']} - {self.wiki_link}{country['name']['common'].replace(' ', '_')}"

    @create_log_file('log.txt')
    def download(self, path):
        with open(path, 'w', encoding='utf-8') as document:
            for wiki_link in self:
                document.write(wiki_link + '\n')


@create_log_file('log.txt')
def hash_iter(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            hash_object = hashlib.md5(line.encode()).hexdigest()
            yield hash_object


if __name__ == '__main__':
    with open('countries.json', encoding='utf-8') as f:
        json_data = json.load(f)

    wiki_links = WikiLinkIter(iter(json_data))
    wiki_links.download('wiki_countries_links.txt')
    hash_iter('wiki_countries_links.txt')
