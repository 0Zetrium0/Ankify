# Preface

Ankify is a lightweight CLI tool designed to automate the creation of Anki decks and flashcards using the AnkiConnect API. It's perfect for importing large amounts of cards generated via LLMs (like ChatGPT, Claude, etc.).

# Pre-requities

1. Open Anki and install the **AnkiConnect** add-on:
   - Go to `Tools` > `Add-ons` > `Get Add-ons...`.
   - Paste the code `2055492159` to download it.
2. Restart Anki. The API will now be accessible locally at `http://localhost:8765`.
3. **Important:** Anki must remain open while running the script.

> For more details, check out the [AnkiConnect Documentation](https://github.com/FooSoft/anki-connect).

# Steps to install

1. Clone the repository : 
(If you installed the .zip archive, skip this step).
```bash
git clone "<repository_url>"
cd <repository_directory>
```
2. Create and activate a python environment : 
```bash
# On Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```
```shell
# On Windows (Command Prompt)
python -m venv venv
venv/Scripts/activate
```
3. Install the required dependencies : 
```bash
pip install -r requirements.txt
```
# File format
The file containing your flashcards must follow a strict format. Each line represents one card, where the question **must end with a question mark** and be separated from the answer by a colon (:).

Example of a valid `flashcard.txt`:
```
What is the capital of France?:Paris
Who developed Python?:Guido van Rossum
Is Python interpreted or compiled?:Interpreted
```
# Usage

## Test the API Connection : 
Verify if the script can successfully communicate with Anki :
```bash
python3 ankify.py --api 
```
## Import flashcards
Create or update a deck with your text file :
```bash
python3 ankify.py --file path/to/file.txt --deck "My Deck Name"
```
## View available Decks
List all your existing Anki decks : 
```bash
python3 ankify.py --get_decks
```
