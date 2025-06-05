# My Movie Database – SQL Edition 🎬

A Python-based Command Line Interface (CLI) application for managing a movie database.  
Users can add, view, update, delete, and analyze movies with automatic data fetching via the OMDb API.  
All data is persisted using SQLite.

---

## Features

- Add movies by title with automatic data enrichment from the OMDb API
- Create, Read, Update, Delete (CRUD) movie entries
- Persistent storage via SQLite database
- Calculate average and median ratings
- Identify top-rated and lowest-rated movies
- Generate histograms (with fixed year display) by rating or year
- Poster URLs stored and shown alongside movie entries
- Menu-based CLI navigation
- Environment variables for secure API config (`.env`)

---

## Tech Stack

- Python 3.10+
- SQLite for persistent structured data storage
- OMDb API integration (via HTTP requests)
- Modular Python architecture

---

## Project Structure

```
.
├── analysis.py           # Rating calculations and statistics
├── config.py             # Configuration values and constants
├── .env                  # API key and external URLs (excluded from version control)
├── handlers.py           # User interaction logic (e.g. add/delete/update)
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
git clone [https://github.com/ItsHarfer/The-Movie-Project-Part-2.git](https://github.com/ItsHarfer/My-Movie-Database.git)
cd The-Movie-Project-Part-2
```

### 2. Configure Environment

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

```bash
python main.py
```

---

## Example Operations

Here are some things you can do with the application:

- **Add a Movie**
  - Example: `Titanic`
  - Automatically fetches rating, release year, and poster from the OMDb API.
  - No need to manually enter data.

- **Delete a Movie**
  - Remove any movie by entering its exact title.
  - Confirmation is shown after deletion.

- **Update a Movie Rating**
  - Modify the rating of an existing movie by name.
  - Input is validated between 1.0 and 10.0.

- **View All Movies**
  - Displays a formatted list of all movies with their rating, year, and poster URL.

- **Search for a Movie**
  - Enter part of a movie title (e.g. `ring`) to see all matches (e.g. `The Lord of the Rings`).

- **Show Movie Statistics**
  - View average and median rating.
  - See top-rated and worst-rated movies from the collection.

- **Random Movie**
  - Picks and displays one random movie from your database for inspiration.

- **Sort Movies by Attribute**
  - Choose an attribute (e.g. `rating` or `year`) and sort ascending or descending.

- **Create a Histogram**
  - Create and save a visualization for rating or release year as `.png`.
  - Year axis uses whole numbers (bugfix included).

- **Filter Movies by Rating and Year**
  - Input a minimum rating and a release year range (e.g. 7.0 from 2000 to 2022).
  - Displays only matching movies.

---

## Author

Martin Haferanke  
GitHub: [@ItsHarfer](https://github.com/ItsHarfer)  
Email: `martin.haferanke@gmail.com`

---

## License

This project is licensed under the MIT License (Educational Use).

---

Built for learning, exploring Python, SQL, and API-powered CLI applications.
