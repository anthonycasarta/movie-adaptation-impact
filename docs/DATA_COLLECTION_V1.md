# Data Collection (Version 1)

## Goal

Build the smallest possible dataset needed to answer the research question:

> **How much do movie adaptations increase book sales?**

Instead of relying on third-party datasets with unknown provenance, Version 1 will build a reproducible dataset directly from authoritative public sources.

Once this foundation is complete, additional datasets can be added incrementally.

---

# Version 1 Datasets

## Dataset 1 — Book-to-Movie Adaptations

### Purpose

Build a dataset linking books to their movie adaptations.

### Required Fields

* Book title
* Author
* Movie title
* Movie release date

### Sources

* Wikipedia
* Open Library API
* TMDb API

### Collection Workflow

```text
Wikipedia
        ↓
Extract adaptation pairs
        ↓
Open Library API
        ↓
Book metadata + ISBN
        ↓
TMDb API
        ↓
Movie metadata
        ↓
Master adaptation dataset
```

### Steps

#### Step 1 — Collect Adaptation Pairs

Extract book-to-movie adaptation pairs from Wikipedia.

Initial fields:

* Book title
* Movie title

Store the raw extraction in:

```text
data/raw/wikipedia/
```

---

#### Step 2 — Enrich Book Metadata

For each book collected from Wikipedia:

Retrieve metadata from Open Library.

Fields:

* Author
* ISBN-10
* ISBN-13
* Publication year
* Publisher

Store raw responses in:

```text
data/raw/openlibrary/
```

---

#### Step 3 — Enrich Movie Metadata

For each movie:

Retrieve metadata from TMDb.

Fields:

* Release date
* TMDb ID

Store raw responses in:

```text
data/raw/tmdb/
```

---

#### Step 4 — Build the Master Dataset

Merge all collected information into a single processed dataset.

Output:

```text
data/processed/adaptations.parquet
```

---

## Dataset 2 — New York Times Bestseller Data

### Purpose

Historical title-level book sales are generally not publicly available.

Version 1 will use New York Times bestseller rankings as a proxy for popularity.

This allows comparison of a book's popularity before and after its movie adaptation.

### Required Fields

* Published date
* Title
* Author
* Rank
* Weeks on list
* ISBN-13
* ISBN-10

### Source

New York Times Books API

### Steps

1. Create a New York Times Developer account.
2. Create an application.
3. Enable access to the Books API.
4. Copy your API key.
5. Create a local `.env` file.

```text
NYT_API_KEY=your_api_key_here
```

6. Add `.env` to `.gitignore`.

```gitignore
.env
```

Store downloaded data in:

```text
data/raw/bestseller/
```

---

# Folder Structure

```text
movie-adaptation-impact/

├── data/
│   ├── raw/
│   │   ├── wikipedia/
│   │   ├── openlibrary/
│   │   ├── tmdb/
│   │   └── bestseller/
│   ├── interim/
│   └── processed/
│
├── notebooks/
├── src/
├── docs/
├── README.md
└── pyproject.toml
```

---

# Collection Order

Complete the datasets in the following order.

## Step 1

Collect adaptation pairs from Wikipedia.

Output:

* Book title
* Movie title

---

## Step 2

Enrich each book using the Open Library API.

Retrieve:

* Author
* ISBN
* Publication year
* Publisher

---

## Step 3

Enrich each movie using the TMDb API.

Retrieve:

* Release date
* TMDb ID

---

## Step 4

Merge all collected data into:

```text
data/processed/adaptations.parquet
```

Verify every record contains:

* Book title
* Author
* ISBN (when available)
* Movie title
* Movie release date

---

## Step 5

Register for the New York Times Books API.

---

## Step 6

Download one year of bestseller data.

Start with:

* 2022

Do **not** download every available year yet.

The goal is to validate the pipeline before collecting additional years.

---

## Step 7

Join the adaptation dataset with the bestseller dataset.

Initially, match using:

* ISBN (preferred)
* Book title
* Author

---

## Step 8

Create the first analysis dataset.

Example:

| Book                    | Author      | Movie                   | Release Date | Bestseller Date | Rank |
| ----------------------- | ----------- | ----------------------- | ------------ | --------------- | ---- |
| Where the Crawdads Sing | Delia Owens | Where the Crawdads Sing | 2022-07-15   | 2022-07-10      | 4    |
| Where the Crawdads Sing | Delia Owens | Where the Crawdads Sing | 2022-07-15   | 2022-07-17      | 2    |

---

# First Analysis

Once the datasets are merged, answer the following questions:

* Did the book appear on the bestseller list before the movie?
* Did it appear after the movie?
* Did its rank improve?
* How many weeks did it remain on the list before the adaptation?
* How many weeks did it remain on the list after the adaptation?

At this stage, the project measures changes in **bestseller ranking**, not exact copies sold.

---

# Current Scope

**Included**

* Book-to-movie adaptations
* Book metadata
* Movie release dates
* Bestseller rankings

**Not Yet Included**

* Goodreads
* Rotten Tomatoes
* Additional TMDb metadata (budget, revenue, genres)
* Genre analysis
* Machine learning
* Exact book sales

These datasets and analyses will be added only after Version 1 is complete.

---

# Success Criteria

Version 1 is complete when:

* Book-to-movie adaptation pairs have been collected from Wikipedia.
* Book metadata has been enriched using Open Library.
* Movie metadata has been enriched using TMDb.
* A processed adaptation dataset has been created.
* One year of NYT bestseller data has been collected.
* The datasets have been successfully merged.
* A basic before-and-after analysis has been performed.
* Initial visualizations have been created.

Only after reaching these milestones should additional datasets be introduced.
