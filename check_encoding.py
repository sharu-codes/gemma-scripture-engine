import json

with open("data/raw/quran-dataset/quran_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data[0]["ayah_ar"])