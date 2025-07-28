
# HR-Analytics-Project
=======

# HR Analytics Project

> **Author:** [ankit-kumarz](https://github.com/ankit-kumarz)

## Overview

HR Analytics is a smart job recommender tool for HRs and job seekers. It suggests the top matching jobs from a dataset based on a candidate's skills, using advanced NLP and machine learning techniques. There are two main modes:

- **Version 1:** Upload your resume (PDF, DOCX, or TXT) and the app extracts your skills automatically.
- **Version 2:** Manually enter your skills and get job recommendations instantly.

The job dataset was scraped from Glassdoor using Selenium and BeautifulSoup, containing ~1923 job postings. Matching is performed using n-grams, TF-IDF vectorization, and KNN for best-fit job suggestions. Both versions are deployed as Flask web apps with modern, user-friendly UIs.

---

## Features

- Upload resume and auto-extract skills (using pyresparser, spaCy, textract, pdfminer, etc.)
- Manual skills input option
- Top 10 job recommendations based on skill-job description similarity
- Modern, attractive web UI (HTML/CSS)
- Dataset scraping script included (see `glassdoor scrapping.ipynb`)
- Easy to run locally

---

## Demo

**Version 1:** Resume Upload
![Resume Upload UI](templates/model.html)

**Version 2:** Manual Skills Input
![Manual Skills UI](templates/new_model.html)

---

## File Structure

```
├── hr_1.py                  # Flask app for resume-based job matching
├── hr_2.py                  # Flask app for manual skills input
├── job_final.csv            # Scraped job dataset
├── glassdoor scrapping.ipynb# Notebook for scraping jobs from Glassdoor
├── skills_extractor.ipynb   # Standalone skill extraction notebook
├── templates/
│   ├── model.html           # UI for resume upload
│   └── new_model.html       # UI for manual skills input
├── README.md                # Project documentation
└── ...                      # Other files (logs, PDFs, etc.)
```

---

## Setup & Installation

> **Important:**
> - For resume-based extraction (`hr_1.py`), use **Python 3.8, 3.9, or 3.10**. `pyresparser` and dependencies are not fully compatible with Python 3.12+.
> - For manual skills input (`hr_2.py`), Python 3.12+ works fine.

### 1. Clone the repository

```bash
git clone https://github.com/ankit-kumarz/HRAnalytics-Project-main.git
cd HRAnalytics-Project-main
```

### 2. Create and activate a virtual environment (recommended)

```bash
# For Python 3.10 (recommended for resume extraction)
python3.10 -m venv venv
venv\Scripts\activate  # On Windows
# Or
source venv/bin/activate  # On Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# Or manually:
pip install flask numpy pandas scikit-learn nltk ftfy textract pdfminer.six tika spacy pyresparser
python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm
```

---

## Usage

### Version 1: Resume-Based Job Matching

```bash
python hr_1.py
# Visit http://127.0.0.1:5000 in your browser
# Upload your resume (PDF, DOCX, or TXT)
# View top job matches based on your skills
```

### Version 2: Manual Skills Input

```bash
python hr_2.py
# Visit http://127.0.0.1:5000 in your browser
# Enter your skills (comma or space separated)
# View top job matches
```

---

## Dataset

- `job_final.csv` contains job postings scraped from Glassdoor (Position, Company, Location, Description, etc.)
- Scraping code is in `glassdoor scrapping.ipynb`

---

## Troubleshooting

- If you get errors with `pyresparser` or `pandas` on Python 3.12+, use Python 3.10 or 3.9 for `hr_1.py`.
- Make sure all dependencies are installed and NLTK stopwords are downloaded.
- For PDF extraction issues, ensure `textract`, `pdfminer.six`, and `tika` are installed.

---

## Credits

- Project by [ankit-kumarz](https://github.com/ankit-kumarz)
- Dataset: Glassdoor (scraped for educational purposes)
- Libraries: Flask, pandas, scikit-learn, spaCy, pyresparser, textract, pdfminer, tika, NLTK, etc.

---

## License

This project is for educational and research purposes only.


>>>>>>> cc75e78 (Initial commit: HR Analytics Project)
