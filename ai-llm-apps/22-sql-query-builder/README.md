# SQL Query Builder 🗃️

An AI-powered tool that converts natural language descriptions into SQL queries using Google's Gemini API.

## Features

- Describe data needs in plain English
- Support for multiple database types (PostgreSQL, MySQL, SQLite, SQL Server, Oracle)
- Optional table and relationship hints
- Clean, dark-themed interface
- Copy-ready SQL output

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Enter your API key in the sidebar

## Usage

1. Describe what data you want in natural language
2. Optionally specify tables and relationships
3. Select your database type
4. Click "Generate SQL" to get your query

## Examples

- "Show all customers who signed up this year"
- "Count orders by product category, only show categories with more than 100 orders"
- "Find the top 5 selling products last month with their revenue"

## Environment Variables

- `GEMINI_API_KEY` - Your Gemini API key (optional, can also enter in UI)
