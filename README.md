# MY-PROJECTS

389 projects, each in its own numbered folder. Most are small: a Flask app, a PDF tool, a browser game, built to see how something works and then left as it was.

The bigger work has its own repos:

- [DESIGN-THINKING-](https://github.com/ramnivasattanti2008-cloud/DESIGN-THINKING-): Bharat Scam X, scam detection for Indian-language messaging, with the paper and a working app
- [smriti-ai](https://github.com/ramnivasattanti2008-cloud/smriti-ai)
- [FINAL-SIH](https://github.com/ramnivasattanti2008-cloud/FINAL-SIH)
- [VOJAS](https://github.com/ramnivasattanti2008-cloud/VOJAS)
- [AVISHKAR-](https://github.com/ramnivasattanti2008-cloud/AVISHKAR-)
- [ai-portfolio-projects](https://github.com/ramnivasattanti2008-cloud/ai-portfolio-projects): 15 AI projects

## How it's laid out

Folders are numbered twice. The two digits are the category, the three digits are the project, counted straight through from 001. So `01-ai-llm-apps/001-ai-chatbot` is project 001, and nothing shares a number.

| Cat | Category | Projects | Numbers |
|---|---|---|---|
| 01 | [AI and LLM apps](#01-ai-and-llm-apps) | 52 | 001 to 052 |
| 02 | [Flask apps](#02-flask-apps) | 53 | 053 to 105 |
| 03 | [Django apps](#03-django-apps) | 5 | 106 to 110 |
| 04 | [FastAPI apps](#04-fastapi-apps) | 8 | 111 to 118 |
| 05 | [Node and Express](#05-node-and-express) | 12 | 119 to 130 |
| 06 | [React apps](#06-react-apps) | 25 | 131 to 155 |
| 07 | [Next.js apps](#07-nextjs-apps) | 6 | 156 to 161 |
| 08 | [Streamlit apps](#08-streamlit-apps) | 1 | 162 to 162 |
| 09 | [Data science and analytics](#09-data-science-and-analytics) | 33 | 163 to 195 |
| 10 | [Python utilities](#10-python-utilities) | 62 | 196 to 257 |
| 11 | [Security and network tools](#11-security-and-network-tools) | 14 | 258 to 271 |
| 12 | [Fun and games](#12-fun-and-games) | 24 | 272 to 295 |
| 13 | [HTML mini apps](#13-html-mini-apps) | 94 | 296 to 389 |

## Running a project

Open the project's own README. The usual routes:

```bash
# Python
cd 02-flask-apps/053-flask-todo
pip install -r requirements.txt
python app.py

# Node, React, Next.js
cd 07-nextjs-apps/xxx-nextjs-blog
npm install
npm run dev
```

AI apps need an API key. Set it as an environment variable as the README says, never in the code. The HTML apps need nothing, just open them in a browser.

## Index

### 01 AI and LLM apps

Small apps built on Gemini and similar APIs: chatbots, writing helpers, summarisers, interview prep.

| # | Project | What it does |
|---|---|---|
| 001 | [ai-chatbot](01-ai-llm-apps/001-ai-chatbot) | A simple conversational AI chatbot powered by Google Gemini. |
| 002 | [sql-generator](01-ai-llm-apps/002-sql-generator) | Transform natural language descriptions into SQL queries using AI. |
| 003 | [code-reviewer](01-ai-llm-apps/003-code-reviewer) | AI-powered code review tool that analyzes your code and provides feedback. |
| 004 | [study-buddy](01-ai-llm-apps/004-study-buddy) | Your AI-powered study assistant for learning any topic. |
| 005 | [meeting-summarizer](01-ai-llm-apps/005-meeting-summarizer) | AI-powered tool to summarize meeting notes, extract action items, and generate formal minutes. |
| 006 | [image-generator](01-ai-llm-apps/006-image-generator) | Transform your text ideas into detailed image prompts using Google Gemini AI. |
| 007 | [translator](01-ai-llm-apps/007-translator) | Intelligent text translation with automatic language detection using Google Gemini AI. |
| 008 | [flashcard-maker](01-ai-llm-apps/008-flashcard-maker) | Create study flashcards from any topic using Google Gemini AI. |
| 009 | [bug-detector](01-ai-llm-apps/009-bug-detector) | Find and fix bugs in your Python code using Google Gemini AI. |
| 010 | [todo-prioritizer](01-ai-llm-apps/010-todo-prioritizer) | AI-powered task prioritization that analyzes your tasks and explains the reasoning. |
| 011 | [tweet-generator](01-ai-llm-apps/011-tweet-generator) | Generate engaging, AI-powered tweets with hashtag suggestions. |
| 012 | [resume-builder](01-ai-llm-apps/012-resume-builder) | Generate professional, ATS-friendly resume bullet points instantly. |
| 013 | [youtube-shorts-script](01-ai-llm-apps/013-youtube-shorts-script) | Create engaging YouTube Shorts scripts with hook, body, and CTA sections. |
| 014 | [calorie-counter](01-ai-llm-apps/014-calorie-counter) | Estimate calories in your meals and get healthier alternatives. |
| 015 | [interview-prep](01-ai-llm-apps/015-interview-prep) | Generate AI-powered interview questions and sample answers for any role. |
| 016 | [code-explainer](01-ai-llm-apps/016-code-explainer) | An AI-powered tool that explains any code snippet line by line using Google's Gemini API. |
| 017 | [sql-query-builder](01-ai-llm-apps/017-sql-query-builder) | An AI-powered tool that converts natural language descriptions into SQL queries using Google's Gemini API. |
| 018 | [blog-post-writer](01-ai-llm-apps/018-blog-post-writer) | An AI-powered tool that generates professional blog post outlines with structure, content ideas, and SEO... |
| 019 | [product-review-summarizer](01-ai-llm-apps/019-product-review-summarizer) | An AI-powered tool that analyzes multiple product reviews to extract common themes, sentiment, and... |
| 020 | [git-commit-writer](01-ai-llm-apps/020-git-commit-writer) | An AI-powered tool that generates professional, descriptive git commit messages from your diff output... |
| 021 | [ai-tutor](01-ai-llm-apps/021-ai-tutor) | An AI-powered study companion that generates personalized lessons with key concepts, examples, and quizzes. |
| 022 | [cover-letter-gen](01-ai-llm-apps/022-cover-letter-gen) | AI-powered tool to create compelling, personalized cover letters. |
| 023 | [meeting-notes](01-ai-llm-apps/023-meeting-notes) | Transform messy meeting notes or transcripts into structured, actionable summaries. |
| 024 | [code-documenter](01-ai-llm-apps/024-code-documenter) | AI-powered tool that generates comprehensive documentation for your code. |
| 025 | [domain-generator](01-ai-llm-apps/025-domain-generator) | AI-powered startup domain name brainstormer with availability hints. |
| 026 | [ai-interview-prep](01-ai-llm-apps/026-ai-interview-prep) | cd 31-ai-interview-prep |
| 027 | [ai-grammar-check](01-ai-llm-apps/027-ai-grammar-check) | cd 32-ai-grammar-check |
| 028 | [ai-article-summarizer](01-ai-llm-apps/028-ai-article-summarizer) | cd 33-ai-article-summarizer |
| 029 | [ai-chatbot-widget](01-ai-llm-apps/029-ai-chatbot-widget) | cd 34-ai-chatbot-widget |
| 030 | [ai-keyword-researcher](01-ai-llm-apps/030-ai-keyword-researcher) | cd 35-ai-keyword-researcher |
| 031 | [ai-job-desc-analyzer](01-ai-llm-apps/031-ai-job-desc-analyzer) | Analyze job descriptions with AI to identify requirements and get resume improvement suggestions. |
| 032 | [ai-sentence-expander](01-ai-llm-apps/032-ai-sentence-expander) | Transform short phrases into compelling full paragraphs using AI. |
| 033 | [ai-music-lyrics](01-ai-llm-apps/033-ai-music-lyrics) | Generate original song lyrics with AI based on mood, theme, and genre. |
| 034 | [ai-mcq-generator](01-ai-llm-apps/034-ai-mcq-generator) | Generate multiple choice questions instantly for any topic with AI. |
| 035 | [ai-bio-generator](01-ai-llm-apps/035-ai-bio-generator) | Create catchy social media bios for any profession using AI. |
| 036 | [ai-outliner](01-ai-llm-apps/036-ai-outliner) | Transform any topic into a structured, compelling outline for essays, articles, and blog posts. |
| 037 | [ai-scheduler](01-ai-llm-apps/037-ai-scheduler) | Let AI create optimal daily schedules based on your tasks, available time, and energy levels. |
| 038 | [ai-deck-slides](01-ai-llm-apps/038-ai-deck-slides) | Generate professional PowerPoint slide content outlines for any presentation topic. |
| 039 | [ai-linkedin-post](01-ai-llm-apps/039-ai-linkedin-post) | Create engaging, viral-worthy LinkedIn posts with AI-powered content generation. |
| 040 | [ai-email-reply](01-ai-llm-apps/040-ai-email-reply) | Get professional email response suggestions for any received email. |
| 041 | [ai-dungeon](01-ai-llm-apps/041-ai-dungeon) | An interactive text adventure game powered by Google Gemini where your choices shape the story. Every... |
| 042 | [bio-writer](01-ai-llm-apps/042-bio-writer) | Craft perfect LinkedIn and Twitter bios in seconds with AI. Enter your professional details and get... |
| 043 | [caption-generator](01-ai-llm-apps/043-caption-generator) | Create viral-worthy captions for any image. Upload a photo or describe it, and get engaging captions for... |
| 044 | [content-calendar](01-ai-llm-apps/044-content-calendar) | Plan, schedule, and track your social media content. Manage posts across platforms and monitor engagement... |
| 045 | [hashtag-generator](01-ai-llm-apps/045-hashtag-generator) | AI-powered hashtag suggestions for social media posts. Get trending and relevant hashtags tailored to your... |
| 046 | [jarvis](01-ai-llm-apps/046-jarvis) | Local LLM via Ollama + Open Interpreter for controlling this PC + offline voice + optional Open WebUI. |
| 047 | [linkedin-post-generator](01-ai-llm-apps/047-linkedin-post-generator) | Create engaging, viral-worthy LinkedIn posts with AI. Perfect for professionals, entrepreneurs, and... |
| 048 | [pickup-lines](01-ai-llm-apps/048-pickup-lines) | A fun, creative tool powered by Google Gemini that generates witty, charming, and sometimes cheesy pickup... |
| 049 | [poem-generator](01-ai-llm-apps/049-poem-generator) | A creative poetry app powered by Google Gemini that transforms emotions and themes into beautiful,... |
| 050 | [recipe-generator](01-ai-llm-apps/050-recipe-generator) | A smart cooking assistant powered by Google Gemini that creates delicious recipes based on ingredients you... |
| 051 | [story-generator](01-ai-llm-apps/051-story-generator) | An interactive storytelling app powered by Google Gemini AI that crafts unique short stories based on your... |
| 052 | [translator-cli](01-ai-llm-apps/052-translator-cli) | A Python command-line tool for translating text between languages using Google Translate. |

### 02 Flask apps

Little web apps: todo lists, blogs, forums, dashboards, URL shorteners.

| # | Project | What it does |
|---|---|---|
| 053 | [api-dashboard](02-flask-apps/053-api-dashboard) | A Flask-based dashboard to manage API keys and monitor API usage statistics. |
| 054 | [blog-flask](02-flask-apps/054-blog-flask) | A minimalist blog with markdown support and commenting system. |
| 055 | [blog-site](02-flask-apps/055-blog-site) | A Flask-based blog with posts, comments, markdown support, and tags. |
| 056 | [blog-template](02-flask-apps/056-blog-template) | A complete blog application with posts, categories, tags, comments, and Markdown support. |
| 057 | [bookmarks-app](02-flask-apps/057-bookmarks-app) | A Flask application to save, organize, and search bookmarks with tags and notes. |
| 058 | [css-generators](02-flask-apps/058-css-generators) | A Flask web application with 5 CSS generator tools for developers. |
| 059 | [ecommerce-starter](02-flask-apps/059-ecommerce-starter) | A complete e-commerce application with products, cart, and checkout flow. |
| 060 | [flask-api](02-flask-apps/060-flask-api) | REST API template with CRUD operations and JWT authentication ready. |
| 061 | [flask-auth](02-flask-apps/061-flask-auth) | Authentication template with login, register, logout, and session management. |
| 062 | [flask-blog](02-flask-apps/062-flask-blog) | A Flask blog application with markdown support and comments. |
| 063 | [flask-bookmarks](02-flask-apps/063-flask-bookmarks) | A bookmark manager with tags and search functionality. |
| 064 | [flask-budget](02-flask-apps/064-flask-budget) | A Flask application to set monthly budgets and track expenses. |
| 065 | [flask-cms](02-flask-apps/065-flask-cms) | Simple CMS with pages, posts, and basic admin panel. |
| 066 | [flask-contacts](02-flask-apps/066-flask-contacts) | A simple Flask application to store and manage your contacts. |
| 067 | [flask-dashboard](02-flask-apps/067-flask-dashboard) | A dark-themed admin dashboard template built with Flask. |
| 068 | [flask-ecommerce](02-flask-apps/068-flask-ecommerce) | E-commerce starter with products, cart, and checkout flow. |
| 069 | [flask-events](02-flask-apps/069-flask-events) | An event management application with RSVP functionality and calendar view. |
| 070 | [flask-expenses](02-flask-apps/070-flask-expenses) | A Flask app to log expenses and view summaries by category. |
| 071 | [flask-forum](02-flask-apps/071-flask-forum) | A simple forum application with threads, replies, and categories. |
| 072 | [flask-gallery](02-flask-apps/072-flask-gallery) | A simple image gallery application with categories. |
| 073 | [flask-inventory](02-flask-apps/073-flask-inventory) | A Flask application to track inventory items, quantities, and stock levels. |
| 074 | [flask-landing](02-flask-apps/074-flask-landing) | A modern SaaS landing page template with hero, features, pricing, and contact sections. |
| 075 | [flask-links](02-flask-apps/075-flask-links) | A simple Flask app to save and organize links with tags. |
| 076 | [flask-notes](02-flask-apps/076-flask-notes) | A Flask notes application with tags support using SQLite. |
| 077 | [flask-notes-api](02-flask-apps/077-flask-notes-api) | A RESTful notes API built with Flask, featuring full CRUD operations and SQLite storage. |
| 078 | [flask-pastebin](02-flask-apps/078-flask-pastebin) | A code pastebin with syntax highlighting, expiration options, and password protection. |
| 079 | [flask-poll](02-flask-apps/079-flask-poll) | A simple polling application built with Flask and SQLite. |
| 080 | [flask-quiz](02-flask-apps/080-flask-quiz) | An interactive quiz application using the Open Trivia Database API with score tracking and leaderboards. |
| 081 | [flask-reading](02-flask-apps/081-flask-reading) | A Flask application to track your reading progress across books. |
| 082 | [flask-recipes](02-flask-apps/082-flask-recipes) | A Flask app to store and browse recipes with ingredients and instructions. |
| 083 | [flask-scheduler](02-flask-apps/083-flask-scheduler) | A simple task scheduling application built with Flask and SQLite. |
| 084 | [flask-tasks](02-flask-apps/084-flask-tasks) | A Flask app to track tasks with priorities and due dates. |
| 085 | [flask-todo](02-flask-apps/085-flask-todo) | A simple Flask todo application with SQLite database. |
| 086 | [flask-url-shortener](02-flask-apps/086-flask-url-shortener) | A modern URL shortener with custom short codes, click tracking, and analytics dashboard. |
| 087 | [flask-wiki](02-flask-apps/087-flask-wiki) | A dark-themed collaborative wiki built with Flask and Markdown. |
| 088 | [landing-page](02-flask-apps/088-landing-page) | A modern, dark-themed landing page template built with Flask. |
| 089 | [microblog](02-flask-apps/089-microblog) | A Flask-based microblog platform with user authentication, following system, and likes. |
| 090 | [news-aggregator](02-flask-apps/090-news-aggregator) | A news reader application using Flask and NewsAPI.org. |
| 091 | [password-vault](02-flask-apps/091-password-vault) | A Flask application for securely storing passwords with Fernet encryption. |
| 092 | [paste-bin](02-flask-apps/092-paste-bin) | A Flask-based pastebin with syntax highlighting, expiration options, and password protection. |
| 093 | [paste-bin-flask](02-flask-apps/093-paste-bin-flask) | A code/text pastebin with syntax highlighting powered by Highlight.js. |
| 094 | [pastebin](02-flask-apps/094-pastebin) | A Flask-based code/text pastebin with syntax highlighting, expiration, and password protection. |
| 095 | [portfolio-site](02-flask-apps/095-portfolio-site) | A modern, dark-themed portfolio template built with Flask. |
| 096 | [quiz-api-flask](02-flask-apps/096-quiz-api-flask) | A trivia quiz application that fetches questions from the Open Trivia Database API. |
| 097 | [quiz-app](02-flask-apps/097-quiz-app) | A Flask-based quiz application with multiple categories, difficulty levels, and leaderboards. |
| 098 | [quiz-game](02-flask-apps/098-quiz-game) | A Flask quiz game that fetches trivia questions from the Open Trivia Database API. |
| 099 | [recipe-app](02-flask-apps/099-recipe-app) | A Flask-based recipe management application with search, categories, and ratings. |
| 100 | [saas-starter](02-flask-apps/100-saas-starter) | A complete SaaS application starter template with authentication, dashboard, billing, and API key management. |
| 101 | [sql-playground](02-flask-apps/101-sql-playground) | A Flask web application for running SQL queries on SQLite databases with a user-friendly interface. |
| 102 | [todo-api](02-flask-apps/102-todo-api) | A Flask REST API for managing todos with filtering, search, and bulk operations. |
| 103 | [todo-api-flask](02-flask-apps/103-todo-api-flask) | A RESTful API for managing a todo list with full CRUD operations. |
| 104 | [url-shortener](02-flask-apps/104-url-shortener) | A Flask-based URL shortener with SQLite database, click tracking, and analytics. |
| 105 | [url-shortener-flask](02-flask-apps/105-url-shortener-flask) | A simple URL shortener with click tracking and analytics dashboard. |

### 03 Django apps

Blog, wiki, e-commerce and social starters.

| # | Project | What it does |
|---|---|---|
| 106 | [django-blog](03-django-apps/106-django-blog) | A clean, minimal blog application built with Django. |
| 107 | [django-ecommerce](03-django-apps/107-django-ecommerce) | A starter e-commerce application with products, cart, and checkout. |
| 108 | [django-social](03-django-apps/108-django-social) | A social networking application with user profiles and follow system. |
| 109 | [django-todo](03-django-apps/109-django-todo) | A task management application with user authentication. |
| 110 | [django-wiki](03-django-apps/110-django-wiki) | A collaborative wiki application with markdown support and version history. |

### 04 FastAPI apps

REST APIs with auth, CRUD and file handling.

| # | Project | What it does |
|---|---|---|
| 111 | [fastapi-auth](04-fastapi-apps/111-fastapi-auth) | A complete Authentication API built with FastAPI, featuring JWT tokens, protected routes, and role-based... |
| 112 | [fastapi-blog](04-fastapi-apps/112-fastapi-blog) | A complete Blog API built with FastAPI and SQLite, featuring posts, comments, categories, and pagination. |
| 113 | [fastapi-crud](04-fastapi-apps/113-fastapi-crud) | A simple FastAPI CRUD API for managing tasks with SQLite database. |
| 114 | [fastapi-file](04-fastapi-apps/114-fastapi-file) | A comprehensive file upload/download service built with FastAPI, featuring metadata management, search,... |
| 115 | [fastapi-todo](04-fastapi-apps/115-fastapi-todo) | A simple and elegant Todo API built with FastAPI and SQLite. |
| 116 | [fastapi-weather](04-fastapi-apps/116-fastapi-weather) | A free weather API that proxies Open-Meteo. No API key required. |
| 117 | [graphql-api](04-fastapi-apps/117-graphql-api) | A Python GraphQL API using Strawberry for managing books. |
| 118 | [websockets-chat](04-fastapi-apps/118-websockets-chat) | A simple real-time chat server using FastAPI WebSockets. |

### 05 Node and Express

Backend services and realtime chat.

| # | Project | What it does |
|---|---|---|
| 119 | [auth-api](05-node-express-apis/119-auth-api) | A secure authentication API with JWT tokens and bcrypt password hashing. |
| 120 | [express-notes-api](05-node-express-apis/120-express-notes-api) | A RESTful notes API built with Express.js, storing notes in a JSON file. |
| 121 | [express-rest](05-node-express-apis/121-express-rest) | A simple Express.js REST API for managing posts with middleware examples, error handling, and pagination. |
| 122 | [file-upload-api](05-node-express-apis/122-file-upload-api) | Express API for uploading, listing, and managing files. |
| 123 | [node-chat](05-node-express-apis/123-node-chat) | A real-time chat application built with Express.js and Socket.IO. |
| 124 | [node-file-upload](05-node-express-apis/124-node-file-upload) | An Express.js file upload application with Multer. |
| 125 | [node-pastebin](05-node-express-apis/125-node-pastebin) | A simple Express.js code pastebin with syntax highlighting using highlight.js. |
| 126 | [node-todo-api](05-node-express-apis/126-node-todo-api) | A RESTful Todo API with JWT authentication built with Express.js and SQLite. |
| 127 | [node-url-shortener](05-node-express-apis/127-node-url-shortener) | A simple Express.js URL shortener with SQLite database. |
| 128 | [notes-api](05-node-express-apis/128-notes-api) | A RESTful API for managing notes with CRUD operations, search, and categories. |
| 129 | [proxy-api](05-node-express-apis/129-proxy-api) | Express proxy service to bypass CORS restrictions when calling external APIs. |
| 130 | [url-api](05-node-express-apis/130-url-api) | Express API for creating short URLs and tracking visits. |

### 06 React apps

Components and small front-end apps.

| # | Project | What it does |
|---|---|---|
| 131 | [chat-room](06-react-apps/131-chat-room) | A real-time multi-room chat application built with Flask-SocketIO and React. |
| 132 | [code-paste](06-react-apps/132-code-paste) | A code sharing site with syntax highlighting. Paste code, get a shareable link, and view with beautiful... |
| 133 | [flask-portfolio](06-react-apps/133-flask-portfolio) | A sleek dark-themed portfolio template built with Flask and Bootstrap. |
| 134 | [link-collector](06-react-apps/134-link-collector) | A link bookmarking and organization app. Save URLs with titles, descriptions, and tags. Search, filter,... |
| 135 | [mini-twitter](06-react-apps/135-mini-twitter) | A lightweight Twitter clone with tweets, follows, likes, and a social feed. |
| 136 | [modal-portal](06-react-apps/136-modal-portal) | A fully-featured modal component with React Portal, backdrop, focus trap, and keyboard support. |
| 137 | [poll-app](06-react-apps/137-poll-app) | A live polling application with real-time result updates. Create polls, vote, and watch results update... |
| 138 | [react-calculator](06-react-apps/138-react-calculator) | A modern calculator app built with React and TypeScript, featuring a sleek dark theme and full keyboard... |
| 139 | [react-emoji-picker](06-react-apps/139-react-emoji-picker) | A sleek, dark-themed emoji picker component built with React and TypeScript. |
| 140 | [react-meme](06-react-apps/140-react-meme) | Create memes with top and bottom text and download as PNG. |
| 141 | [react-music-player](06-react-apps/141-react-music-player) | A sleek, dark-themed music player built with React and TypeScript. |
| 142 | [react-notes](06-react-apps/142-react-notes) | A minimal notes app with localStorage persistence. |
| 143 | [react-qr](06-react-apps/143-react-qr) | Generate QR codes from text or URLs and download as PNG. |
| 144 | [react-quiz](06-react-apps/144-react-quiz) | An interactive quiz application with multiple choice questions, score tracking, and detailed explanations. |
| 145 | [react-random-quote](06-react-apps/145-react-random-quote) | A beautiful, dark-themed random quote generator built with React and TypeScript. |
| 146 | [react-random-user](06-react-apps/146-react-random-user) | A React application that fetches and displays random user profiles from the RandomUser.me API. |
| 147 | [react-stopwatch](06-react-apps/147-react-stopwatch) | A sleek, dark-themed stopwatch app built with React and TypeScript. |
| 148 | [react-timer](06-react-apps/148-react-timer) | A sleek countdown timer built with React. |
| 149 | [react-todo](06-react-apps/149-react-todo) | A feature-rich todo application with localStorage persistence, categories, filtering, and dark/light theme... |
| 150 | [react-todo-list](06-react-apps/150-react-todo-list) | A polished, feature-rich Todo List React component with local storage persistence. |
| 151 | [react-weather](06-react-apps/151-react-weather) | A weather app using the Open-Meteo API with geocoding support. |
| 152 | [react-weather-app](06-react-apps/152-react-weather-app) | A beautiful weather application that fetches real-time weather data using the Open-Meteo API (free, no API... |
| 153 | [react-weather-widget](06-react-apps/153-react-weather-widget) | A sleek, dark-themed weather widget built with React and TypeScript. |
| 154 | [search-autocomplete](06-react-apps/154-search-autocomplete) | A fully-featured search input with autocomplete dropdown, debounced API calls, keyboard navigation, and... |
| 155 | [todo-context](06-react-apps/155-todo-context) | A complete React todo application with CRUD operations, localStorage persistence, and filter functionality. |

### 07 Next.js apps

Blog, dashboard, store, landing page, portfolio and a SaaS starter.

| # | Project | What it does |
|---|---|---|
| 156 | [nextjs-blog](07-nextjs-apps/156-nextjs-blog) | A modern, dark-themed blog template built with Next.js 15, TypeScript, MDX, and Tailwind CSS. |
| 157 | [nextjs-dashboard](07-nextjs-apps/157-nextjs-dashboard) | A modern, dark-themed admin dashboard template built with Next.js 15, TypeScript, Tailwind CSS, and Lucide... |
| 158 | [nextjs-ecommerce](07-nextjs-apps/158-nextjs-ecommerce) | A modern, dark-themed e-commerce template built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons. |
| 159 | [nextjs-landing](07-nextjs-apps/159-nextjs-landing) | A modern, dark-themed landing page template built with Next.js 15, TypeScript, and Tailwind CSS. |
| 160 | [nextjs-portfolio](07-nextjs-apps/160-nextjs-portfolio) | A modern, dark-themed portfolio website built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons. |
| 161 | [portfolio](07-nextjs-apps/161-portfolio) | A world-class portfolio website for Attanti Ramnivas, AI/ML Developer and B.Tech CSBS Student. |

### 08 Streamlit apps

Quick data and recipe apps.

| # | Project | What it does |
|---|---|---|
| 162 | [markdown-editor](08-streamlit-apps/162-markdown-editor) | A Streamlit application for writing Markdown with live preview and HTML export. |

### 09 Data science and analytics

Classifiers, predictors, CSV tools and charts.

| # | Project | What it does |
|---|---|---|
| 163 | [budget-tracker](09-data-science-and-analytics/163-budget-tracker) | A dark-themed budget tracking application with charts and savings goals. |
| 164 | [covid-tracker](09-data-science-and-analytics/164-covid-tracker) | A real-time COVID-19 statistics dashboard built with Streamlit and Plotly. |
| 165 | [cricket-analysis](09-data-science-and-analytics/165-cricket-analysis) | A comprehensive Streamlit application for analyzing cricket player statistics with interactive visualizations. |
| 166 | [cricket-stats](09-data-science-and-analytics/166-cricket-stats) | An interactive dashboard to explore cricket player stats, team rankings, and match data. |
| 167 | [crypto-tracker](09-data-science-and-analytics/167-crypto-tracker) | A real-time cryptocurrency price tracker using Flask and the CoinGecko API. |
| 168 | [csv-analyzer](09-data-science-and-analytics/168-csv-analyzer) | A Python utility for comprehensive analysis of CSV files with statistical summaries, data quality... |
| 169 | [csv-visualizer](09-data-science-and-analytics/169-csv-visualizer) | Generate interactive charts and visualizations from CSV data. |
| 170 | [data-cleaner](09-data-science-and-analytics/170-data-cleaner) | Clean messy CSV data by removing duplicates, fixing encoding issues, and trimming whitespace. |
| 171 | [data-exporter](09-data-science-and-analytics/171-data-exporter) | A command-line tool for exporting SQLite databases to JSON, CSV, SQL dump, or NDJSON formats. |
| 172 | [diabetes-predictor](09-data-science-and-analytics/172-diabetes-predictor) | A machine learning application that predicts diabetes risk based on health metrics using the Pima Indians... |
| 173 | [digit-recognizer](09-data-science-and-analytics/173-digit-recognizer) | A beginner-friendly machine learning project that recognizes handwritten digits (0-9) using Support Vector... |
| 174 | [exam-grade-analyzer](09-data-science-and-analytics/174-exam-grade-analyzer) | A comprehensive Streamlit application for analyzing student exam results with detailed statistics and... |
| 175 | [excel-to-json](09-data-science-and-analytics/175-excel-to-json) | Convert Excel (.xlsx, .xls) and CSV files to JSON with support for multiple sheets. |
| 176 | [expense-simple](09-data-science-and-analytics/176-expense-simple) | A Streamlit application for tracking personal expenses with visual analytics. |
| 177 | [expense-tracker](09-data-science-and-analytics/177-expense-tracker) | A budget tracking application built with Streamlit and Python. |
| 178 | [football-analysis](09-data-science-and-analytics/178-football-analysis) | A comprehensive Streamlit application for analyzing football/soccer player statistics with interactive... |
| 179 | [git-stats](09-data-science-and-analytics/179-git-stats) | A command-line tool to display GitHub statistics for any user. Shows repositories, stars, languages, and... |
| 180 | [github-profile-stats](09-data-science-and-analytics/180-github-profile-stats) | A Python script that generates visual ASCII art statistics for any GitHub profile. Display commits,... |
| 181 | [grade-calculator](09-data-science-and-analytics/181-grade-calculator) | A comprehensive academic performance tracker with GPA calculation and visualizations. |
| 182 | [house-price-predictor](09-data-science-and-analytics/182-house-price-predictor) | A beginner-friendly machine learning project that predicts house prices using Linear Regression. |
| 183 | [iris-classifier](09-data-science-and-analytics/183-iris-classifier) | A beginner-friendly machine learning project that classifies iris flowers into three species based on... |
| 184 | [json-to-excel](09-data-science-and-analytics/184-json-to-excel) | Convert JSON data to Excel (.xlsx) files with formatting and nested structure support. |
| 185 | [movie-recommender](09-data-science-and-analytics/185-movie-recommender) | A Python CLI application that recommends movies based on your genre preferences. Features ASCII art... |
| 186 | [population-viz](09-data-science-and-analytics/186-population-viz) | An interactive dashboard to explore global population data. |
| 187 | [reading-list](09-data-science-and-analytics/187-reading-list) | Track your reading journey with a beautiful book manager. |
| 188 | [recipe-app-streamlit](09-data-science-and-analytics/188-recipe-app-streamlit) | A clean, dark-themed recipe management application. |
| 189 | [sales-dashboard](09-data-science-and-analytics/189-sales-dashboard) | A comprehensive Streamlit application for analyzing sales data with interactive visualizations and KPIs. |
| 190 | [sentiment-simple](09-data-science-and-analytics/190-sentiment-simple) | A beginner-friendly machine learning project that analyzes the sentiment (positive, negative, or neutral)... |
| 191 | [spam-detector](09-data-science-and-analytics/191-spam-detector) | A beginner-friendly machine learning project that detects spam messages using Naive Bayes classification. |
| 192 | [stock-viz](09-data-science-and-analytics/192-stock-viz) | An interactive stock market visualization dashboard with technical indicators. |
| 193 | [study-tracker](09-data-science-and-analytics/193-study-tracker) | Track your study sessions and visualize progress. |
| 194 | [weather-dashboard](09-data-science-and-analytics/194-weather-dashboard) | A beautiful Streamlit application that displays weather information for multiple cities side by side,... |
| 195 | [weight-tracker](09-data-science-and-analytics/195-weight-tracker) | Track your weight and health metrics with beautiful charts. |

### 10 Python utilities

Command line helpers for files, PDFs, images and text.

| # | Project | What it does |
|---|---|---|
| 196 | [api-docs-generator](10-python-utilities/196-api-docs-generator) | Auto-generate API documentation from Python docstrings. Scans Python files, extracts function signatures,... |
| 197 | [auto-backup](10-python-utilities/197-auto-backup) | A Python script that creates timestamped compressed backups of important folders. |
| 198 | [auto-email-sender](10-python-utilities/198-auto-email-sender) | A Python tool for sending emails via SMTP (Gmail) with support for attachments, HTML content, and email... |
| 199 | [bulk-renamer](10-python-utilities/199-bulk-renamer) | A Python command-line tool for batch renaming files with pattern matching, preview support, and undo... |
| 200 | [clipboard-manager](10-python-utilities/200-clipboard-manager) | Manage clipboard history with save, search, and paste functionality. |
| 201 | [csv-cleaner](10-python-utilities/201-csv-cleaner) | A Python CLI tool for cleaning and standardizing CSV files. |
| 202 | [currency-cmd](10-python-utilities/202-currency-cmd) | A colorful command-line currency converter using free exchange rate APIs. |
| 203 | [currency-converter](10-python-utilities/203-currency-converter) | A Python CLI tool to convert between currencies using free exchange rate APIs. |
| 204 | [data-exporter](10-python-utilities/204-data-exporter) | Data Exporter - Export SQLite database to JSON, CSV, or SQL dump formats. |
| 205 | [data-generator](10-python-utilities/205-data-generator) | A Python CLI tool for generating fake data for testing purposes. |
| 206 | [data-validator](10-python-utilities/206-data-validator) | A Python CLI tool for validating data against common rules and reporting errors. |
| 207 | [db-migrator](10-python-utilities/207-db-migrator) | A Python script for converting data between SQLite databases and CSV files. |
| 208 | [db-migrator-script](10-python-utilities/208-db-migrator-script) | Database Migrator - Convert data between SQLite and CSV formats. |
| 209 | [db-visualizer](10-python-utilities/209-db-visualizer) | A Python script that generates ASCII ER diagrams from SQLite databases. Visualize your database schema,... |
| 210 | [db-visualizer-script](10-python-utilities/210-db-visualizer-script) | Database Visualizer - Generate ASCII ER diagrams from SQLite databases. |
| 211 | [disk-usage](10-python-utilities/211-disk-usage) | Analyze disk usage and visualize largest files and folders with bar charts. |
| 212 | [duplicate-finder](10-python-utilities/212-duplicate-finder) | Find duplicate files by content hash and optionally remove them. |
| 213 | [excel-to-json](10-python-utilities/213-excel-to-json) | A Python CLI tool for converting Excel and CSV files to JSON format. |
| 214 | [file-organizer](10-python-utilities/214-file-organizer) | A Python script that automatically organizes files in a directory by their type into categorized subfolders. |
| 215 | [file-searcher](10-python-utilities/215-file-searcher) | A fast Python command-line tool for searching files by name, content, size, and modification date. |
| 216 | [file-splitter](10-python-utilities/216-file-splitter) | Split large files into manageable chunks and merge them back with verification. |
| 217 | [folder-sync](10-python-utilities/217-folder-sync) | Synchronize two folders by copying new and modified files from source to destination. |
| 218 | [image-batch](10-python-utilities/218-image-batch) | Batch resize, crop, compress, and transform multiple images with a single command. |
| 219 | [image-compressor](10-python-utilities/219-image-compressor) | Reduce image file sizes with configurable JPEG quality, PNG optimization, and batch processing. |
| 220 | [image-converter](10-python-utilities/220-image-converter) | Convert images between formats: JPEG, PNG, WebP, GIF, BMP, TIFF, ICO. Batch conversion supported. |
| 221 | [image-cropper](10-python-utilities/221-image-cropper) | Crop images with interactive selection or CLI using exact coordinates. |
| 222 | [image-metadata](10-python-utilities/222-image-metadata) | A Python utility for extracting and displaying EXIF metadata from images, including camera information,... |
| 223 | [image-resizer](10-python-utilities/223-image-resizer) | Resize images by width, height, or percentage. Supports batch processing of entire directories. |
| 224 | [image-resizer-script](10-python-utilities/224-image-resizer-script) | A Python CLI tool to resize images to different dimensions with batch processing support. |
| 225 | [image-watermark](10-python-utilities/225-image-watermark) | Add text or image watermarks to images with customizable position control. |
| 226 | [json-editor](10-python-utilities/226-json-editor) | An interactive command-line tool for viewing, adding, editing, and deleting keys in JSON files. |
| 227 | [json-to-csv](10-python-utilities/227-json-to-csv) | Python script. Run it with python json-to-csv.py. |
| 228 | [json-to-model](10-python-utilities/228-json-to-model) | Convert JSON data to typed data models in Python, TypeScript, or Go. Perfect for quickly creating... |
| 229 | [mock-api](10-python-utilities/229-mock-api) | A Python Flask-based mock API server. Define endpoints in YAML and serve realistic mock responses. Perfect... |
| 230 | [movie-info](10-python-utilities/230-movie-info) | A command-line tool to look up movie information including ratings, cast, plot, and more. Uses the OMDB API. |
| 231 | [pdf-info](10-python-utilities/231-pdf-info) | Extract metadata and information from PDF files including page count, title, author, and more. |
| 232 | [pdf-merge](10-python-utilities/232-pdf-merge) | Merge multiple PDF files into a single PDF document with optional bookmarks. |
| 233 | [pdf-merger](10-python-utilities/233-pdf-merger) | Merge multiple PDF files into one with support for drag & drop and CLI usage. |
| 234 | [pdf-split](10-python-utilities/234-pdf-split) | Split PDF files into separate pages, page ranges, or chunks. |
| 235 | [pdf-to-images](10-python-utilities/235-pdf-to-images) | Convert PDF pages to images with customizable resolution and format. |
| 236 | [pdf-to-text](10-python-utilities/236-pdf-to-text) | A Python CLI tool to extract text content from PDF files with support for tables and metadata. |
| 237 | [pdf-watermark](10-python-utilities/237-pdf-watermark) | Add text or image watermarks to PDF documents with customizable options. |
| 238 | [qr-batch](10-python-utilities/238-qr-batch) | Generate multiple QR codes from CSV data. Perfect for batch processing URLs, contacts, WiFi credentials,... |
| 239 | [qr-code-reader](10-python-utilities/239-qr-code-reader) | A versatile Python tool for generating and reading QR codes. Supports image files, webcam input, batch... |
| 240 | [qr-generator](10-python-utilities/240-qr-generator) | A Python command-line tool to generate QR codes from text or URLs and save them as PNG images. |
| 241 | [query-builder](10-python-utilities/241-query-builder) | A visual tool for building SQL queries without writing code. Point and click to select tables, columns,... |
| 242 | [quick-notes](10-python-utilities/242-quick-notes) | A fast, terminal-based note-taking application with tagging and search capabilities. |
| 243 | [regex-extractor](10-python-utilities/243-regex-extractor) | A Python utility for extracting emails, phone numbers, URLs, IP addresses, and more from text files or... |
| 244 | [regex-tester](10-python-utilities/244-regex-tester) | Interactive regex pattern testing with highlighted matches and detailed group information. |
| 245 | [screenshot](10-python-utilities/245-screenshot) | Take screenshots - full screen or with interactive region selection. |
| 246 | [screenshot-capture](10-python-utilities/246-screenshot-capture) | Take screenshots on Windows using Pillow and Windows GDI. Full screen, specific monitors, region... |
| 247 | [screenshot-tool](10-python-utilities/247-screenshot-tool) | A Python script for capturing screenshots with hotkey support. Supports full screen and region capture on... |
| 248 | [sql-query-runner](10-python-utilities/248-sql-query-runner) | A Python CLI tool for running SQL queries against CSV files. |
| 249 | [system-info](10-python-utilities/249-system-info) | A Python command-line tool to display comprehensive system information including OS, CPU, RAM, disk space,... |
| 250 | [text-stats](10-python-utilities/250-text-stats) | Analyze text files for statistics, vocabulary metrics, and readability scores. |
| 251 | [text-to-speech](10-python-utilities/251-text-to-speech) | A Python script that converts text to speech using Google Text-to-Speech (gTTS) and saves the result as an... |
| 252 | [todo-cmd](10-python-utilities/252-todo-cmd) | A powerful command-line todo list manager with priorities, due dates, and categories. |
| 253 | [url-checker](10-python-utilities/253-url-checker) | A Python CLI tool to check if URLs are alive, returning status codes and response times. |
| 254 | [video-downloader](10-python-utilities/254-video-downloader) | A powerful YouTube video and audio downloader using the yt-dlp library. |
| 255 | [watermark-tool](10-python-utilities/255-watermark-tool) | Add text or image watermarks to images with full position, opacity, and batch control. |
| 256 | [weather-cli](10-python-utilities/256-weather-cli) | A Python CLI tool to get weather information for any city using the free Open-Meteo API. |
| 257 | [web-scraper](10-python-utilities/257-web-scraper) | A powerful and flexible web scraping tool using Python with requests and BeautifulSoup. Extract structured... |

### 11 Security and network tools

Educational scanners, hashing and encryption tools. Read the disclaimer in docs/.

| # | Project | What it does |
|---|---|---|
| 258 | [cert-checker](11-security-and-network-tools/258-cert-checker) | A Python tool that demonstrates SSL/TLS certificate inspection for learning about web security and HTTPS... |
| 259 | [file-encrypter](11-security-and-network-tools/259-file-encrypter) | A Python utility for encrypting and decrypting files using Fernet symmetric encryption. |
| 260 | [file-hasher](11-security-and-network-tools/260-file-hasher) | Calculate cryptographic hashes (MD5, SHA1, SHA256, SHA512) for any file. |
| 261 | [hash-cracker](11-security-and-network-tools/261-hash-cracker) | A Python tool that demonstrates password hash vulnerabilities through dictionary attacks. |
| 262 | [leak-checker](11-security-and-network-tools/262-leak-checker) | A Python tool that checks if emails or passwords have appeared in known data breaches using the... |
| 263 | [pdf-encrypt](11-security-and-network-tools/263-pdf-encrypt) | Encrypt or decrypt PDF files with password protection and permissions control. |
| 264 | [port-scanner](11-security-and-network-tools/264-port-scanner) | A Python tool that demonstrates network port scanning concepts for learning about network security. |
| 265 | [request-logger](11-security-and-network-tools/265-request-logger) | A browser-based tool to log and inspect HTTP requests. Use the browser's fetch API to make requests and... |
| 266 | [rest-client](11-security-and-network-tools/266-rest-client) | A command-line HTTP client for making API requests with formatted JSON output. |
| 267 | [simple-proxy-api](11-security-and-network-tools/267-simple-proxy-api) | A Flask API that proxies requests to external APIs, helping you avoid CORS issues when building front-end... |
| 268 | [ssh-keygen-tool](11-security-and-network-tools/268-ssh-keygen-tool) | A Python tool that demonstrates SSH key pair generation for learning about public-key cryptography. |
| 269 | [web-server](11-security-and-network-tools/269-web-server) | A simple HTTP web server built entirely with Python's built-in http.server module. No external... |
| 270 | [webhook-tester](11-security-and-network-tools/270-webhook-tester) | A Flask application to receive, store, and display webhook payloads. Useful for testing webhooks during... |
| 271 | [wifi-passwords](11-security-and-network-tools/271-wifi-passwords) | A Windows utility to view saved WiFi passwords stored on your computer. View all saved WiFi networks or... |

### 12 Fun and games

Terminal games and small toys.

| # | Project | What it does |
|---|---|---|
| 272 | [animated-counter](12-fun-and-games/272-animated-counter) | A React component that animates numbers when scrolled into view, with smooth easing and various... |
| 273 | [ascii-art](12-fun-and-games/273-ascii-art) | A fun CLI tool that converts text into beautiful ASCII art with multiple font styles and color support. |
| 274 | [color-detect](12-fun-and-games/274-color-detect) | Upload any image and discover its dominant colors! Perfect for designers, artists, and anyone curious... |
| 275 | [dark-mode-toggle](12-fun-and-games/275-dark-mode-toggle) | A beautiful, animated dark/light mode toggle switch with smooth transitions, stars animation, and sun/moon... |
| 276 | [fortune-cookie](12-fun-and-games/276-fortune-cookie) | A fun virtual fortune cookie that reveals random fortunes with a beautiful ASCII art presentation! |
| 277 | [gif-maker](12-fun-and-games/277-gif-maker) | Create animated GIFs from images with adjustable speed, loop, and resize options. |
| 278 | [hangman](12-fun-and-games/278-hangman) | A classic word guessing game with ASCII art and multiple word categories. |
| 279 | [joke-teller](12-fun-and-games/279-joke-teller) | Get ready to laugh with random jokes and fun facts! Features standard jokes, programming humor, and... |
| 280 | [joke-teller-script](12-fun-and-games/280-joke-teller-script) | Joke Teller - Random Jokes & Facts |
| 281 | [mad-libs](12-fun-and-games/281-mad-libs) | The classic word-filling game brought to life! Create hilarious stories by filling in blanks with funny words. |
| 282 | [mad-libs-script](12-fun-and-games/282-mad-libs-script) | Mad Libs Generator - Classic Word Game |
| 283 | [magic-8ball](12-fun-and-games/283-magic-8ball) | A mystical fortune-telling experience in your terminal! Ask any yes/no question and receive wisdom from... |
| 284 | [magic-8ball-script](12-fun-and-games/284-magic-8ball-script) | Magic 8-Ball - Virtual Fortune Teller |
| 285 | [meme-generator](12-fun-and-games/285-meme-generator) | A fun and easy tool to create memes by adding text to images. Perfect for creating classic memes with top... |
| 286 | [number-guessing](12-fun-and-games/286-number-guessing) | A twist on the classic guessing game where YOU think of a number and the computer tries to guess it! |
| 287 | [quiz-game](12-fun-and-games/287-quiz-game) | A multi-choice quiz game with multiple categories and difficulty levels. Test your knowledge! |
| 288 | [rock-paper-scissors](12-fun-and-games/288-rock-paper-scissors) | The classic game with an epic twist! Challenge the computer in best-of-N rounds with ASCII art, win... |
| 289 | [rock-paper-scissors-script](12-fun-and-games/289-rock-paper-scissors-script) | Rock Paper Scissors - Classic RPS Game |
| 290 | [snake-game](12-fun-and-games/290-snake-game) | A classic arcade snake game built with Python's turtle graphics module. |
| 291 | [text-adventure](12-fun-and-games/291-text-adventure) | A classic text adventure game where you explore a mysterious castle, collect items, solve puzzles, and... |
| 292 | [text-to-ascii](12-fun-and-games/292-text-to-ascii) | Transform any image into stunning ASCII art! Perfect for creating text-based versions of photos, logos,... |
| 293 | [tic-tac-toe](12-fun-and-games/293-tic-tac-toe) | Play against an unbeatable AI opponent using the Minimax algorithm with alpha-beta pruning! |
| 294 | [truth-or-dare](12-fun-and-games/294-truth-or-dare) | The ultimate party game experience! Challenge your friends, uncover secrets, and complete hilarious dares. |
| 295 | [truth-or-dare-script](12-fun-and-games/295-truth-or-dare-script) | Truth or Dare - Classic Party Game |

### 13 HTML mini apps

Single-file browser tools and games. Each has its own folder, open index.html.

| # | Project | What it does |
|---|---|---|
| 296 | [color-blender](13-html-mini-apps/296-color-blender) | Color Blender |
| 297 | [color-contrast](13-html-mini-apps/297-color-contrast) | Color Contrast Checker |
| 298 | [color-mixer](13-html-mini-apps/298-color-mixer) | Color Mixer |
| 299 | [color-palette](13-html-mini-apps/299-color-palette) | Color Palette Extractor |
| 300 | [color-picker-advanced](13-html-mini-apps/300-color-picker-advanced) | Advanced Color Picker |
| 301 | [color-themer](13-html-mini-apps/301-color-themer) | Color Themer |
| 302 | [css-animation](13-html-mini-apps/302-css-animation) | CSS Animation Generator |
| 303 | [css-variables](13-html-mini-apps/303-css-variables) | CSS Variables Generator |
| 304 | [emoji-art](13-html-mini-apps/304-emoji-art) | ASCII Art Generator |
| 305 | [emoji-picker](13-html-mini-apps/305-emoji-picker) | Emoji Picker |
| 306 | [emoji-search](13-html-mini-apps/306-emoji-search) | Emoji Search |
| 307 | [favicon-creator](13-html-mini-apps/307-favicon-creator) | Favicon Creator |
| 308 | [favicon-generator](13-html-mini-apps/308-favicon-generator) | Favicon Generator |
| 309 | [font-pairing](13-html-mini-apps/309-font-pairing) | Font Pairing |
| 310 | [gradient-generator](13-html-mini-apps/310-gradient-generator) | CSS Gradient Generator |
| 311 | [gradient-preview](13-html-mini-apps/311-gradient-preview) | Gradient Preview |
| 312 | [mockup-generator](13-html-mini-apps/312-mockup-generator) | Mockup Generator |
| 313 | [placeholder-generator](13-html-mini-apps/313-placeholder-generator) | Placeholder Generator |
| 314 | [svg-generator](13-html-mini-apps/314-svg-generator) | SVG Generator |
| 315 | [loremgenerator](13-html-mini-apps/315-loremgenerator) | Lorem Ipsum Generator |
| 316 | [api-playground](13-html-mini-apps/316-api-playground) | API Playground |
| 317 | [api-tester](13-html-mini-apps/317-api-tester) | API Tester |
| 318 | [ascii-table](13-html-mini-apps/318-ascii-table) | ASCII Table Generator |
| 319 | [base64-editor](13-html-mini-apps/319-base64-editor) | Base64 Editor |
| 320 | [base64-tool](13-html-mini-apps/320-base64-tool) | Base64 Encoder/Decoder |
| 321 | [binary-clock](13-html-mini-apps/321-binary-clock) | Binary Clock |
| 322 | [binary-decimal](13-html-mini-apps/322-binary-decimal) | Binary-Decimal Converter |
| 323 | [code-diff](13-html-mini-apps/323-code-diff) | Code Diff Tool |
| 324 | [code-formatter](13-html-mini-apps/324-code-formatter) | Code Formatter |
| 325 | [code-runner](13-html-mini-apps/325-code-runner) | Code Runner |
| 326 | [cron-generator](13-html-mini-apps/326-cron-generator) | Cron Expression Generator |
| 327 | [curl-generator](13-html-mini-apps/327-curl-generator) | cURL Generator |
| 328 | [fake-data-generator](13-html-mini-apps/328-fake-data-generator) | Fake Data Generator |
| 329 | [git-commands](13-html-mini-apps/329-git-commands) | Git Commands Cheatsheet |
| 330 | [hash-checker](13-html-mini-apps/330-hash-checker) | Hash Checker |
| 331 | [hash-generator](13-html-mini-apps/331-hash-generator) | Hash Generator |
| 332 | [html-entities](13-html-mini-apps/332-html-entities) | HTML Entities Encoder/Decoder |
| 333 | [image-compressor-web](13-html-mini-apps/333-image-compressor-web) | Image Compressor |
| 334 | [image-optimizer](13-html-mini-apps/334-image-optimizer) | Image Optimizer |
| 335 | [ip-lookup](13-html-mini-apps/335-ip-lookup) | IP Lookup Tool |
| 336 | [json-formatter](13-html-mini-apps/336-json-formatter) | JSON Formatter & Validator |
| 337 | [json-path](13-html-mini-apps/337-json-path) | JSONPath Query |
| 338 | [json-validator](13-html-mini-apps/338-json-validator) | JSON Validator |
| 339 | [lorem-generator](13-html-mini-apps/339-lorem-generator) | Lorem Ipsum Generator |
| 340 | [lorem-ipsum](13-html-mini-apps/340-lorem-ipsum) | Lorem Ipsum Generator |
| 341 | [markdown-preview](13-html-mini-apps/341-markdown-preview) | Markdown Preview |
| 342 | [markdown-table](13-html-mini-apps/342-markdown-table) | Markdown Table Generator |
| 343 | [mathjax-renderer](13-html-mini-apps/343-mathjax-renderer) | MathJax Renderer |
| 344 | [password-meter](13-html-mini-apps/344-password-meter) | Password Strength Meter |
| 345 | [password-strength](13-html-mini-apps/345-password-strength) | Password Strength Checker |
| 346 | [pdf-viewer](13-html-mini-apps/346-pdf-viewer) | PDF Viewer |
| 347 | [qr-generator](13-html-mini-apps/347-qr-generator) | QR Code Generator |
| 348 | [qr-scanner](13-html-mini-apps/348-qr-scanner) | QR Scanner |
| 349 | [query-builder](13-html-mini-apps/349-query-builder) | SQL Query Builder |
| 350 | [regex-playground](13-html-mini-apps/350-regex-playground) | Regex Playground |
| 351 | [regex-tester](13-html-mini-apps/351-regex-tester) | Regex Tester & Visualizer |
| 352 | [slug-checker](13-html-mini-apps/352-slug-checker) | Slug Checker |
| 353 | [slug-generator](13-html-mini-apps/353-slug-generator) | Slug Generator |
| 354 | [syntax-highlighter](13-html-mini-apps/354-syntax-highlighter) | Syntax Highlighter |
| 355 | [table-generator](13-html-mini-apps/355-table-generator) | Table Generator |
| 356 | [textarea-enhancer](13-html-mini-apps/356-textarea-enhancer) | Textarea Enhancer |
| 357 | [timestamp-converter](13-html-mini-apps/357-timestamp-converter) | Timestamp Converter |
| 358 | [timezoneconverter](13-html-mini-apps/358-timezoneconverter) | Timezone Converter |
| 359 | [tip-calculator](13-html-mini-apps/359-tip-calculator) | Tip Calculator |
| 360 | [unit-converter](13-html-mini-apps/360-unit-converter) | Unit Converter & Calculator |
| 361 | [url-encoder](13-html-mini-apps/361-url-encoder) | URL Encoder/Decoder |
| 362 | [uuid-generator](13-html-mini-apps/362-uuid-generator) | UUID Generator |
| 363 | [word-counter](13-html-mini-apps/363-word-counter) | Word Counter & Text Analyzer |
| 364 | [breakout-game](13-html-mini-apps/364-breakout-game) | Neon Breakout |
| 365 | [coin-flip](13-html-mini-apps/365-coin-flip) | Coin Flip Simulator |
| 366 | [cookie-clicker](13-html-mini-apps/366-cookie-clicker) | Cookie Clicker |
| 367 | [dice-roller](13-html-mini-apps/367-dice-roller) | Virtual Dice Roller |
| 368 | [guess-number](13-html-mini-apps/368-guess-number) | AI Number Guess - Voice Powered |
| 369 | [minesweeper](13-html-mini-apps/369-minesweeper) | Minesweeper |
| 370 | [random-picker](13-html-mini-apps/370-random-picker) | Random Picker |
| 371 | [random-string](13-html-mini-apps/371-random-string) | Random String Generator |
| 372 | [random-team](13-html-mini-apps/372-random-team) | Random Team Generator |
| 373 | [random-winner](13-html-mini-apps/373-random-winner) | Random Winner Selector |
| 374 | [sudoku](13-html-mini-apps/374-sudoku) | Sudoku |
| 375 | [tower-blocks](13-html-mini-apps/375-tower-blocks) | Tower Blocks |
| 376 | [countdown](13-html-mini-apps/376-countdown) | Countdown Timer |
| 377 | [daily-planner](13-html-mini-apps/377-daily-planner) | Daily Planner |
| 378 | [focus-mode](13-html-mini-apps/378-focus-mode) | Focus Mode |
| 379 | [goal-setter](13-html-mini-apps/379-goal-setter) | Goal Setter |
| 380 | [habit-tracker](13-html-mini-apps/380-habit-tracker) | Habit Tracker |
| 381 | [image-slideshow](13-html-mini-apps/381-image-slideshow) | Image Slideshow |
| 382 | [mind-map](13-html-mini-apps/382-mind-map) | Mind Map Creator |
| 383 | [music-player](13-html-mini-apps/383-music-player) | Music Player |
| 384 | [notes-app](13-html-mini-apps/384-notes-app) | Notes |
| 385 | [pomodoro-advanced](13-html-mini-apps/385-pomodoro-advanced) | Advanced Pomodoro Timer |
| 386 | [pomodoro-timer](13-html-mini-apps/386-pomodoro-timer) | Pomodoro Timer |
| 387 | [stopwatch](13-html-mini-apps/387-stopwatch) | Stopwatch |
| 388 | [todo-list](13-html-mini-apps/388-todo-list) | Todo List |
| 389 | [whiteboard](13-html-mini-apps/389-whiteboard) | Whiteboard |

## Notes

The security tools are for learning and for testing your own machines only. There's a longer disclaimer in [docs/security-tools-overview.md](docs/security-tools-overview.md).

MIT licensed, see [LICENSE](LICENSE).
