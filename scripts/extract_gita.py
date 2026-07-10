import json
import os
import pandas as pd

slok_dir = "data/raw/bhagavad-gita/slok"
rows = []

for filename in os.listdir(slok_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(slok_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        chapter = data.get("chapter")
        verse = data.get("verse")
        original = data.get("slok")
        translation = data.get("prabhu", {}).get("et")

        if translation:
            rows.append({
                "tradition": "Gita",
                "reference": f"{chapter}.{verse}",
                "original_text": original,
                "translation": translation
            })

df = pd.DataFrame(rows)
df = df.sort_values(by="reference", key=lambda col: col.map(lambda x: tuple(map(int, x.split(".")))))
df.to_csv("data/processed/gita.csv", index=False, encoding="utf-8-sig")

print(f"Saved {len(df)} verses to data/processed/gita.csv")
print(df.head())