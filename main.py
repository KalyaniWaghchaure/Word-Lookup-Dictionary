# app.py - Main Flask application

import os
from flask import Flask, render_template, request, jsonify
from wordlookup import WordLookup

app = Flask(__name__)
word_lookup = WordLookup()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    word = data.get('word', '').strip().lower()

    if not word:
        return jsonify({'error': 'No word provided'})

    result = word_lookup.lookup(word)
    suggestions = []

    if not result['found']:
        suggestions = word_lookup.get_suggestions(word)

    return jsonify({
        'word': word,
        'found': result['found'],
        'definition': result['definition'],
        'suggestions': suggestions
    })


@app.route('/add_word', methods=['POST'])
def add_word():
    data = request.get_json()
    word = data.get('word', '').strip().lower()
    definition = data.get('definition', '').strip()

    if not word or not definition:
        return jsonify({'error': 'Word and definition are required'})

    success = word_lookup.add_word(word, definition)
    return jsonify({'success': success})


if __name__ == '__main__':
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    app.run(debug=True)