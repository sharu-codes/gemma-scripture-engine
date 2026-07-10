import requests, time, pandas as pd

rows = []
for ang in range(1, 1431):
    r = requests.get(f"https://api.gurbaninow.com/v2/ang/{ang}").json()
    for item in r["page"]:
        line = item["line"]
        translation = line.get("translation", {}).get("english", {}).get("default")
        original = line.get("gurmukhi", {}).get("unicode")
        if translation:
            rows.append({
                "tradition": "Guru Granth Sahib",
                "reference": f"Ang {ang}, Line {line.get('lineno')}",
                "original_text": original,
                "translation": translation
            })
    if ang % 100 == 0:
        print(f"...{ang}/1430")
    time.sleep(0.1)

df = pd.DataFrame(rows)
df.to_csv("data/processed/ggs.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(df)} lines to data/processed/ggs.csv")
print(df.head())