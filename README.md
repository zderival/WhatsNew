# WhatsNew 📰

A command-line news aggregation and personalization platform built in Python. 
WhatsNew lets users browse top headlines, search for articles, save favorites, manage topic preferences, receive AI-powered recommendations, and gain insights into their reading habits.

---

## Features

### Authentication & Security
- Secure user registration and login with **Argon2 password hashing**
- Email and username recovery via **SendGrid email verification with one-time codes**
- Login rate limiting with a **5-minute cooldown after 5 failed attempts** using Python threading
- Age verification during account creation

### News
- Browse **top US headlines** powered by the [NewsAPI](https://newsapi.org/)
- Search articles by keyword
- Save articles to your profile
- Open articles directly in your default web browser
- Track articles that have been read
- Configurable page size for search results
- Articles display title, source, and URL

### Personalization & Recommendations
- Store topic preferences in PostgreSQL for persistent personalization
- Save articles for long-term recommendation history
- **Content-based recommendation engine** built with:
  - **pandas** for article preprocessing
  - **scikit-learn TF-IDF vectorization**
  - **Cosine similarity** for personalized recommendations
- Recommendations adapt based on both user preferences and saved articles
- **Gemini LLM-powered recommendation explanations** summarize why articles were recommended and identify common themes

### Reading Analytics
- Personalized "Wrapped"-style reading summary including:
  - Total Articles read
  - Total Articles saved
  - Favorite news source
  - Most Saved Source from Saved Articles list
  - Most Read Source 
  - Most Searched Keyword
### Profile Management
- Change email (with verification)
- Change password (with verification)
- Change username
- Upload a profile picture
- Delete account
- Forgot password and forgot username flows secured with email verification

### Deployment
- Fully containerized using **Docker** and **Docker Compose**
- Consistent setup across Windows, macOS, and Linux

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Database | PostgreSQL (psycopg2) |
| Machine Learning | pandas, scikit-learn |
| LLM | Google Gemini (google-genai) |
| Password Security | Argon2 |
| News Data | NewsAPI |
| Email | SendGrid |
| Browser Integration | webbrowser |
| Containerization | Docker, Docker Compose |
| Unique IDs | UUID4 |

---

## Project Structure

```text
WhatsNew/
├── main.py
├── Login.py
├── Profile.py
├── NewsManagment.py
├── Recommendations.py
├── LLM_Generation.py      # Gemini recommendation explanations
├── db.py                  # Database helper functions
├── Password_Security.py
├── Email_Maintance.py
├── docker-compose.yml
├── Dockerfile
└── .env
```

---

## Setup & Installation

### Prerequisites

- Docker Desktop
- NewsAPI API Key
- SendGrid API Key
- Google Gemini API Key

### Clone the Repository

```bash
git clone https://github.com/zderival/WhatsNew.git
cd WhatsNew
```

### Environment Variables

Create a `.env` file in the project root.

```env
NEWS_API_KEY=your_newsapi_key
SENDGRID_API_KEY=your_sendgrid_key
GEMINI_API_KEY=your_gemini_api_key

Database_Name=whats_new
Database_Username=postgres
Database_Password=your_password
host=db - for Docker host= localhost - for running local
```

### Run with Docker

Build and start the application.

```bash
docker compose up --build
```

To stop the application:

```bash
docker compose down
```

Docker automatically creates and configures the PostgreSQL database, so no manual SQL setup is required.

---

## Author

**Zachary Derival**

GitHub: https://github.com/zderival