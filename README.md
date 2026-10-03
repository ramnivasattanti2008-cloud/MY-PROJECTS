# MY-PROJECTS

Everything I've built that doesn't have its own repo, in one place: 389 projects, sorted by what they're made of. Most are small. A Flask app, a PDF tool, a browser game, built to see how something works and then left as it was.

The bigger work lives in separate repos, listed below.

## Bigger projects (own repos)

- [DESIGN-THINKING-](https://github.com/ramnivasattanti2008-cloud/DESIGN-THINKING-): Bharat Scam X, scam detection for Indian-language messaging, with the paper and a working app
- [smriti-ai](https://github.com/ramnivasattanti2008-cloud/smriti-ai)
- [FINAL-SIH](https://github.com/ramnivasattanti2008-cloud/FINAL-SIH)
- [VOJAS](https://github.com/ramnivasattanti2008-cloud/VOJAS)
- [AVISHKAR-](https://github.com/ramnivasattanti2008-cloud/AVISHKAR-)
- [ai-portfolio-projects](https://github.com/ramnivasattanti2008-cloud/ai-portfolio-projects): 15 AI projects

## What's in here

| Category | Count |
|---|---|
| [AI and LLM apps](#ai-and-llm-apps) | 52 |
| [Flask apps](#flask-apps) | 53 |
| [Django apps](#django-apps) | 5 |
| [FastAPI apps](#fastapi-apps) | 8 |
| [Node and Express](#node-and-express) | 12 |
| [React apps](#react-apps) | 25 |
| [Next.js apps](#nextjs-apps) | 6 |
| [Streamlit apps](#streamlit-apps) | 1 |
| [Data science and analytics](#data-science-and-analytics) | 33 |
| [Python utilities](#python-utilities) | 62 |
| [Security and network tools](#security-and-network-tools) | 14 |
| [Fun and games](#fun-and-games) | 24 |
| [HTML mini apps](#html-mini-apps) | 94 |

## Running a project

Each project folder is self-contained. Open its README for the details. The usual routes:

```bash
# Python projects
cd flask-apps/flask-todo
pip install -r requirements.txt
python app.py

# Node, React and Next.js projects
cd nextjs-apps/nextjs-blog
npm install
npm run dev
```

The AI apps need an API key. Put it in an environment variable as the project's README says, never in the code. The single-file HTML tools need nothing, just open them in a browser.

## Index

### AI and LLM apps

Small apps built on Gemini and similar APIs: chatbots, writing helpers, summarisers, interview prep.

| Project | What it does |
|---|---|
| [01-ai-chatbot](ai-llm-apps/01-ai-chatbot) | A simple conversational AI chatbot powered by Google Gemini. |
| [02-sql-generator](ai-llm-apps/02-sql-generator) | Transform natural language descriptions into SQL queries using AI. |
| [03-code-reviewer](ai-llm-apps/03-code-reviewer) | AI-powered code review tool that analyzes your code and provides feedback. |
| [04-study-buddy](ai-llm-apps/04-study-buddy) | Your AI-powered study assistant for learning any topic. |
| [05-meeting-summarizer](ai-llm-apps/05-meeting-summarizer) | AI-powered tool to summarize meeting notes, extract action items, and generate formal minutes. |
| [06-image-generator](ai-llm-apps/06-image-generator) | Transform your text ideas into detailed image prompts using Google Gemini AI. |
| [07-translator](ai-llm-apps/07-translator) | Intelligent text translation with automatic language detection using Google Gemini AI. |
| [08-flashcard-maker](ai-llm-apps/08-flashcard-maker) | Create study flashcards from any topic using Google Gemini AI. |
| [09-bug-detector](ai-llm-apps/09-bug-detector) | Find and fix bugs in your Python code using Google Gemini AI. |
| [10-todo-prioritizer](ai-llm-apps/10-todo-prioritizer) | AI-powered task prioritization that analyzes your tasks and explains the reasoning. |
| [11-tweet-generator](ai-llm-apps/11-tweet-generator) | Generate engaging, AI-powered tweets with hashtag suggestions. |
| [12-resume-builder](ai-llm-apps/12-resume-builder) | Generate professional, ATS-friendly resume bullet points instantly. |
| [13-youtube-shorts-script](ai-llm-apps/13-youtube-shorts-script) | Create engaging YouTube Shorts scripts with hook, body, and CTA sections. |
| [14-calorie-counter](ai-llm-apps/14-calorie-counter) | Estimate calories in your meals and get healthier alternatives. |
| [15-interview-prep](ai-llm-apps/15-interview-prep) | Generate AI-powered interview questions and sample answers for any role. |
| [21-code-explainer](ai-llm-apps/21-code-explainer) | An AI-powered tool that explains any code snippet line by line using Google's Gemini API. |
| [22-sql-query-builder](ai-llm-apps/22-sql-query-builder) | An AI-powered tool that converts natural language descriptions into SQL queries using Google's Gemini API. |
| [23-blog-post-writer](ai-llm-apps/23-blog-post-writer) | An AI-powered tool that generates professional blog post outlines with structure, content ideas, and SEO... |
| [24-product-review-summarizer](ai-llm-apps/24-product-review-summarizer) | An AI-powered tool that analyzes multiple product reviews to extract common themes, sentiment, and... |
| [25-git-commit-writer](ai-llm-apps/25-git-commit-writer) | An AI-powered tool that generates professional, descriptive git commit messages from your diff output... |
| [26-ai-tutor](ai-llm-apps/26-ai-tutor) | An AI-powered study companion that generates personalized lessons with key concepts, examples, and quizzes. |
| [27-cover-letter-gen](ai-llm-apps/27-cover-letter-gen) | AI-powered tool to create compelling, personalized cover letters. |
| [28-meeting-notes](ai-llm-apps/28-meeting-notes) | Transform messy meeting notes or transcripts into structured, actionable summaries. |
| [29-code-documenter](ai-llm-apps/29-code-documenter) | AI-powered tool that generates comprehensive documentation for your code. |
| [30-domain-generator](ai-llm-apps/30-domain-generator) | AI-powered startup domain name brainstormer with availability hints. |
| [31-ai-interview-prep](ai-llm-apps/31-ai-interview-prep) | cd 31-ai-interview-prep |
| [32-ai-grammar-check](ai-llm-apps/32-ai-grammar-check) | cd 32-ai-grammar-check |
| [33-ai-article-summarizer](ai-llm-apps/33-ai-article-summarizer) | cd 33-ai-article-summarizer |
| [34-ai-chatbot-widget](ai-llm-apps/34-ai-chatbot-widget) | cd 34-ai-chatbot-widget |
| [35-ai-keyword-researcher](ai-llm-apps/35-ai-keyword-researcher) | cd 35-ai-keyword-researcher |
| [36-ai-job-desc-analyzer](ai-llm-apps/36-ai-job-desc-analyzer) | Analyze job descriptions with AI to identify requirements and get resume improvement suggestions. |
| [37-ai-sentence-expander](ai-llm-apps/37-ai-sentence-expander) | Transform short phrases into compelling full paragraphs using AI. |
| [38-ai-music-lyrics](ai-llm-apps/38-ai-music-lyrics) | Generate original song lyrics with AI based on mood, theme, and genre. |
| [39-ai-mcq-generator](ai-llm-apps/39-ai-mcq-generator) | Generate multiple choice questions instantly for any topic with AI. |
| [40-ai-bio-generator](ai-llm-apps/40-ai-bio-generator) | Create catchy social media bios for any profession using AI. |
| [41-ai-outliner](ai-llm-apps/41-ai-outliner) | Transform any topic into a structured, compelling outline for essays, articles, and blog posts. |
| [42-ai-scheduler](ai-llm-apps/42-ai-scheduler) | Let AI create optimal daily schedules based on your tasks, available time, and energy levels. |
| [43-ai-deck-slides](ai-llm-apps/43-ai-deck-slides) | Generate professional PowerPoint slide content outlines for any presentation topic. |
| [44-ai-linkedin-post](ai-llm-apps/44-ai-linkedin-post) | Create engaging, viral-worthy LinkedIn posts with AI-powered content generation. |
| [45-ai-email-reply](ai-llm-apps/45-ai-email-reply) | Get professional email response suggestions for any received email. |
| [ai-dungeon](ai-llm-apps/ai-dungeon) | An interactive text adventure game powered by Google Gemini where your choices shape the story. Every... |
| [bio-writer](ai-llm-apps/bio-writer) | Craft perfect LinkedIn and Twitter bios in seconds with AI. Enter your professional details and get... |
| [caption-generator](ai-llm-apps/caption-generator) | Create viral-worthy captions for any image. Upload a photo or describe it, and get engaging captions for... |
| [content-calendar](ai-llm-apps/content-calendar) | Plan, schedule, and track your social media content. Manage posts across platforms and monitor engagement... |
| [hashtag-generator](ai-llm-apps/hashtag-generator) | AI-powered hashtag suggestions for social media posts. Get trending and relevant hashtags tailored to your... |
| [jarvis](ai-llm-apps/jarvis) | Local LLM via Ollama + Open Interpreter for controlling this PC + offline voice + optional Open WebUI. |
| [linkedin-post-generator](ai-llm-apps/linkedin-post-generator) | Create engaging, viral-worthy LinkedIn posts with AI. Perfect for professionals, entrepreneurs, and... |
| [pickup-lines](ai-llm-apps/pickup-lines) | A fun, creative tool powered by Google Gemini that generates witty, charming, and sometimes cheesy pickup... |
| [poem-generator](ai-llm-apps/poem-generator) | A creative poetry app powered by Google Gemini that transforms emotions and themes into beautiful,... |
| [recipe-generator](ai-llm-apps/recipe-generator) | A smart cooking assistant powered by Google Gemini that creates delicious recipes based on ingredients you... |
| [story-generator](ai-llm-apps/story-generator) | An interactive storytelling app powered by Google Gemini AI that crafts unique short stories based on your... |
| [translator-cli](ai-llm-apps/translator-cli) | A Python command-line tool for translating text between languages using Google Translate. |

### Flask apps

Full little web apps: todo lists, blogs, forums, dashboards, URL shorteners.

| Project | What it does |
|---|---|
| [api-dashboard](flask-apps/api-dashboard) | A Flask-based dashboard to manage API keys and monitor API usage statistics. |
| [blog-flask](flask-apps/blog-flask) | A minimalist blog with markdown support and commenting system. |
| [blog-site](flask-apps/blog-site) | A Flask-based blog with posts, comments, markdown support, and tags. |
| [blog-template](flask-apps/blog-template) | A complete blog application with posts, categories, tags, comments, and Markdown support. |
| [bookmarks-app](flask-apps/bookmarks-app) | A Flask application to save, organize, and search bookmarks with tags and notes. |
| [css-generators](flask-apps/css-generators) | A Flask web application with 5 CSS generator tools for developers. |
| [ecommerce-starter](flask-apps/ecommerce-starter) | A complete e-commerce application with products, cart, and checkout flow. |
| [flask-api](flask-apps/flask-api) | REST API template with CRUD operations and JWT authentication ready. |
| [flask-auth](flask-apps/flask-auth) | Authentication template with login, register, logout, and session management. |
| [flask-blog](flask-apps/flask-blog) | A Flask blog application with markdown support and comments. |
| [flask-bookmarks](flask-apps/flask-bookmarks) | A bookmark manager with tags and search functionality. |
| [flask-budget](flask-apps/flask-budget) | A Flask application to set monthly budgets and track expenses. |
| [flask-cms](flask-apps/flask-cms) | Simple CMS with pages, posts, and basic admin panel. |
| [flask-contacts](flask-apps/flask-contacts) | A simple Flask application to store and manage your contacts. |
| [flask-dashboard](flask-apps/flask-dashboard) | A dark-themed admin dashboard template built with Flask. |
| [flask-ecommerce](flask-apps/flask-ecommerce) | E-commerce starter with products, cart, and checkout flow. |
| [flask-events](flask-apps/flask-events) | An event management application with RSVP functionality and calendar view. |
| [flask-expenses](flask-apps/flask-expenses) | A Flask app to log expenses and view summaries by category. |
| [flask-forum](flask-apps/flask-forum) | A simple forum application with threads, replies, and categories. |
| [flask-gallery](flask-apps/flask-gallery) | A simple image gallery application with categories. |
| [flask-inventory](flask-apps/flask-inventory) | A Flask application to track inventory items, quantities, and stock levels. |
| [flask-landing](flask-apps/flask-landing) | A modern SaaS landing page template with hero, features, pricing, and contact sections. |
| [flask-links](flask-apps/flask-links) | A simple Flask app to save and organize links with tags. |
| [flask-notes](flask-apps/flask-notes) | A Flask notes application with tags support using SQLite. |
| [flask-notes-api](flask-apps/flask-notes-api) | A RESTful notes API built with Flask, featuring full CRUD operations and SQLite storage. |
| [flask-pastebin](flask-apps/flask-pastebin) | A code pastebin with syntax highlighting, expiration options, and password protection. |
| [flask-poll](flask-apps/flask-poll) | A simple polling application built with Flask and SQLite. |
| [flask-quiz](flask-apps/flask-quiz) | An interactive quiz application using the Open Trivia Database API with score tracking and leaderboards. |
| [flask-reading](flask-apps/flask-reading) | A Flask application to track your reading progress across books. |
| [flask-recipes](flask-apps/flask-recipes) | A Flask app to store and browse recipes with ingredients and instructions. |
| [flask-scheduler](flask-apps/flask-scheduler) | A simple task scheduling application built with Flask and SQLite. |
| [flask-tasks](flask-apps/flask-tasks) | A Flask app to track tasks with priorities and due dates. |
| [flask-todo](flask-apps/flask-todo) | A simple Flask todo application with SQLite database. |
| [flask-url-shortener](flask-apps/flask-url-shortener) | A modern URL shortener with custom short codes, click tracking, and analytics dashboard. |
| [flask-wiki](flask-apps/flask-wiki) | A dark-themed collaborative wiki built with Flask and Markdown. |
| [landing-page](flask-apps/landing-page) | A modern, dark-themed landing page template built with Flask. |
| [microblog](flask-apps/microblog) | A Flask-based microblog platform with user authentication, following system, and likes. |
| [news-aggregator](flask-apps/news-aggregator) | A news reader application using Flask and NewsAPI.org. |
| [password-vault](flask-apps/password-vault) | A Flask application for securely storing passwords with Fernet encryption. |
| [paste-bin](flask-apps/paste-bin) | A Flask-based pastebin with syntax highlighting, expiration options, and password protection. |
| [paste-bin-flask](flask-apps/paste-bin-flask) | A code/text pastebin with syntax highlighting powered by Highlight.js. |
| [pastebin](flask-apps/pastebin) | A Flask-based code/text pastebin with syntax highlighting, expiration, and password protection. |
| [portfolio-site](flask-apps/portfolio-site) | A modern, dark-themed portfolio template built with Flask. |
| [quiz-api-flask](flask-apps/quiz-api-flask) | A trivia quiz application that fetches questions from the Open Trivia Database API. |
| [quiz-app](flask-apps/quiz-app) | A Flask-based quiz application with multiple categories, difficulty levels, and leaderboards. |
| [quiz-game](flask-apps/quiz-game) | A Flask quiz game that fetches trivia questions from the Open Trivia Database API. |
| [recipe-app](flask-apps/recipe-app) | A Flask-based recipe management application with search, categories, and ratings. |
| [saas-starter](flask-apps/saas-starter) | A complete SaaS application starter template with authentication, dashboard, billing, and API key management. |
| [sql-playground](flask-apps/sql-playground) | A Flask web application for running SQL queries on SQLite databases with a user-friendly interface. |
| [todo-api](flask-apps/todo-api) | A Flask REST API for managing todos with filtering, search, and bulk operations. |
| [todo-api-flask](flask-apps/todo-api-flask) | A RESTful API for managing a todo list with full CRUD operations. |
| [url-shortener](flask-apps/url-shortener) | A Flask-based URL shortener with SQLite database, click tracking, and analytics. |
| [url-shortener-flask](flask-apps/url-shortener-flask) | A simple URL shortener with click tracking and analytics dashboard. |

### Django apps

Blog, wiki, e-commerce and social starters.

| Project | What it does |
|---|---|
| [django-blog](django-apps/django-blog) | A clean, minimal blog application built with Django. |
| [django-ecommerce](django-apps/django-ecommerce) | A starter e-commerce application with products, cart, and checkout. |
| [django-social](django-apps/django-social) | A social networking application with user profiles and follow system. |
| [django-todo](django-apps/django-todo) | A task management application with user authentication. |
| [django-wiki](django-apps/django-wiki) | A collaborative wiki application with markdown support and version history. |

### FastAPI apps

REST APIs with auth, CRUD and file handling.

| Project | What it does |
|---|---|
| [fastapi-auth](fastapi-apps/fastapi-auth) | A complete Authentication API built with FastAPI, featuring JWT tokens, protected routes, and role-based... |
| [fastapi-blog](fastapi-apps/fastapi-blog) | A complete Blog API built with FastAPI and SQLite, featuring posts, comments, categories, and pagination. |
| [fastapi-crud](fastapi-apps/fastapi-crud) | A simple FastAPI CRUD API for managing tasks with SQLite database. |
| [fastapi-file](fastapi-apps/fastapi-file) | A comprehensive file upload/download service built with FastAPI, featuring metadata management, search,... |
| [fastapi-todo](fastapi-apps/fastapi-todo) | A simple and elegant Todo API built with FastAPI and SQLite. |
| [fastapi-weather](fastapi-apps/fastapi-weather) | A free weather API that proxies Open-Meteo. No API key required. |
| [graphql-api](fastapi-apps/graphql-api) | A Python GraphQL API using Strawberry for managing books. |
| [websockets-chat](fastapi-apps/websockets-chat) | A simple real-time chat server using FastAPI WebSockets. |

### Node and Express

Backend services and realtime chat.

| Project | What it does |
|---|---|
| [auth-api](node-express-apis/auth-api) | A secure authentication API with JWT tokens and bcrypt password hashing. |
| [express-notes-api](node-express-apis/express-notes-api) | A RESTful notes API built with Express.js, storing notes in a JSON file. |
| [express-rest](node-express-apis/express-rest) | A simple Express.js REST API for managing posts with middleware examples, error handling, and pagination. |
| [file-upload-api](node-express-apis/file-upload-api) | Express API for uploading, listing, and managing files. |
| [node-chat](node-express-apis/node-chat) | A real-time chat application built with Express.js and Socket.IO. |
| [node-file-upload](node-express-apis/node-file-upload) | An Express.js file upload application with Multer. |
| [node-pastebin](node-express-apis/node-pastebin) | A simple Express.js code pastebin with syntax highlighting using highlight.js. |
| [node-todo-api](node-express-apis/node-todo-api) | A RESTful Todo API with JWT authentication built with Express.js and SQLite. |
| [node-url-shortener](node-express-apis/node-url-shortener) | A simple Express.js URL shortener with SQLite database. |
| [notes-api](node-express-apis/notes-api) | A RESTful API for managing notes with CRUD operations, search, and categories. |
| [proxy-api](node-express-apis/proxy-api) | Express proxy service to bypass CORS restrictions when calling external APIs. |
| [url-api](node-express-apis/url-api) | Express API for creating short URLs and tracking visits. |

### React apps

Components and small front-end apps.

| Project | What it does |
|---|---|
| [chat-room](react-apps/chat-room) | A real-time multi-room chat application built with Flask-SocketIO and React. |
| [code-paste](react-apps/code-paste) | A code sharing site with syntax highlighting. Paste code, get a shareable link, and view with beautiful... |
| [flask-portfolio](react-apps/flask-portfolio) | A sleek dark-themed portfolio template built with Flask and Bootstrap. |
| [link-collector](react-apps/link-collector) | A link bookmarking and organization app. Save URLs with titles, descriptions, and tags. Search, filter,... |
| [mini-twitter](react-apps/mini-twitter) | A lightweight Twitter clone with tweets, follows, likes, and a social feed. |
| [modal-portal](react-apps/modal-portal) | A fully-featured modal component with React Portal, backdrop, focus trap, and keyboard support. |
| [poll-app](react-apps/poll-app) | A live polling application with real-time result updates. Create polls, vote, and watch results update... |
| [react-calculator](react-apps/react-calculator) | A modern calculator app built with React and TypeScript, featuring a sleek dark theme and full keyboard... |
| [react-emoji-picker](react-apps/react-emoji-picker) | A sleek, dark-themed emoji picker component built with React and TypeScript. |
| [react-meme](react-apps/react-meme) | Create memes with top and bottom text and download as PNG. |
| [react-music-player](react-apps/react-music-player) | A sleek, dark-themed music player built with React and TypeScript. |
| [react-notes](react-apps/react-notes) | A minimal notes app with localStorage persistence. |
| [react-qr](react-apps/react-qr) | Generate QR codes from text or URLs and download as PNG. |
| [react-quiz](react-apps/react-quiz) | An interactive quiz application with multiple choice questions, score tracking, and detailed explanations. |
| [react-random-quote](react-apps/react-random-quote) | A beautiful, dark-themed random quote generator built with React and TypeScript. |
| [react-random-user](react-apps/react-random-user) | A React application that fetches and displays random user profiles from the RandomUser.me API. |
| [react-stopwatch](react-apps/react-stopwatch) | A sleek, dark-themed stopwatch app built with React and TypeScript. |
| [react-timer](react-apps/react-timer) | A sleek countdown timer built with React. |
| [react-todo](react-apps/react-todo) | A feature-rich todo application with localStorage persistence, categories, filtering, and dark/light theme... |
| [react-todo-list](react-apps/react-todo-list) | A polished, feature-rich Todo List React component with local storage persistence. |
| [react-weather](react-apps/react-weather) | A weather app using the Open-Meteo API with geocoding support. |
| [react-weather-app](react-apps/react-weather-app) | A beautiful weather application that fetches real-time weather data using the Open-Meteo API (free, no API... |
| [react-weather-widget](react-apps/react-weather-widget) | A sleek, dark-themed weather widget built with React and TypeScript. |
| [search-autocomplete](react-apps/search-autocomplete) | A fully-featured search input with autocomplete dropdown, debounced API calls, keyboard navigation, and... |
| [todo-context](react-apps/todo-context) | A complete React todo application with CRUD operations, localStorage persistence, and filter functionality. |

### Next.js apps

Blog, dashboard, store, landing page, portfolio and a SaaS starter.

| Project | What it does |
|---|---|
| [nextjs-blog](nextjs-apps/nextjs-blog) | A modern, dark-themed blog template built with Next.js 15, TypeScript, MDX, and Tailwind CSS. |
| [nextjs-dashboard](nextjs-apps/nextjs-dashboard) | A modern, dark-themed admin dashboard template built with Next.js 15, TypeScript, Tailwind CSS, and Lucide... |
| [nextjs-ecommerce](nextjs-apps/nextjs-ecommerce) | A modern, dark-themed e-commerce template built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons. |
| [nextjs-landing](nextjs-apps/nextjs-landing) | A modern, dark-themed landing page template built with Next.js 15, TypeScript, and Tailwind CSS. |
| [nextjs-portfolio](nextjs-apps/nextjs-portfolio) | A modern, dark-themed portfolio website built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons. |
| [portfolio](nextjs-apps/portfolio) | A world-class portfolio website for Attanti Ramnivas, AI/ML Developer and B.Tech CSBS Student. |

### Streamlit apps

Quick data and recipe apps.

| Project | What it does |
|---|---|
| [markdown-editor](streamlit-apps/markdown-editor) | A Streamlit application for writing Markdown with live preview and HTML export. |

### Data science and analytics

Classifiers, predictors, CSV tools and charts.

| Project | What it does |
|---|---|
| [budget-tracker](data-science-and-analytics/budget-tracker) | A dark-themed budget tracking application with charts and savings goals. |
| [covid-tracker](data-science-and-analytics/covid-tracker) | A real-time COVID-19 statistics dashboard built with Streamlit and Plotly. |
| [cricket-analysis](data-science-and-analytics/cricket-analysis) | A comprehensive Streamlit application for analyzing cricket player statistics with interactive visualizations. |
| [cricket-stats](data-science-and-analytics/cricket-stats) | An interactive dashboard to explore cricket player stats, team rankings, and match data. |
| [crypto-tracker](data-science-and-analytics/crypto-tracker) | A real-time cryptocurrency price tracker using Flask and the CoinGecko API. |
| [csv-analyzer](data-science-and-analytics/csv-analyzer) | A Python utility for comprehensive analysis of CSV files with statistical summaries, data quality... |
| [csv-visualizer](data-science-and-analytics/csv-visualizer) | Generate interactive charts and visualizations from CSV data. |
| [data-cleaner](data-science-and-analytics/data-cleaner) | Clean messy CSV data by removing duplicates, fixing encoding issues, and trimming whitespace. |
| [data-exporter](data-science-and-analytics/data-exporter) | A command-line tool for exporting SQLite databases to JSON, CSV, SQL dump, or NDJSON formats. |
| [diabetes-predictor](data-science-and-analytics/diabetes-predictor) | A machine learning application that predicts diabetes risk based on health metrics using the Pima Indians... |
| [digit-recognizer](data-science-and-analytics/digit-recognizer) | A beginner-friendly machine learning project that recognizes handwritten digits (0-9) using Support Vector... |
| [exam-grade-analyzer](data-science-and-analytics/exam-grade-analyzer) | A comprehensive Streamlit application for analyzing student exam results with detailed statistics and... |
| [excel-to-json](data-science-and-analytics/excel-to-json) | Convert Excel (.xlsx, .xls) and CSV files to JSON with support for multiple sheets. |
| [expense-simple](data-science-and-analytics/expense-simple) | A Streamlit application for tracking personal expenses with visual analytics. |
| [expense-tracker](data-science-and-analytics/expense-tracker) | A budget tracking application built with Streamlit and Python. |
| [football-analysis](data-science-and-analytics/football-analysis) | A comprehensive Streamlit application for analyzing football/soccer player statistics with interactive... |
| [git-stats](data-science-and-analytics/git-stats) | A command-line tool to display GitHub statistics for any user. Shows repositories, stars, languages, and... |
| [github-profile-stats](data-science-and-analytics/github-profile-stats) | A Python script that generates visual ASCII art statistics for any GitHub profile. Display commits,... |
| [grade-calculator](data-science-and-analytics/grade-calculator) | A comprehensive academic performance tracker with GPA calculation and visualizations. |
| [house-price-predictor](data-science-and-analytics/house-price-predictor) | A beginner-friendly machine learning project that predicts house prices using Linear Regression. |
| [iris-classifier](data-science-and-analytics/iris-classifier) | A beginner-friendly machine learning project that classifies iris flowers into three species based on... |
| [json-to-excel](data-science-and-analytics/json-to-excel) | Convert JSON data to Excel (.xlsx) files with formatting and nested structure support. |
| [movie-recommender](data-science-and-analytics/movie-recommender) | A Python CLI application that recommends movies based on your genre preferences. Features ASCII art... |
| [population-viz](data-science-and-analytics/population-viz) | An interactive dashboard to explore global population data. |
| [reading-list](data-science-and-analytics/reading-list) | Track your reading journey with a beautiful book manager. |
| [recipe-app-streamlit](data-science-and-analytics/recipe-app-streamlit) | A clean, dark-themed recipe management application. |
| [sales-dashboard](data-science-and-analytics/sales-dashboard) | A comprehensive Streamlit application for analyzing sales data with interactive visualizations and KPIs. |
| [sentiment-simple](data-science-and-analytics/sentiment-simple) | A beginner-friendly machine learning project that analyzes the sentiment (positive, negative, or neutral)... |
| [spam-detector](data-science-and-analytics/spam-detector) | A beginner-friendly machine learning project that detects spam messages using Naive Bayes classification. |
| [stock-viz](data-science-and-analytics/stock-viz) | An interactive stock market visualization dashboard with technical indicators. |
| [study-tracker](data-science-and-analytics/study-tracker) | Track your study sessions and visualize progress. |
| [weather-dashboard](data-science-and-analytics/weather-dashboard) | A beautiful Streamlit application that displays weather information for multiple cities side by side,... |
| [weight-tracker](data-science-and-analytics/weight-tracker) | Track your weight and health metrics with beautiful charts. |

### Python utilities

Command line and desktop helpers for files, PDFs, images and text.

| Project | What it does |
|---|---|
| [api-docs-generator](python-utilities/api-docs-generator) | Auto-generate API documentation from Python docstrings. Scans Python files, extracts function signatures,... |
| [auto-backup](python-utilities/auto-backup) | A Python script that creates timestamped compressed backups of important folders. |
| [auto-email-sender](python-utilities/auto-email-sender) | A Python tool for sending emails via SMTP (Gmail) with support for attachments, HTML content, and email... |
| [bulk-renamer](python-utilities/bulk-renamer) | A Python command-line tool for batch renaming files with pattern matching, preview support, and undo... |
| [clipboard-manager](python-utilities/clipboard-manager) | Manage clipboard history with save, search, and paste functionality. |
| [csv-cleaner](python-utilities/csv-cleaner) | A Python CLI tool for cleaning and standardizing CSV files. |
| [currency-cmd](python-utilities/currency-cmd) | A colorful command-line currency converter using free exchange rate APIs. |
| [currency-converter](python-utilities/currency-converter) | A Python CLI tool to convert between currencies using free exchange rate APIs. |
| [data-exporter](python-utilities/data-exporter) | Data exporter |
| [data-generator](python-utilities/data-generator) | A Python CLI tool for generating fake data for testing purposes. |
| [data-validator](python-utilities/data-validator) | A Python CLI tool for validating data against common rules and reporting errors. |
| [db-migrator](python-utilities/db-migrator) | A Python script for converting data between SQLite databases and CSV files. |
| [db-migrator-script](python-utilities/db-migrator-script) | Db migrator script |
| [db-visualizer](python-utilities/db-visualizer) | A Python script that generates ASCII ER diagrams from SQLite databases. Visualize your database schema,... |
| [db-visualizer-script](python-utilities/db-visualizer-script) | Db visualizer script |
| [disk-usage](python-utilities/disk-usage) | Analyze disk usage and visualize largest files and folders with bar charts. |
| [duplicate-finder](python-utilities/duplicate-finder) | Find duplicate files by content hash and optionally remove them. |
| [excel-to-json](python-utilities/excel-to-json) | A Python CLI tool for converting Excel and CSV files to JSON format. |
| [file-organizer](python-utilities/file-organizer) | A Python script that automatically organizes files in a directory by their type into categorized subfolders. |
| [file-searcher](python-utilities/file-searcher) | A fast Python command-line tool for searching files by name, content, size, and modification date. |
| [file-splitter](python-utilities/file-splitter) | Split large files into manageable chunks and merge them back with verification. |
| [folder-sync](python-utilities/folder-sync) | Synchronize two folders by copying new and modified files from source to destination. |
| [image-batch](python-utilities/image-batch) | Batch resize, crop, compress, and transform multiple images with a single command. |
| [image-compressor](python-utilities/image-compressor) | Reduce image file sizes with configurable JPEG quality, PNG optimization, and batch processing. |
| [image-converter](python-utilities/image-converter) | Convert images between formats: JPEG, PNG, WebP, GIF, BMP, TIFF, ICO. Batch conversion supported. |
| [image-cropper](python-utilities/image-cropper) | Crop images with interactive selection or CLI using exact coordinates. |
| [image-metadata](python-utilities/image-metadata) | A Python utility for extracting and displaying EXIF metadata from images, including camera information,... |
| [image-resizer](python-utilities/image-resizer) | Resize images by width, height, or percentage. Supports batch processing of entire directories. |
| [image-resizer-script](python-utilities/image-resizer-script) | A Python CLI tool to resize images to different dimensions with batch processing support. |
| [image-watermark](python-utilities/image-watermark) | Add text or image watermarks to images with customizable position control. |
| [json-editor](python-utilities/json-editor) | An interactive command-line tool for viewing, adding, editing, and deleting keys in JSON files. |
| [json-to-csv](python-utilities/json-to-csv) | Json to csv |
| [json-to-model](python-utilities/json-to-model) | Convert JSON data to typed data models in Python, TypeScript, or Go. Perfect for quickly creating... |
| [mock-api](python-utilities/mock-api) | A Python Flask-based mock API server. Define endpoints in YAML and serve realistic mock responses. Perfect... |
| [movie-info](python-utilities/movie-info) | A command-line tool to look up movie information including ratings, cast, plot, and more. Uses the OMDB API. |
| [pdf-info](python-utilities/pdf-info) | Extract metadata and information from PDF files including page count, title, author, and more. |
| [pdf-merge](python-utilities/pdf-merge) | Merge multiple PDF files into a single PDF document with optional bookmarks. |
| [pdf-merger](python-utilities/pdf-merger) | Merge multiple PDF files into one with support for drag & drop and CLI usage. |
| [pdf-split](python-utilities/pdf-split) | Split PDF files into separate pages, page ranges, or chunks. |
| [pdf-to-images](python-utilities/pdf-to-images) | Convert PDF pages to images with customizable resolution and format. |
| [pdf-to-text](python-utilities/pdf-to-text) | A Python CLI tool to extract text content from PDF files with support for tables and metadata. |
| [pdf-watermark](python-utilities/pdf-watermark) | Add text or image watermarks to PDF documents with customizable options. |
| [qr-batch](python-utilities/qr-batch) | Generate multiple QR codes from CSV data. Perfect for batch processing URLs, contacts, WiFi credentials,... |
| [qr-code-reader](python-utilities/qr-code-reader) | A versatile Python tool for generating and reading QR codes. Supports image files, webcam input, batch... |
| [qr-generator](python-utilities/qr-generator) | A Python command-line tool to generate QR codes from text or URLs and save them as PNG images. |
| [query-builder](python-utilities/query-builder) | A visual tool for building SQL queries without writing code. Point and click to select tables, columns,... |
| [quick-notes](python-utilities/quick-notes) | A fast, terminal-based note-taking application with tagging and search capabilities. |
| [regex-extractor](python-utilities/regex-extractor) | A Python utility for extracting emails, phone numbers, URLs, IP addresses, and more from text files or... |
| [regex-tester](python-utilities/regex-tester) | Interactive regex pattern testing with highlighted matches and detailed group information. |
| [screenshot](python-utilities/screenshot) | Take screenshots - full screen or with interactive region selection. |
| [screenshot-capture](python-utilities/screenshot-capture) | Take screenshots on Windows using Pillow and Windows GDI. Full screen, specific monitors, region... |
| [screenshot-tool](python-utilities/screenshot-tool) | A Python script for capturing screenshots with hotkey support. Supports full screen and region capture on... |
| [sql-query-runner](python-utilities/sql-query-runner) | A Python CLI tool for running SQL queries against CSV files. |
| [system-info](python-utilities/system-info) | A Python command-line tool to display comprehensive system information including OS, CPU, RAM, disk space,... |
| [text-stats](python-utilities/text-stats) | Analyze text files for statistics, vocabulary metrics, and readability scores. |
| [text-to-speech](python-utilities/text-to-speech) | A Python script that converts text to speech using Google Text-to-Speech (gTTS) and saves the result as an... |
| [todo-cmd](python-utilities/todo-cmd) | A powerful command-line todo list manager with priorities, due dates, and categories. |
| [url-checker](python-utilities/url-checker) | A Python CLI tool to check if URLs are alive, returning status codes and response times. |
| [video-downloader](python-utilities/video-downloader) | A powerful YouTube video and audio downloader using the yt-dlp library. |
| [watermark-tool](python-utilities/watermark-tool) | Add text or image watermarks to images with full position, opacity, and batch control. |
| [weather-cli](python-utilities/weather-cli) | A Python CLI tool to get weather information for any city using the free Open-Meteo API. |
| [web-scraper](python-utilities/web-scraper) | A powerful and flexible web scraping tool using Python with requests and BeautifulSoup. Extract structured... |

### Security and network tools

Educational scanners, hashing and encryption tools. Read the disclaimer in docs/.

| Project | What it does |
|---|---|
| [cert-checker](security-and-network-tools/cert-checker) | A Python tool that demonstrates SSL/TLS certificate inspection for learning about web security and HTTPS... |
| [file-encrypter](security-and-network-tools/file-encrypter) | A Python utility for encrypting and decrypting files using Fernet symmetric encryption. |
| [file-hasher](security-and-network-tools/file-hasher) | Calculate cryptographic hashes (MD5, SHA1, SHA256, SHA512) for any file. |
| [hash-cracker](security-and-network-tools/hash-cracker) | A Python tool that demonstrates password hash vulnerabilities through dictionary attacks. |
| [leak-checker](security-and-network-tools/leak-checker) | A Python tool that checks if emails or passwords have appeared in known data breaches using the... |
| [pdf-encrypt](security-and-network-tools/pdf-encrypt) | Encrypt or decrypt PDF files with password protection and permissions control. |
| [port-scanner](security-and-network-tools/port-scanner) | A Python tool that demonstrates network port scanning concepts for learning about network security. |
| [request-logger](security-and-network-tools/request-logger) | A browser-based tool to log and inspect HTTP requests. Use the browser's fetch API to make requests and... |
| [rest-client](security-and-network-tools/rest-client) | A command-line HTTP client for making API requests with formatted JSON output. |
| [simple-proxy-api](security-and-network-tools/simple-proxy-api) | A Flask API that proxies requests to external APIs, helping you avoid CORS issues when building front-end... |
| [ssh-keygen-tool](security-and-network-tools/ssh-keygen-tool) | A Python tool that demonstrates SSH key pair generation for learning about public-key cryptography. |
| [web-server](security-and-network-tools/web-server) | A simple HTTP web server built entirely with Python's built-in http.server module. No external... |
| [webhook-tester](security-and-network-tools/webhook-tester) | A Flask application to receive, store, and display webhook payloads. Useful for testing webhooks during... |
| [wifi-passwords](security-and-network-tools/wifi-passwords) | A Windows utility to view saved WiFi passwords stored on your computer. View all saved WiFi networks or... |

### Fun and games

Terminal games and small toys.

| Project | What it does |
|---|---|
| [animated-counter](fun-and-games/animated-counter) | A React component that animates numbers when scrolled into view, with smooth easing and various... |
| [ascii-art](fun-and-games/ascii-art) | A fun CLI tool that converts text into beautiful ASCII art with multiple font styles and color support. |
| [color-detect](fun-and-games/color-detect) | Upload any image and discover its dominant colors! Perfect for designers, artists, and anyone curious... |
| [dark-mode-toggle](fun-and-games/dark-mode-toggle) | A beautiful, animated dark/light mode toggle switch with smooth transitions, stars animation, and sun/moon... |
| [fortune-cookie](fun-and-games/fortune-cookie) | A fun virtual fortune cookie that reveals random fortunes with a beautiful ASCII art presentation! |
| [gif-maker](fun-and-games/gif-maker) | Create animated GIFs from images with adjustable speed, loop, and resize options. |
| [hangman](fun-and-games/hangman) | A classic word guessing game with ASCII art and multiple word categories. |
| [joke-teller](fun-and-games/joke-teller) | Get ready to laugh with random jokes and fun facts! Features standard jokes, programming humor, and... |
| [joke-teller-script](fun-and-games/joke-teller-script) | Joke teller script |
| [mad-libs](fun-and-games/mad-libs) | The classic word-filling game brought to life! Create hilarious stories by filling in blanks with funny words. |
| [mad-libs-script](fun-and-games/mad-libs-script) | Mad libs script |
| [magic-8ball](fun-and-games/magic-8ball) | A mystical fortune-telling experience in your terminal! Ask any yes/no question and receive wisdom from... |
| [magic-8ball-script](fun-and-games/magic-8ball-script) | Magic 8ball script |
| [meme-generator](fun-and-games/meme-generator) | A fun and easy tool to create memes by adding text to images. Perfect for creating classic memes with top... |
| [number-guessing](fun-and-games/number-guessing) | A twist on the classic guessing game where YOU think of a number and the computer tries to guess it! |
| [quiz-game](fun-and-games/quiz-game) | A multi-choice quiz game with multiple categories and difficulty levels. Test your knowledge! |
| [rock-paper-scissors](fun-and-games/rock-paper-scissors) | The classic game with an epic twist! Challenge the computer in best-of-N rounds with ASCII art, win... |
| [rock-paper-scissors-script](fun-and-games/rock-paper-scissors-script) | Rock paper scissors script |
| [snake-game](fun-and-games/snake-game) | A classic arcade snake game built with Python's turtle graphics module. |
| [text-adventure](fun-and-games/text-adventure) | A classic text adventure game where you explore a mysterious castle, collect items, solve puzzles, and... |
| [text-to-ascii](fun-and-games/text-to-ascii) | Transform any image into stunning ASCII art! Perfect for creating text-based versions of photos, logos,... |
| [tic-tac-toe](fun-and-games/tic-tac-toe) | Play against an unbeatable AI opponent using the Minimax algorithm with alpha-beta pruning! |
| [truth-or-dare](fun-and-games/truth-or-dare) | The ultimate party game experience! Challenge your friends, uncover secrets, and complete hilarious dares. |
| [truth-or-dare-script](fun-and-games/truth-or-dare-script) | Truth or dare script |

### HTML mini apps

Single-file browser tools and games. Open the file, it runs.

| Project | What it does |
|---|---|
| [color-blender.html](html-mini-apps/design-tools/color-blender.html) | Color Blender |
| [color-contrast.html](html-mini-apps/design-tools/color-contrast.html) | Color Contrast Checker |
| [color-mixer.html](html-mini-apps/design-tools/color-mixer.html) | Color Mixer |
| [color-palette.html](html-mini-apps/design-tools/color-palette.html) | Color Palette Extractor |
| [color-picker-advanced.html](html-mini-apps/design-tools/color-picker-advanced.html) | Advanced Color Picker |
| [color-themer.html](html-mini-apps/design-tools/color-themer.html) | Color Themer |
| [css-animation.html](html-mini-apps/design-tools/css-animation.html) | CSS Animation Generator |
| [css-variables.html](html-mini-apps/design-tools/css-variables.html) | CSS Variables Generator |
| [emoji-art.html](html-mini-apps/design-tools/emoji-art.html) | ASCII Art Generator |
| [emoji-picker.html](html-mini-apps/design-tools/emoji-picker.html) | Emoji Picker |
| [emoji-search.html](html-mini-apps/design-tools/emoji-search.html) | Emoji Search |
| [favicon-creator.html](html-mini-apps/design-tools/favicon-creator.html) | Favicon Creator |
| [favicon-generator.html](html-mini-apps/design-tools/favicon-generator.html) | Favicon Generator |
| [font-pairing.html](html-mini-apps/design-tools/font-pairing.html) | Font Pairing |
| [gradient-generator.html](html-mini-apps/design-tools/gradient-generator.html) | CSS Gradient Generator |
| [gradient-preview.html](html-mini-apps/design-tools/gradient-preview.html) | Gradient Preview |
| [mockup-generator.html](html-mini-apps/design-tools/mockup-generator.html) | Mockup Generator |
| [placeholder-generator.html](html-mini-apps/design-tools/placeholder-generator.html) | Placeholder Generator |
| [svg-generator.html](html-mini-apps/design-tools/svg-generator.html) | SVG Generator |
| [LoremGenerator.html](html-mini-apps/dev-tools/LoremGenerator.html) | Lorem Ipsum Generator |
| [api-playground.html](html-mini-apps/dev-tools/api-playground.html) | API Playground |
| [api-tester.html](html-mini-apps/dev-tools/api-tester.html) | API Tester |
| [ascii-table.html](html-mini-apps/dev-tools/ascii-table.html) | ASCII Table Generator |
| [base64-editor.html](html-mini-apps/dev-tools/base64-editor.html) | Base64 Editor |
| [base64-tool.html](html-mini-apps/dev-tools/base64-tool.html) | Base64 Encoder/Decoder |
| [binary-clock.html](html-mini-apps/dev-tools/binary-clock.html) | Binary Clock |
| [binary-decimal.html](html-mini-apps/dev-tools/binary-decimal.html) | Binary-Decimal Converter |
| [code-diff.html](html-mini-apps/dev-tools/code-diff.html) | Code Diff Tool |
| [code-formatter.html](html-mini-apps/dev-tools/code-formatter.html) | Code Formatter |
| [code-runner.html](html-mini-apps/dev-tools/code-runner.html) | Code Runner |
| [cron-generator.html](html-mini-apps/dev-tools/cron-generator.html) | Cron Expression Generator |
| [curl-generator.html](html-mini-apps/dev-tools/curl-generator.html) | cURL Generator |
| [fake-data-generator.html](html-mini-apps/dev-tools/fake-data-generator.html) | Fake Data Generator |
| [git-commands.html](html-mini-apps/dev-tools/git-commands.html) | Git Commands Cheatsheet |
| [hash-checker.html](html-mini-apps/dev-tools/hash-checker.html) | Hash Checker |
| [hash-generator.html](html-mini-apps/dev-tools/hash-generator.html) | Hash Generator |
| [html-entities.html](html-mini-apps/dev-tools/html-entities.html) | HTML Entities Encoder/Decoder |
| [image-compressor-web.html](html-mini-apps/dev-tools/image-compressor-web.html) | Image Compressor |
| [image-optimizer.html](html-mini-apps/dev-tools/image-optimizer.html) | Image Optimizer |
| [ip-lookup.html](html-mini-apps/dev-tools/ip-lookup.html) | IP Lookup Tool |
| [json-formatter.html](html-mini-apps/dev-tools/json-formatter.html) | JSON Formatter & Validator |
| [json-path.html](html-mini-apps/dev-tools/json-path.html) | JSONPath Query |
| [json-validator.html](html-mini-apps/dev-tools/json-validator.html) | JSON Validator |
| [lorem-generator.html](html-mini-apps/dev-tools/lorem-generator.html) | Lorem Ipsum Generator |
| [lorem-ipsum.html](html-mini-apps/dev-tools/lorem-ipsum.html) | Lorem Ipsum Generator |
| [markdown-preview.html](html-mini-apps/dev-tools/markdown-preview.html) | Markdown Preview |
| [markdown-table.html](html-mini-apps/dev-tools/markdown-table.html) | Markdown Table Generator |
| [mathjax-renderer.html](html-mini-apps/dev-tools/mathjax-renderer.html) | MathJax Renderer |
| [password-meter.html](html-mini-apps/dev-tools/password-meter.html) | Password Strength Meter |
| [password-strength.html](html-mini-apps/dev-tools/password-strength.html) | Password Strength Checker |
| [pdf-viewer.html](html-mini-apps/dev-tools/pdf-viewer.html) | PDF Viewer |
| [qr-generator.html](html-mini-apps/dev-tools/qr-generator.html) | QR Code Generator |
| [qr-scanner.html](html-mini-apps/dev-tools/qr-scanner.html) | QR Scanner |
| [query-builder.html](html-mini-apps/dev-tools/query-builder.html) | SQL Query Builder |
| [regex-playground.html](html-mini-apps/dev-tools/regex-playground.html) | Regex Playground |
| [regex-tester.html](html-mini-apps/dev-tools/regex-tester.html) | Regex Tester & Visualizer |
| [slug-checker.html](html-mini-apps/dev-tools/slug-checker.html) | Slug Checker |
| [slug-generator.html](html-mini-apps/dev-tools/slug-generator.html) | Slug Generator |
| [syntax-highlighter.html](html-mini-apps/dev-tools/syntax-highlighter.html) | Syntax Highlighter |
| [table-generator.html](html-mini-apps/dev-tools/table-generator.html) | Table Generator |
| [textarea-enhancer.html](html-mini-apps/dev-tools/textarea-enhancer.html) | Textarea Enhancer |
| [timestamp-converter.html](html-mini-apps/dev-tools/timestamp-converter.html) | Timestamp Converter |
| [timezoneConverter.html](html-mini-apps/dev-tools/timezoneConverter.html) | Timezone Converter |
| [tip-calculator.html](html-mini-apps/dev-tools/tip-calculator.html) | Tip Calculator |
| [unit-converter.html](html-mini-apps/dev-tools/unit-converter.html) | Unit Converter & Calculator |
| [url-encoder.html](html-mini-apps/dev-tools/url-encoder.html) | URL Encoder/Decoder |
| [uuid-generator.html](html-mini-apps/dev-tools/uuid-generator.html) | UUID Generator |
| [word-counter.html](html-mini-apps/dev-tools/word-counter.html) | Word Counter & Text Analyzer |
| [breakout-game.html](html-mini-apps/games/breakout-game.html) | Neon Breakout |
| [coin-flip.html](html-mini-apps/games/coin-flip.html) | Coin Flip Simulator |
| [cookie-clicker.html](html-mini-apps/games/cookie-clicker.html) | Cookie Clicker |
| [dice-roller.html](html-mini-apps/games/dice-roller.html) | Virtual Dice Roller |
| [guess-number.html](html-mini-apps/games/guess-number.html) | AI Number Guess - Voice Powered |
| [minesweeper.html](html-mini-apps/games/minesweeper.html) | Minesweeper |
| [random-picker.html](html-mini-apps/games/random-picker.html) | Random Picker |
| [random-string.html](html-mini-apps/games/random-string.html) | Random String Generator |
| [random-team.html](html-mini-apps/games/random-team.html) | Random Team Generator |
| [random-winner.html](html-mini-apps/games/random-winner.html) | Random Winner Selector |
| [sudoku.html](html-mini-apps/games/sudoku.html) | Sudoku |
| [tower-blocks.html](html-mini-apps/games/tower-blocks.html) | Tower Blocks |
| [countdown.html](html-mini-apps/productivity/countdown.html) | Countdown Timer |
| [daily-planner.html](html-mini-apps/productivity/daily-planner.html) | Daily Planner |
| [focus-mode.html](html-mini-apps/productivity/focus-mode.html) | Focus Mode |
| [goal-setter.html](html-mini-apps/productivity/goal-setter.html) | Goal Setter |
| [habit-tracker.html](html-mini-apps/productivity/habit-tracker.html) | Habit Tracker |
| [image-slideshow.html](html-mini-apps/productivity/image-slideshow.html) | Image Slideshow |
| [mind-map.html](html-mini-apps/productivity/mind-map.html) | Mind Map Creator |
| [music-player.html](html-mini-apps/productivity/music-player.html) | Music Player |
| [notes-app.html](html-mini-apps/productivity/notes-app.html) | Notes |
| [pomodoro-advanced.html](html-mini-apps/productivity/pomodoro-advanced.html) | Advanced Pomodoro Timer |
| [pomodoro-timer.html](html-mini-apps/productivity/pomodoro-timer.html) | Pomodoro Timer |
| [stopwatch.html](html-mini-apps/productivity/stopwatch.html) | Stopwatch |
| [todo-list.html](html-mini-apps/productivity/todo-list.html) | Todo List |
| [whiteboard.html](html-mini-apps/productivity/whiteboard.html) | Whiteboard |

## Notes

The security tools are for learning and for testing your own machines only. There's a longer disclaimer in [docs/security-tools-overview.md](docs/security-tools-overview.md).

Licensed under MIT, see [LICENSE](LICENSE).
