# wordlookup.py - Core word lookup functionality

import os
import json
import requests
from bs4 import BeautifulSoup
import pickle


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.definition = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, definition):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.definition = definition

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False, None
            node = node.children[char]
        return node.is_end_of_word, node.definition

    def get_all_words(self, prefix=""):
        words = []
        self._collect_words(self.root, prefix, "", words)
        return words

    def _collect_words(self, node, prefix, current, words):
        if node.is_end_of_word:
            words.append((prefix + current, node.definition))

        for char, child in node.children.items():
            self._collect_words(child, prefix, current + char, words)


class WordLookup:
    def __init__(self):
        self.trie = Trie()
        self.dictionary_file = "data/dictionary.pkl"
        self.load_dictionary()

    def load_dictionary(self):
        if os.path.exists(self.dictionary_file):
            with open(self.dictionary_file, 'rb') as f:
                self.trie = pickle.load(f)
        else:
            # Load some initial words
            sample_words = {
                "apple": "A round fruit with red, yellow, or green skin and crisp flesh.",
                "banana": "A long curved fruit with a yellow skin and soft sweet flesh.",
                "computer": "An electronic device capable of processing data according to instructions.",
                "dictionary": "A book or electronic resource that lists words and gives their meanings.",
                "python": "A high-level programming language known for its readability and versatility."
            }

            for word, definition in sample_words.items():
                self.trie.insert(word, definition)

            self.save_dictionary()

    def save_dictionary(self):
        with open(self.dictionary_file, 'wb') as f:
            pickle.dump(self.trie, f)

    def lookup(self, word):
        exists, definition = self.trie.search(word)

        if exists:
            return {
                'found': True,
                'definition': definition
            }

        # Try to fetch definition from online
        online_definition = self.fetch_online_definition(word)
        if online_definition:
            # Add to our dictionary
            self.add_word(word, online_definition)
            return {
                'found': True,
                'definition': online_definition
            }

        return {
            'found': False,
            'definition': None
        }

    def add_word(self, word, definition):
        if not word or not definition:
            return False

        self.trie.insert(word, definition)
        self.save_dictionary()
        return True

    def fetch_online_definition(self, word):
        try:
            # Using Merriam-Webster's website for scraping
            url = f"https://www.merriam-webster.com/dictionary/{word}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the definition section
                definition_div = soup.find('div', class_='entry-word-section-container')
                if definition_div:
                    definition_element = definition_div.find('span', class_='dtText')
                    if definition_element:
                        return definition_element.get_text().strip()

            return None
        except Exception as e:
            print(f"Error fetching definition: {e}")
            return None

    def get_edit_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.get_edit_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def get_suggestions(self, word, max_distance=2, max_suggestions=5):
        all_words = self.trie.get_all_words()
        suggestions = []

        for dict_word, definition in all_words:
            distance = self.get_edit_distance(word, dict_word)
            if distance <= max_distance:
                suggestions.append({
                    'word': dict_word,
                    'distance': distance
                })

        # Sort by edit distance (closest first)
        suggestions.sort(key=lambda x: x['distance'])

        # Return top suggestions
        return [sugg['word'] for sugg in suggestions[:max_suggestions]]