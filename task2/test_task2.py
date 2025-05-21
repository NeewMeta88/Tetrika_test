import os
import csv
import tempfile
from task2 import count_by_first_letter, save_counts_to_csv, RUS_ALPHABET


def test_count_by_first_letter_basic():
    sample_titles = [
        "Акула",
        "Антилопа",
        "Бобр",
        "Барсук",
        "Воробей",
        "Ёж",
        "енот",
        "Ягуар"
    ]
    counts = count_by_first_letter(sample_titles)
    assert counts["А"] == 2
    assert counts["Б"] == 2
    assert counts["В"] == 1
    assert counts["Ё"] == 1
    assert counts["Е"] == 1
    assert counts["Я"] == 1
    assert counts["Ж"] == 0
    assert counts["Ъ"] == 0
    assert set(counts.keys()) == set(RUS_ALPHABET)


def test_save_counts_to_csv_output():
    fd, temp_path = tempfile.mkstemp(text=True)
    os.close(fd)
    try:
        sample_counts = {letter: 0 for letter in RUS_ALPHABET}
        sample_counts.update({"А": 3, "Б": 1, "Ё": 2, "Я": 5})
        save_counts_to_csv(sample_counts, filename=temp_path)
        with open(temp_path, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
        assert len(lines) == len(RUS_ALPHABET)
        assert lines[0][0] == "А"
        assert lines[-1][0] == "Я"
        for letter, count in [("А", "3"), ("Б", "1"), ("Ё", "2"), ("В", "0"), ("Ъ", "0"), ("Я", "5")]:
            row = next((r for r in lines if r[0] == letter), None)
            assert row is not None, f"Не найдена строка для буквы {letter}"
            assert row[1] == str(count), f"Неверное количество для буквы {letter}"
    finally:
        os.remove(temp_path)
