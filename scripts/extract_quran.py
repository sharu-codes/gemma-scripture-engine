import pandas as pd

df = pd.read_csv("data/raw/quran-dataset/quran_dataset.csv", encoding="utf-8")
df = df.drop_duplicates(subset=["surah_no", "ayah_no_surah"])

quran = pd.DataFrame({
    "tradition": "Quran",
    "reference": df["surah_no"].astype(str) + ":" + df["ayah_no_surah"].astype(str),
    "original_text": df["ayah_ar"],
    "translation": df["ayah_en"]
})

quran.to_csv("data/processed/quran.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(quran)} verses to data/processed/quran.csv")
print(quran.head())