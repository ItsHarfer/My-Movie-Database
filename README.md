# Movie Rating CLI App

A Python-based Command Line Interface (CLI) application for managing a local movie database. Users can add, view, edit, delete, and analyze movie entries. Data is persisted in a local JSON file.

---

## Features

- Create, Read, Update, Delete (CRUD) movie entries
- Calculate average ratings
- Identify top-rated and lowest-rated movies
- Menu-based navigation system
- JSON file-based data storage

---

## Tech Stack

- Python 3.10+
- JSON for data persistence
- Modular structure with clean separation of concerns

---

## Project Structure

```
.
├── analysis.py           # Handles movie rating calculations
├── config.py             # Configuration and constants
├── data.json             # JSON file used as a database
├── data_io.py            # File I/O for loading and saving data
├── handlers.py           # Functions for user actions
├── helpers.py            # Helper functions (e.g., input validation)
├── main.py               # Entry point with CLI logic
├── menu.py               # Menu structure definition
├── menu_dispatcher.py    # Routing menu selections to handlers
├── movie_crud.py         # Core CRUD operations
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie-rating-cli.git
cd movie-rating-cli
```

### 2. Install Requirements

No external packages needed – just make sure Python 3.10+ is installed.

### 3. Run the Application

```bash
python main.py
```

---

## Example Operations

- Add a Movie  
  - Title: `The Matrix`  
  - Rating: `8.7`  
  - Release Year: `1999`
- Analyze  
  - Top Rated: `Pulp Fiction (9.5)`  
  - Worst Rated: `The Room (3.6)`, `Everything Everywhere All At Once (3.6)`

---

## Author

Martin Haferanke  
GitHub: [@harfer](https://github.com/harfer)  
Email: `harfer@msnp.ninja`

---

## License

This project is licensed under the MIT License.

---

Built for learning, practicing Python, and exploring data handling.
