# Word Lookup Dictionary Web App

A web application for looking up word definitions, with spelling suggestions and the ability to add new words to the dictionary.

## Features

- Word lookup with definitions
- Spelling correction and auto-suggestions using edit distance algorithm
- Web scraping to fetch definitions from online sources
- Add new words and definitions to the dictionary
- Persistent storage using pickle

## Installation

1. Clone this repository or download the source code

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install flask requests beautifulsoup4
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to http://127.0.0.1:5000/

## Project Structure

- `app.py`: Main Flask application
- `wordlookup.py`: Core functionality including Trie implementation and edit distance algorithm
- `data/`: Directory for storing the dictionary data
- `static/`: Static files (CSS, JavaScript)
- `templates/`: HTML templates

## How It Works

1. **Trie Data Structure**: Efficiently stores words and their definitions, allowing for fast lookups.
2. **Edit Distance Algorithm**: Used to calculate the similarity between words and provide spelling suggestions.
3. **Web Scraping**: If a word is not found in the local dictionary, the application attempts to fetch its definition from an online source.
4. **Persistence**: The dictionary is saved to disk using pickle, ensuring data persists between application restarts.

## Usage

1. **Search for a word**: Type a word in the search box and click "Search" or press Enter.
2. **Get spelling suggestions**: If a word is not found, spelling suggestions will be displayed.
3. **Add a new word**: Enter a word and its definition in the form at the bottom of the page, then click "Add Word".

## Extending the Application

- Add user authentication to allow multiple users with personal dictionaries
- Implement history of searched words
- Add support for multiple languages
- Improve web scraping by adding more online dictionary sources
- Add example sentences for each word
