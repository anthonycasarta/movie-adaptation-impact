
# Folder Structure

```text
movie-adaptation-impact/
├── data/
│   ├── raw/
│   │   ├── wikipedia/
│   │   ├── openlibrary/
│   │   └── tmdb/
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   └── 02_data_validation.ipynb
│
├── src/
│   ├── __init__.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── wikipedia.py
│   │   ├── wikipedia_index.py
│   │   ├── openlibrary.py
│   │   └── tmdb.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── build_dataset.py
│   └── utils/
│       ├── __init__.py
│       └── text.py
│
├── tests/
│   ├── __init__.py
│   ├── test_text.py
│   └── test_wikipedia_index.py
│
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── DATA_COLLECTION_V1.md
│   ├── DATA_SOURCES.md
│   └── FOLDER_STRUCTURE.md
│
├── .env.example
├── .gitignore
├── README.md
└── pyproject.toml
```
