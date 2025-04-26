// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const wordInput = document.getElementById('word-input');
    const searchBtn = document.getElementById('search-btn');
    const resultContainer = document.getElementById('result-container');
    const resultWord = document.getElementById('result-word');
    const resultDefinition = document.getElementById('result-definition');
    const suggestionsContainer = document.getElementById('suggestions-container');
    const suggestionsList = document.getElementById('suggestions-list');
    const newWordInput = document.getElementById('new-word');
    const newDefinitionInput = document.getElementById('new-definition');
    const addWordBtn = document.getElementById('add-word-btn');
    const addWordMessage = document.getElementById('add-word-message');

    // Search word function
    async function searchWord(word) {
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ word })
            });

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error searching word:', error);
        }
    }

    // Display search results
    function displayResults(data) {
        resultContainer.classList.remove('hidden');
        resultWord.textContent = data.word;

        if (data.found) {
            resultDefinition.textContent = data.definition;
            suggestionsContainer.classList.add('hidden');
        } else {
            resultDefinition.textContent = 'Word not found in dictionary.';

            if (data.suggestions && data.suggestions.length > 0) {
                displaySuggestions(data.suggestions);
            } else {
                suggestionsContainer.classList.add('hidden');
            }
        }
    }

    // Display word suggestions
    function displaySuggestions(suggestions) {
        suggestionsList.innerHTML = '';
        suggestionsContainer.classList.remove('hidden');

        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            li.addEventListener('click', () => {
                wordInput.value = suggestion;
                searchWord(suggestion);
            });
            suggestionsList.appendChild(li);
        });
    }

    // Add new word function
    async function addWord(word, definition) {
        try {
            const response = await fetch('/add_word', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ word, definition })
            });

            const data = await response.json();

            if (data.success) {
                showAddWordMessage('Word added successfully!', 'success');
                newWordInput.value = '';
                newDefinitionInput.value = '';
            } else {
                showAddWordMessage(data.error || 'Failed to add word.', 'error');
            }
        } catch (error) {
            console.error('Error adding word:', error);
            showAddWordMessage('An error occurred.', 'error');
        }
    }

    // Show add word message
    function showAddWordMessage(message, type) {
        addWordMessage.textContent = message;
        addWordMessage.className = type;

        setTimeout(() => {
            addWordMessage.textContent = '';
            addWordMessage.className = '';
        }, 3000);
    }

    // Event listeners
    searchBtn.addEventListener('click', () => {
        const word = wordInput.value.trim();
        if (word) {
            searchWord(word);
        }
    });

    wordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const word = wordInput.value.trim();
            if (word) {
                searchWord(word);
            }
        }
    });

    addWordBtn.addEventListener('click', () => {
        const word = newWordInput.value.trim();
        const definition = newDefinitionInput.value.trim();

        if (!word) {
            showAddWordMessage('Please enter a word.', 'error');
            return;
        }

        if (!definition) {
            showAddWordMessage('Please enter a definition.', 'error');
            return;
        }

        addWord(word, definition);
    });
});