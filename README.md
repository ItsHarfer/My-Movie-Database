# My Movie Database – SQL Edition 🎬

A Python-based application for managing a movie database, accessible via both Command Line Interface (CLI) and a static web interface. Users can add, view, update, delete, and analyze movies with automatic data fetching via the OMDb API. All data is persisted using SQLite.

---

## Features

- **Dual Interface:** Command Line Interface (CLI) and Static Web Interface
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
├── analysis.py           # Rating calculations and statistics
├── config.py             # Configuration values and constants
├── .env                  # API key and external URLs (excluded from version control)
├── handlers.py           # User interaction logic (e.g., add/delete/update/web generation)
├── helpers.py            # Input validation, filtering, visualizations
├── main.py               # CLI entry point
├── menu.py               # Menu structure
├── menu_dispatcher.py    # Maps menu commands to handlers
├── movie_crud.py         # Database interaction helpers
├── movie_storage_sql.py  # SQLAlchemy logic for storage backend
├── printers.py           # Colored terminal output formatting
├── requirements.txt      # External Python dependencies
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

- **Add a Movie:** Automatically fetch rating, release year, and poster from OMDb API.
- **Delete a Movie:** Remove movies by entering their exact titles.
- **Update a Movie Rating:** Modify existing ratings with validation (1.0–10.0).
- **View All Movies:** Display all movies with their details.
- **Search Movies:** Find movies by partial title match.
- **Movie Statistics:** View average, median, top-rated, and lowest-rated movies.
- **Random Movie:** Display a randomly selected movie from your database.
- **Sort Movies:** Organize movies by rating or release year.
- **Create a Histogram:** Visualize ratings or release years as `.png` images.
- **Filter Movies:** Filter movies by rating and release year ranges.
- **Static Web Interface:** Generate a visually appealing web page to overview your movie collection.

---

## Author

Martin Haferanke  
GitHub: [@ItsHarfer](https://github.com/ItsHarfer)  
Email: `martin.haferanke@gmail.com`

---

## License

Licensed under the MIT License (Educational Use).

Built for learning, exploring Python, SQL, API-powered CLI applications, and static web interfaces.
