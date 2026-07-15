# 📖 Gemma Scripture Engine

A RAG-powered spiritual Q&A assistant that answers questions with **cited verses** from the Bhagavad Gita, Quran, Guru Granth Sahib, and Bible — built with Gemma 2B-IT, FAISS, and Gradio.

---

## 🔗 Links

- 👤 **GitHub:** [github.com/YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- 📓 **Kaggle Notebook:** [Open on Kaggle](https://www.kaggle.com/YOUR_USERNAME/YOUR_NOTEBOOK)

---

## 🚀 Run It Yourself (Kaggle)

The easiest way to run this project is directly on Kaggle — no setup required, free GPU included.

### Steps

1. Open the Kaggle notebook link above
2. Click **"Copy & Edit"** (top right button)
3. Make sure GPU is enabled: **Settings → Accelerator → GPU T4 x2**
4. Attach the dataset: in the right panel under **Input**, add `sharucodes/all-scriptures-clean`
5. Attach the model: add `google/gemma/transformers/2b-it` from the **Models** tab
6. Click **"Run All"** and wait for the Gradio link to appear at the bottom

> ⚠️ The notebook uses `demo.launch(share=True, prevent_thread_lock=True)` — Gradio will print a public link valid for 72 hours.

---

## 🧠 How It Works

```
User Query
    ↓
SentenceTransformer (all-MiniLM-L6-v2)   ← encodes query
    ↓
FAISS Index                                ← retrieves top-k relevant verses
    ↓
Gemma 2B-IT                               ← generates cited answer from verses only
    ↓
Hallucination Check                        ← strips any IDs not in retrieved set
    ↓
Gradio UI                                  ← displays answer with source citations
```

### Two Modes

| Mode | Description |
|------|-------------|
| **Single Scripture Answer** | Retrieves top 5 verses globally, answers with citations |
| **Cross-Tradition Comparison** | Retrieves 2 verses per scripture, compares all 4 traditions |

---

## 🗂️ Project Structure

```
├── app.py                    # HuggingFace Spaces deployment (see note below)
├── requirements.txt          # Python dependencies
├── all_scriptures_clean.csv  # Verse dataset (Gita, Quran, GGS, Bible)
└── hackathon.ipynb           # Original Kaggle notebook
```

---

## 📦 Dependencies

```
torch
transformers
sentence-transformers
faiss-cpu
gradio
pandas
langdetect
huggingface_hub
spaces
```

---

## ⚠️ Deployment Status

**HuggingFace Spaces deployment is currently failing.**

The app is built for ZeroGPU (`@spaces.GPU`) but the ZeroGPU worker consistently fails to allocate a physical GPU at inference time:

```
RuntimeError: No CUDA GPUs are available
POST .../release?fail=true   ← GPU allocation fails at worker level
```

This appears to be a ZeroGPU quota/infrastructure issue — the code itself is correct. Possible fixes being explored:

- Switching to a static **T4 Small** paid GPU tier and removing `@spaces.GPU`
- Waiting for ZeroGPU quota availability

**In the meantime, please use the Kaggle notebook (link above) — it works fully with a free T4 GPU.**

---

## 📊 Dataset

**All Scriptures Clean** by [@sharucodes](https://www.kaggle.com/sharucodes) on Kaggle
Contains translated verses from: Bhagavad Gita · Quran · Guru Granth Sahib · Bible

---

## 🏆 Built For

This project was built as part of a Kaggle Hackathon. The goal was to build a grounded, citation-safe LLM pipeline over religious texts — with zero hallucinated verse IDs.
