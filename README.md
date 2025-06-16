# My Movie Database – SQL / HTML / API Edition 🎬

A Python-based application for managing a movie database, accessible via both Command Line Interface (CLI) and a static web interface. Users can add, view, update, delete, and analyze movies with automatic data fetching via the OMDb API. All data is persisted using SQLite. Multi-user support is now included with login and user-specific movie libraries.

---

## Features

- **Dual Interface:** Command Line Interface (CLI) and Static Web Interface
- **Multi-User Support:** Manage separate movie collections for each user
- Add movies by title with automatic data enrichment from the OMDb API
- Create, Read, Update, Delete (CRUD) movie entries
- Persistent storage via SQLite database
- Calculate average and median ratings
- Identify top-rated and lowest-rated movies
- Generate histograms by rating or year
- Poster URLs stored and shown alongside movie entries
- Menu-based CLI navigation
- Environment variables for secure API config (`.env`)
- Generate static web pages displaying current movie library

---

## Tech Stack

- Python 3.10+
- SQLite for persistent structured data storage
- OMDb API integration (via HTTP requests)
- Modular Python architecture
- HTML/CSS for static web frontend

---

## Project Structure

```
.
├── main.py                      # CLI entry point
├── requirements.txt             # External dependencies
├── analysis.py                  # Rating calculations and statistics
├── printers.py                  # Colored terminal output formatting
├── .env                         # Environment variables (excluded from VCS)
├── config/
│   ├── config.py                # Global configuration settings
│   └── sql_queries.py           # SQL query strings
├── data/
│   └── movies.db                # SQLite database (excluded from VCS)
├── helpers/                     # Utility functions
│   ├── dispatcher_utils.py      # Dispatcher helpers
│   ├── file_utils.py            # File-related utilities
│   ├── filter_utils.py          # Filtering logic
│   ├── html_utils.py            # HTML generation helpers
│   ├── input_utils.py           # Input parsing and validation
│   ├── movie_utils.py           # Movie-specific helpers (e.g., country codes)
│   ├── stats_utils.py           # Statistical calculation helpers
│   └── system_utils.py          # System-level utilities
├── movies/                      # Movie module
│   ├── dispatcher.py            # Menu routing for movies
│   ├── handler.py               # Logic for handling movie commands
│   ├── menu.py                  # Menu interaction loop
│   ├── storage_json.py          # JSON-based movie storage
│   └── storage_sql.py           # SQL-based movie storage
├── users/                       # User management
│   ├── dispatcher.py            # Menu routing for users
│   ├── handler.py               # User creation/selection logic
│   ├── menu.py                  # User menu interaction loop
│   ├── session_user.py          # Active user session state
│   └── storage_sql.py           # SQL-based user data storage
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ItsHarfer/My-Movie-Database.git
cd My-Movie-Database
```

### 2. Configure Environment

> Before we can move on, get your personal API key from OMDB: https://www.omdbapi.com/ and activate it in your registration email.
 
Create a `.env` file in the root directory and add your OMDb API key:

```
OMDB_API_KEY='your_api_key_here'
OMDB_API_URL='https://www.omdbapi.com/?'
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

*Dependencies include:*  
- `colorama` – terminal color formatting  
- `matplotlib` – for visualizations  
- `sqlalchemy` – for database operations  
- `python-dotenv` – for environment variable loading  
- `requests` – for API access

### 4. Run the Application

CLI:
```bash
python main.py
```

Generate Web Interface:
- Select the "Generate Static Website" option within the CLI.
- Open the generated HTML file in your browser.

---

## Example Operations

- **👤 User Login/Create/Switch:** Select an existing user, switch to another or create a new one to manage personal collections
- **🎬 Add a Movie:** Automatically fetch rating, release year, and poster from OMDb API
- **❌ Delete a Movie:** Remove a movie from the current user's collection by exact title
- **📝 Update a Movie** With a personal note or mark it as your favourite movie.
- **📋 View All Movies:** Show all movies stored for the current user
- **🔍 Search Movies:** Find movies by partial match in title
- **📊 Movie Statistics:** Display average, median, highest, and lowest-rated movies
- **🎲 Random Movie:** Show a randomly selected movie
- **↕️ Sort Movies:** Order movies by rating or release year (ascending/descending)
- **🎯 Filter Movies:** Filter by minimum rating and release year range
- **📈 Create a Histogram:** Generate bar or scatter plots as `.png` images
- **🌐 Static Web Interface:** Export all movies to a styled HTML webpage
 

---

## Author

Martin Haferanke  
GitHub: [@ItsHarfer](https://github.com/ItsHarfer)  
Email: `martin.haferanke@gmail.com`

---

## License

Licensed under the MIT License (Educational Use).

Built for learning, exploring Python, SQL, API-powered CLI applications, and static web interfaces.
