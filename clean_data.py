import pandas as pd

# ---- GITA ----
gita = pd.read_csv('data/processed/gita.csv')
gita['chapter'] = gita['reference'].astype(str).str.split('.').str[0]
gita['verse'] = gita['reference'].astype(str).str.split('.').str[1]
gita['book'] = ''

# ---- QURAN ----
quran = pd.read_csv('data/processed/quran.csv')
quran['chapter'] = quran['reference'].str.split(':').str[0]
quran['verse'] = quran['reference'].str.split(':').str[1]
quran['book'] = ''

# ---- GGS ----
ggs = pd.read_csv('data/processed/ggs.csv')
ggs['chapter'] = ggs['reference'].str.extract(r'Ang (\d+)')
ggs['verse'] = ggs['reference'].str.extract(r'Line (\d+)')
ggs['book'] = ''

# ---- BIBLE ----
bible = pd.read_csv('data/processed/bible.csv')
bible['book'] = bible['reference'].str.rsplit(' ', n=1).str[0]
rest = bible['reference'].str.rsplit(' ', n=1).str[1]
bible['chapter'] = rest.str.split(':').str[0]
bible['verse'] = rest.str.split(':').str[1]

# ---- Quick check: print 3 rows from each ----
for name, df in [('gita', gita), ('quran', quran), ('ggs', ggs), ('bible', bible)]:
    print(f"\n📄 {name}")
    print(df[['reference', 'book', 'chapter', 'verse']].head(3))
    print("Any missing chapter/verse?:", df[['chapter','verse']].isnull().sum().to_dict())


# ---- Create unique IDs ----
gita['id'] = 'GITA_' + gita['chapter'].astype(str) + '_' + gita['verse'].astype(str)
quran['id'] = 'QURAN_' + quran['chapter'].astype(str) + '_' + quran['verse'].astype(str)
ggs['id'] = 'GGS_' + ggs['chapter'].astype(str) + '_' + ggs['verse'].astype(str)
bible['id'] = 'BIBLE_' + bible['book'].str.replace(' ', '') + '_' + bible['chapter'].astype(str) + '_' + bible['verse'].astype(str)

# ---- Check: are IDs unique within each file? ----
for name, df in [('gita', gita), ('quran', quran), ('ggs', ggs), ('bible', bible)]:
    total = len(df)
    unique = df['id'].nunique()
    print(f"{name}: total rows = {total}, unique ids = {unique}, duplicates = {total - unique}")
    if total != unique:
        print("  ⚠️ Sample duplicate IDs:")
        print(df[df.duplicated('id', keep=False)]['id'].value_counts().head(5))

# ---- Inspect actual duplicate content ----
print("\n🔍 GITA duplicate example (GITA_1_1):")
print(gita[gita['id'] == 'GITA_1_1'][['id', 'original_text', 'translation']])

print("\n🔍 GGS duplicate example (GGS_51_17):")
print(ggs[ggs['id'] == 'GGS_51_17'][['id', 'original_text', 'translation']])

# ---- Make IDs unique by adding a suffix when repeated ----
def make_unique_ids(df):
    df['_dup_count'] = df.groupby('id').cumcount()  # 0,1,2... for repeats
    suffix_map = {0:'', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    df['id'] = df.apply(
        lambda row: row['id'] + suffix_map.get(row['_dup_count'], f"_{row['_dup_count']}"),
        axis=1
    )
    df.drop(columns=['_dup_count'], inplace=True)
    return df

gita = make_unique_ids(gita)
quran = make_unique_ids(quran)
ggs = make_unique_ids(ggs)
bible = make_unique_ids(bible)

# ---- Final check: confirm zero duplicates now ----
for name, df in [('gita', gita), ('quran', quran), ('ggs', ggs), ('bible', bible)]:
    total = len(df)
    unique = df['id'].nunique()
    print(f"{name}: total = {total}, unique ids = {unique}, duplicates = {total - unique}")

print("\nSample GITA ids after fix:")
print(gita[gita['id'].str.startswith('GITA_1_1')][['id']])

# ---- Encoding check ----
print("\n🔍 Quran original_text sample (should show Arabic script):")
print(quran['original_text'].head(3).tolist())

print("\n🔍 GGS original_text sample (should show Gurmukhi script):")
print(ggs['original_text'].head(3).tolist())

# ---- Check for corruption markers ----
def check_corruption(df, name):
    bad = df['original_text'].astype(str).str.contains(' ', na=False).sum()
    print(f"{name}: rows with corrupted ( ) characters = {bad}")

check_corruption(quran, 'quran')
check_corruption(ggs, 'ggs')

# ---- Add missing columns and finalize schema ----
def finalize_schema(df, source_name):
    df['source'] = source_name
    df['commentary'] = ''  # empty for now, can be filled later if you find commentary data
    final_cols = ['id', 'source', 'chapter', 'verse', 'original_text', 'translation', 'commentary']
    return df[final_cols]

gita_final = finalize_schema(gita, 'Gita')
quran_final = finalize_schema(quran, 'Quran')
ggs_final = finalize_schema(ggs, 'Guru Granth Sahib')
bible_final = finalize_schema(bible, 'Bible')

# ---- Check final structure ----
for name, df in [('gita', gita_final), ('quran', quran_final), ('ggs', ggs_final), ('bible', bible_final)]:
    print(f"\n📄 {name}_final")
    print(df.columns.tolist())
    print(df.head(2))

# ---- Fix Bible's missing original_text ----
bible_final['original_text'] = bible_final['translation']

# ---- Merge all 4 into one dataset ----
all_scriptures = pd.concat([gita_final, quran_final, ggs_final, bible_final], ignore_index=True)

print("\n📊 Final merged dataset:")
print("Total rows:", len(all_scriptures))
print("Rows per source:")
print(all_scriptures['source'].value_counts())

# ---- Final sanity checks before saving ----
print("\nDuplicate IDs in merged file:", all_scriptures['id'].duplicated().sum())
print("Missing values per column:")
print(all_scriptures.isnull().sum())

# ---- Save the final clean file ----
all_scriptures.to_csv('data/processed/all_scriptures_clean.csv', index=False, encoding='utf-8-sig')
print("\n✅ Saved: data/processed/all_scriptures_clean.csv")