import requests
import csv

RUS_ALPHABET = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К',
    'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц',
    'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'
]


def fetch_all_titles():
    titles = []
    session = requests.Session()
    API_URL = "https://ru.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmtype": "page",
        "cmnamespace": "0",
        "cmlimit": "500",
        "format": "json"
    }
    while True:
        response = session.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        for page in data["query"]["categorymembers"]:
            titles.append(page["title"])
        if "continue" in data:
            params["cmcontinue"] = data["continue"]["cmcontinue"]
        else:
            break
    return titles


def count_by_first_letter(titles):
    counts = {letter: 0 for letter in RUS_ALPHABET}
    for title in titles:
        if not title:
            continue
        first_char = title[0].upper()
        if first_char in counts:
            counts[first_char] += 1
        else:
            pass
    return counts


def save_counts_to_csv(counts, filename="beasts.csv"):
    with open(filename, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for letter in RUS_ALPHABET:
            writer.writerow([letter, counts.get(letter, 0)])


if __name__ == "__main__":
    all_titles = fetch_all_titles()
    letter_counts = count_by_first_letter(all_titles)
    save_counts_to_csv(letter_counts)
    print(f"Результаты сохранены в {len(RUS_ALPHABET)} строк в файл beasts.csv")
