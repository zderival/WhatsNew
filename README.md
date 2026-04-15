# WhatsNew 📰

A command-line news aggregator and personalization platform built in Python. WhatsNew lets users browse top headlines, search for articles, save favorites, set topic preferences, and receive AI-powered article recommendations tailored to their reading habits.

---

## Features

### Authentication & Security
- Secure user registration and login with **Argon2 password hashing**
- Email and username recovery via **SendGrid email verification with one-time codes**
- Login rate limiting with a **5-minute cooldown after 5 failed attempts** using Python threading
- Age verification during account creation

### News
- Browse **top US headlines** powered by the [NewsAPI](https://newsapi.org/)
- **Search articles** by keyword
- **Save articles** to your profile for later reading
- **Configurable page size** — control how many articles are returned per request
- Articles display title, source, and URL

### Personalization & Recommendations
- Set **topic preferences** (e.g. "AI, Sports, UGA") to tailor your feed
- **Content-based recommendation engine** built with:
  - **pandas** for structured article data processing
  - **scikit-learn TF-IDF vectorization** to convert article text into numerical representations
  - **Cosine similarity** to match candidate articles against your saved article history
- Recommendations work with preferences alone, or are further personalized when saved articles are present

### Profile Management
- Change email (with verification code confirmation)
- Change password (with email verification)
- Change username
- Upload a profile picture
- Delete account
- Forgot password and forgot username flows — both secured with email verification

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Database | PostgreSQL (via psycopg2) |
| Password Security | Argon2 (argon2-cffi) |
| News Data | NewsAPI |
| Email | SendGrid |
| Data Processing | pandas |
| Machine Learning | scikit-learn |
| Unique IDs | UUID4 |

---

## Project Structure

```
WhatsNew/
├── main.py               # Entry point, navigation, and dashboard
├── Login.py              # Authentication, account creation, login flow
├── Profile.py            # Profile management, account settings, recovery flows
├── NewsManagment.py      # Article fetching, saving, searching, DataFrame conversion
├── Recommendations.py    # TF-IDF recommendation engine
├── Password_Security.py  # Argon2 hashing and verification
├── Email_Maintance.py    # SendGrid email verification
└── .env                  # Environment variables (not included in repo)
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL
- A [NewsAPI](https://newsapi.org/) API key
- A [SendGrid](https://sendgrid.com/) API key

### Installation

```bash
# Clone the repository
git clone https://github.com/zderival/WhatsNew.git
cd WhatsNew

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```
NEWS_API_KEY=your_newsapi_key
SENDGRID_API_KEY=your_sendgrid_key
Database_Password=your_postgres_password
```

### Database

Create a PostgreSQL database called `whats_new` and set up the `user` table:

```sql
CREATE TABLE "user" (
    id UUID PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    dob DATE NOT NULL
);
```

### Run

```bash
python main.py
```

---

## Roadmap

- [ ] Persist saved articles and preferences to the database
- [ ] GUI (planned for future release)
- [ ] Expanded recommendation model using article descriptions and authors
- [ ] Article filtering by date range

---

## Author

**Zachary Derival**  
GitHub: [@zderival](https://github.com/zderival)