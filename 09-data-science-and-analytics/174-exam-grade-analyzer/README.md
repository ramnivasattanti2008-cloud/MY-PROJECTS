# Exam Grade Analyzer 📚

A comprehensive Streamlit application for analyzing student exam results with detailed statistics and visualizations.

## Features

- **Data Upload**: Upload CSV files with student exam results
- **Overview Dashboard**: Pass rate, average scores, grade distribution
- **Subject Analysis**: Performance breakdown by subject with pass percentages
- **Student Rankings**: Top performers, search functionality, weak student identification
- **Visual Analytics**: Radar charts, heatmaps, scatter plots, correlation analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## CSV Format

Your CSV file should have the following columns:

```csv
student_name,roll_no,Mathematics,Physics,Chemistry,English
John Doe,2024001,85,78,92,88
Jane Smith,2024002,91,85,78,95
```

## Grading System

| Grade | Percentage Range |
|-------|-----------------|
| A+ | 90%+ |
| A | 80-89% |
| B+ | 70-79% |
| B | 60-69% |
| C | 50-59% |
| D | 40-49% |
| F | Below 40% |

## Tech Stack

- Streamlit - Web framework
- Pandas - Data manipulation
- Plotly - Interactive visualizations
- NumPy - Numerical computing

## License

MIT License
