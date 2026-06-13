__author__="z3tr1um"
__version__="1.0"

import click
import requests
import json
import re

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

HOST = "http://localhost:8765"

console = Console()

BANNER = r"""
	     _____ _        _                 
	 ___|___ /| |_ _ __(_)_   _ _ __ ___  
	|_  / |_ \| __| '__| | | | | '_ ` _ \ 
	 / / ___) | |_| |  | | |_| | | | | | |
	/___|____/ \__|_|  |_|\__,_|_| |_| |_|  

	2026		         ankicard v1.0                                                                                                               
"""

# Options creation
@click.command(no_args_is_help=True)
@click.option('--api', is_flag=True, help="Try the connection with AnkiConnect.")
@click.option('--file', type=click.File('r', encoding='utf-8'), help="File containing 'front:back' flashcards. The question must have a question mark.")
@click.option('--get_decks', is_flag=True, help="Allow you to see your decks.")
@click.option('--deck', help="Specify the deck where create cards if (use --file).")

def main(api, file, get_decks, deck):
	console.print(BANNER, style="bold purple")
	# Test if AnkiConnect is connected before doing anything.
	api_test = apiConnectionTest(HOST)
	if api_test:
		if api:
			console.print("[bold green][*] AnkiConnect connected.[/bold green]")
		elif file and deck:
			handleCards(file, deck)
		elif file:
			console.print("[bold red][!] You must specify the deck [italic bold red](--deck)[/italic bold red] where the cards will be created.[/bold red]")
		elif deck:
			console.print("[bold red][!] You must specify the file [italic bold red](--file)[/italic bold red] that contains 'front:back' of flashcards.[/bold red]")
		elif get_decks:
			getDecks()
	else:
		console.print("[bold red][!] AnkiConnect not connected. Launch Anki or install the add-on.[/bold red]")

def apiConnectionTest(host):
	try:
		r = requests.get(host)
		if r.status_code == 200:
			return True
	except requests.exceptions.ConnectionError:
		return False

def handleCards(file, deck):
	if deck == None:
		console.print("[bold red][!] You must specify the deck.[/bold red]")
		return
	flashcard_list = handleFile(file)
	if flashcard_list is False:
		return
	in_deck = inDeck(deck)
	if in_deck:
		console.print(f"[bold green][+] The deck [italic bold green]{deck}[/italic bold green] already exists and the cards will be added.[/bold green]")
		createCards(flashcard_list, deck)
	else:
		console.print(f"[bold green][+] The deck [italic bold green]{deck}[/italic bold green] will be created.[/bold green]")
		createDeck(deck)
		createCards(flashcard_list, deck)
		
def createCards(flashcard, deck):
	card_number = 0
	for item in flashcard:
			payload = {"action":"addNote","version":6,"params":{"note":{"deckName":f"{deck}","modelName": "Basic","fields":{"Front":f"{item['front']}","Back":f"{item['back']}"}}}}
			json_payload = json.dumps(payload)
			r = requests.post(HOST, data=json_payload)
			card_number += 1
	console.print(Panel(f"[bold green][+] {card_number} cards created in the deck [italic bold green]{deck}[/italic bold green][/bold green]", border_style="green",))

def getDecks():
	data = {"action":"deckNames","version":6}
	json_data = json.dumps(data)
	r = requests.post(HOST, data=json_data)
	response = json.loads(r.text)

	table = Table(title="Available Anki decks", border_style="green")
	table.add_column("Deck name", style="bold green")

	for deck in response["result"]:
		table.add_row(deck)

	console.print(table)

def inDeck(deck):
	payload = {"action":"deckNames","version":6}
	json_payload = json.dumps(payload)
	r = requests.post(HOST, data=json_payload)
	response = json.loads(r.text)
	if deck in response['result']:
		return True
	else:
		return False

def createDeck(deck):
	payload = {"action":"createDeck","version":6,"params":{"deck":f"{deck}"}}
	json_payload = json.dumps(payload)
	r = requests.post(HOST, data=json_payload)
	response = json.loads(r.text)

def handleFile(file):
	temp_cards = []

	while True:
		chunk = file.readline()
		if not chunk:
			break
		elif not chunk.strip():
			continue
		elif re.search(r'[\S ]+\?:[\S ]+', chunk):
			clean_chunk = chunk.strip('\n')
			flashcard = clean_chunk.split(':', 1)
			temp_cards.append({'front':flashcard[0],'back':flashcard[1]})
		else:
			console.print("[bold red][!] Syntax error in the file. Program stopped. [/bold red]")
			return False

	yield from temp_cards

if __name__ == "__main__":
	main()