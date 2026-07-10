import pandas as pd

df = pd.read_csv("data/raw/bible_databases/formats/csv/KJV.csv", encoding="utf-8")

bible = pd.DataFrame({
    "tradition": "Bible",
    "reference": df["Book"].astype(str) + " " + df["Chapter"].astype(str) + ":" + df["Verse"].astype(str),
    "original_text": None,
    "translation": df["Text"]
})
bible.to_csv("data/processed/bible.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(bible)} verses to data/processed/bible.csv")
print(bible.head())