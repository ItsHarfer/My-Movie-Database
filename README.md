# My Movie Database Part 2

A Python-based Command Line Interface (CLI) application for managing a local movie database. Users can add, view, edit, delete, and analyze movie entries. All data is persisted in a local JSON file.

---

## Features

- Create, Read, Update, Delete (CRUD) movie entries
- Calculate average and median ratings
- Identify top-rated and lowest-rated movies
- Generate rating histograms by attribute
- Menu-based navigation system
- Local JSON file storage

---

## Tech Stack

- Python 3.10+
- JSON for data persistence
- Modular structure with clear separation of concerns

---

## Project Structure

```
.
├── analysis.py           # Handles movie rating calculations
├── config.py             # Configuration and constants
├── data.json             # JSON file used as a local database
├── handlers.py           # Functions for user actions
├── helpers.py            # Helper functions (e.g., input validation)
├── main.py               # Entry point with CLI logic
├── menu.py               # Menu structure definition
├── menu_dispatcher.py    # Routes menu selections to handler functions
├── movie_crud.py         # Core CRUD logic for add/delete/update
├── movie_storage.py      # File I/O for loading and saving movie data
├── printers.py           # Colored and formatted output
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ItsHarfer/The-Movie-Project-Part-2.git
cd The-Movie-Project-Part-2-main
```

### 2. Install Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

*This project requires the following external libraries:*  
- Colorama (for colored terminal output)  
- Matplotlib (for generating rating histograms)  

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
Email: `martin.haferanke@gmail.com`

---

## License

This project is licensed under the MIT License.

---

Built for learning, practicing Python, and exploring structured data processing with CLI tools.
