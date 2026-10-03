# Text Statistics Analyzer

Analyze text files for statistics, vocabulary metrics, and readability scores.

## Features

- **Basic Statistics**: Characters, words, sentences, paragraphs, lines
- **Vocabulary Analysis**: Unique words, lexical diversity, syllable counts
- **Readability Scores**: Flesch, Gunning Fog, SMOG, ARI, Coleman-Liau
- **Word Frequency**: Top content words (stopwords filtered)
- **GUI Mode**: Interactive interface with tabbed results

## Installation

No installation required. Requires Python 3.7+.

```bash
python text-stats.py
```

## Usage

### GUI Mode (Recommended)

```bash
python text-stats.py
```

- Load a text file or paste text directly
- View basic statistics, readability scores, and word frequency
- Analyze sample text with one click

### CLI Mode

```bash
# Analyze a file
text-stats.py document.txt

# Analyze text directly
text-stats.py --text "Your text here goes..."

# Save results to file
text-stats.py document.txt -o results.txt
```

## Readability Indices Explained

| Index | Description | Interpretation |
|-------|-------------|----------------|
| Flesch Reading Ease | 0-100 scale | 60-70 is ideal for most content |
| Flesch-Kincaid Grade | US grade level | 7-8 is general audience |
| Gunning Fog Index | Years of education | 10-12 for business writing |
| SMOG Index | Years of education | Similar to Fog index |
| Automated Readability | US grade level | Based on characters/words |
| Coleman-Liau Index | US grade level | Based on letters/sentences |

### Flesch Reading Ease Interpretation

| Score | Grade Level | Description |
|-------|-------------|-------------|
| 90-100 | 5th grade | Very Easy |
| 80-90 | 6th grade | Easy |
| 70-80 | 7th grade | Fairly Easy |
| 60-70 | 8th-9th grade | Standard |
| 50-60 | 10th-12th grade | Fairly Difficult |
| 30-50 | College | Difficult |
| 0-30 | College Graduate | Very Difficult |

## Output Example

```
============================================================
TEXT STATISTICS ANALYSIS
============================================================

BASIC STATISTICS
----------------------------------------
Characters:          1,234
  (without spaces):  987
Words:               256
  Unique words:       142
  Avg word length:    4.52
Sentences:           18
  Avg sentence len:   14.2 words
Paragraphs:          5
Lines:               23

VOCABULARY ANALYSIS
----------------------------------------
Total syllables:      398
Avg syllables/word:   1.55
Lexical diversity:    55.5%

READABILITY INDICES
----------------------------------------
Flesch Reading Ease:      65.3 (Standard)
Flesch-Kincaid Grade:     7.8
Gunning Fog Index:        9.2
```

## Use Cases

### Content Writing
```bash
# Check if your blog post is readable
text-stats.py blog-post.txt
```

### Academic Writing
```bash
# Analyze thesis readability
text-stats.py thesis/chapter1.txt -o chapter1-analysis.txt
```

### Translation Quality
```bash
# Compare source and translated text
text-stats.py original.txt -o orig-stats.txt
text-stats.py translated.txt -o trans-stats.txt
```

### SEO Analysis
```bash
# Check keyword density and content length
text-stats.py article.txt
```

## Troubleshooting

**GUI doesn't start on Linux?**
```bash
sudo apt install python3-tk
```

**Special characters not detected?**
The analyzer uses UTF-8 encoding, which handles most Unicode characters.

**Want word-by-word syllable counts?**
Use the `--verbose` flag (if implemented) for detailed syllable analysis.
