import os
import requests
from bs4 import BeautifulSoup
import datetime
import json

# this script gets the word of the day
url = 'https://www.dictionary.com/e/word-of-the-day/'

# get word of the day
def get_word_of_the_day(soup):
    word = soup.find('h1', class_="js-fit-text").text
    return word


# get pronunciation
def get_pronunciation(soup):
    pronunciation = soup.find('span',
                              class_="otd-item-headword__pronunciation__text").text
    # remove brackets and empty space
    pronunciation = pronunciation.replace('[', '').replace(']', '').replace(' ', '').replace('\n', '')
    return pronunciation


# get part of speach
def get_part_of_speach(soup):
    part_of_speach = soup.find('div', class_="otd-item-headword__pos-blocks").find('span', class_="italic").text.replace('\n', '').replace(' ', '')
    return part_of_speach

# get definition
def get_definition(soup):
    definition = soup.find('div', class_="otd-item-headword__pos-blocks").text

    definition = definition.split('\n', 1)[1].replace(get_part_of_speach(soup), '').replace('\n', '')

    # find the first non blank space and remove everything before it
    for i in range(0, len(definition)):
        if definition[i] != ' ':
            definition = definition[i:]
            break

    return definition

if __name__ == '__main__':
    raw = requests.get(url)
    soup = BeautifulSoup(raw.content, 'html.parser')

    print(get_word_of_the_day(soup))
    print(get_pronunciation(soup))
    print(get_part_of_speach(soup))
    print(get_definition(soup), end='\n')

    wotd_json = {
        "word": get_word_of_the_day(soup),
        "pronunciation": get_pronunciation(soup),
        "part_of_speach": get_part_of_speach(soup),
        "definition": get_definition(soup)
    }
    print(wotd_json, end='\n')

    date = datetime.datetime.now().strftime("%Y-%m-%d") # get the current date

    # make a dir for our data of the day
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data', date)
    os.makedirs(data_dir, exist_ok=True)
    os.chdir(data_dir)

    # save the json
    with open('word_of_the_day.json', 'w') as f:
        json.dump(wotd_json, f, indent=4)
    print(f"Saved word of the day to {os.path.join(data_dir, 'word_of_the_day.json')}")