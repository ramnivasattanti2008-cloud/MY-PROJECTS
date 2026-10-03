# SQL Generator

Transform natural language descriptions into SQL queries using AI.

## Features

- Natural language to SQL conversion
- Support for multiple database dialects (PostgreSQL, MySQL, SQLite, SQL Server)
- Query explanation in plain English
- Clean dark theme UI

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create an API key
   - Set as environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key"
     ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select your target database
2. Describe what you want in plain English
3. Click "Generate SQL"
4. View the generated query and explanation
5. Copy the SQL to use in your project

## Example Queries

- "Show all users who signed up in the last month"
- "Count orders by status"
- "Find products with inventory below 10"
- "Get the top 5 customers by total spend"

## Project Structure

```
02-sql-generator/
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # This file
```
