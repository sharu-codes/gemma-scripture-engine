import pandas as pd

files = ["gita.csv", "quran.csv", "ggs.csv", "bible.csv"]
combined = pd.concat(
    [pd.read_csv(f"data/processed/{f}", encoding="utf-8") for f in files],
    ignore_index=True
)
combined.to_csv("data/processed/all_scriptures.csv", index=False, encoding="utf-8-sig")

print(combined.shape)
print(combined["tradition"].value_counts())
print(combined.sample(5))