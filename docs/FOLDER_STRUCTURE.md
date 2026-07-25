
# Folder Structure

`todo/` contains the project checklist and the ordered implementation step files.
`todo/10-adaptation-parser/` contains the ordered step files for the Wikipedia adaptation feature.

```text
movie-adaptation-impact/
├── todo/
│   ├── todo.md
│   ├── 01-configure-dependencies/
│   │   └── 01-configure-dependencies.md
│   ├── 02-create-index-fixture/
│   │   └── 02-create-index-fixture.md
│   ├── 03-create-adaptation-fixture/
│   │   └── 03-create-adaptation-fixture.md
│   ├── 04-implement-title-normalization/
│   │   └── 04-implement-title-normalization.md
│   ├── 05-test-title-normalization/
│   │   └── 05-test-title-normalization.md
│   ├── 06-define-wikipedia-sources/
│   │   └── 06-define-wikipedia-sources.md
│   ├── 07-implement-index-parsing/
│   │   └── 07-implement-index-parsing.md
│   ├── 08-test-index-parsing/
│   │   └── 08-test-index-parsing.md
│   ├── 09-organize-wikipedia-collector-modules/
│   │   └── 09-organize-wikipedia-collector-modules.md
│   ├── 10-adaptation-parser/
│   │   ├── 10-adaptation-parser.md
│   │   └── substeps/
│   │       ├── 10a-adaptation-parser-contract.md
│   │       ├── 10b-adaptation-input-tests.md
│   │       ├── 10c-adaptation-table-tests/
│   │       │   ├── 10c-adaptation-table-tests.md
│   │       │   └── substeps/
│   │       │       ├── 10c-01-test-module-setup.md
│   │       │       ├── 10c-02-exact-required-headers.md
│   │       │       ├── 10c-03-header-text-normalization.md
│   │       │       ├── 10c-04-case-sensitive-headers.md
│   │       │       ├── 10c-05-split-header-rows.md
│   │       │       ├── 10c-06-reversed-column-order.md
│   │       │       ├── 10c-07-unrelated-columns.md
│   │       │       ├── 10c-08-unrelated-table.md
│   │       │       ├── 10c-09-multiple-valid-tables.md
│   │       │       ├── 10c-10-changed-header-table.md
│   │       │       ├── 10c-11-missing-required-header.md
│   │       │       ├── 10c-12-no-recognizable-table.md
│   │       │       └── 10c-13-nested-table.md
│   │       ├── 10d-adaptation-row-tests.md
│   │       ├── 10e-adaptation-title-tests.md
│   │       ├── 10f-adaptation-rowspan-tests.md
│   │       ├── 10g-adaptation-same-as-above-tests.md
│   │       ├── 10h-adaptation-output-tests.md
│   │       └── 10i-adaptation-red-phase-verification.md
│   ├── 11-adaptation-parser-implementation/
│   │   └── 11-adaptation-parser-implementation.md
│   ├── 12-record-finalization/
│   │   └── 12-record-finalization.md
│   ├── 13-record-finalization-tests/
│   │   └── 13-record-finalization-tests.md
│   ├── 14-http-collection/
│   │   └── 14-http-collection.md
│   ├── 15-http-failure-tests/
│   │   └── 15-http-failure-tests.md
│   ├── 16-atomic-csv-output/
│   │   └── 16-atomic-csv-output.md
│   ├── 17-csv-output-tests/
│   │   └── 17-csv-output-tests.md
│   ├── 18-collection-statistics/
│   │   └── 18-collection-statistics.md
│   ├── 19-command-line-entry-point/
│   │   └── 19-command-line-entry-point.md
│   ├── 20-offline-verification/
│   │   └── 20-offline-verification.md
│   └── 21-controlled-live-verification/
│       └── 21-controlled-live-verification.md
│
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
