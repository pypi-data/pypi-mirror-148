import os
import json
import typer
from qzlt.cards import Card
from copy import deepcopy

# Home directory
HOME = os.path.expanduser("~")
# Where all quiz files are stored
BASE_PATH = os.path.abspath(f"{HOME}/.qzlt")


def create():
    """Prompts user to create a new set"""
    title = typer.prompt(typer.style("Title", fg="bright_black")).strip()
    description = typer.prompt(typer.style("Description", fg="bright_black")).strip()
    new_set = Set(title, description)
    save(new_set)
    typer.secho("Set successfully created", fg="green")


def remove(set_title):
    """
    Deletes a set from disk

    :param set_title: Title of set to be deleted
    """
    SET_PATH = f"{BASE_PATH}/{set_title}"
    if os.path.exists(SET_PATH):
        filenames = os.listdir(SET_PATH)
        for filename in filenames:
            os.remove(f"{SET_PATH}/{filename}")
        os.rmdir(SET_PATH)
        typer.echo(f"Deleted set `{set_title}`")
    else:
        typer.secho(f"Could not find set `{set_title}`", fg="red")


def save(s):
    """Save a set to disk"""
    SET_PATH = f"{BASE_PATH}/{s.title}"
    if not os.path.exists(SET_PATH):
        typer.secho(f"Directory {SET_PATH} not found. Creating it now...")
        os.makedirs(SET_PATH)
    with open(f"{SET_PATH}/info.json", "w") as info_file:
        info = {"title": s.title, "description": s.description}
        info = json.dump(info, info_file, indent=4)
    with open(f"{SET_PATH}/terms.txt", "w") as terms_file:
        for card in s:
            terms_file.writelines(f"{card.term}\n")
            terms_file.writelines(f"{card.definition}\n")


def load(set_title):
    """
    Loads an exisiting set from disk

    :param set_title: Title of the set to be loaded
    :returns: instance of Set or None if it doesn't exist
    """
    if not os.path.exists(f"{BASE_PATH}/{set_title}"):
        return None

    loaded_title, loaded_description = None, None
    loaded_cards = []

    # Populate title and description
    with open(f"{BASE_PATH}/{set_title}/info.json", "r") as info_file:
        info = json.load(info_file)
        loaded_title = info["title"]
        loaded_description = info["description"]

    # Populate cards
    with open(f"{BASE_PATH}/{set_title}/terms.txt", "r") as file:
        lines = file.read().splitlines()
        for i in range(len(lines) // 2):
            term, definition = lines[2 * i], lines[2 * i + 1]
            card = Card(term, definition)
            loaded_cards.append(card)

    return Set(loaded_title, loaded_description, loaded_cards)


def list():
    """Prints all sets to stdout"""
    size = os.get_terminal_size()
    terminal_width = min(size.columns, 120)

    title_width = terminal_width // 4
    description_width = terminal_width // 4 * 3

    typer.echo(f"{'TITLE': <{title_width}}{'DESCRIPTION': <{description_width}}")

    for title in os.listdir(BASE_PATH):
        with open(f"{BASE_PATH}/{title}/info.json", "r") as info_file:
            info = json.load(info_file)
            title, description = info["title"], info["description"]
            title_str = f"{title: <{title_width}}"
            description_str = f"{description: <{description_width}}"
            typer.echo(f"{title_str}{description_str}")


def add(set_title):
    """Prompts user to add cards to set"""
    s = load(set_title)
    if s is None:
        typer.secho(f"Could not find deck titled `{set_title}`", fg="red")
        return

    while True:
        typer.secho("Adding new card (press ctrl+c to exit)", fg="magenta")
        term = typer.prompt(typer.style("Term", fg="bright_black")).strip()
        definition = typer.prompt(typer.style("Definition", fg="bright_black")).strip()
        new_card = Card(term, definition)
        s.add(new_card)
        save(s)
        typer.secho("Card added", fg="green")
        typer.echo()


def delete(set_title, idx):
    """Deletes card `idx` from a set"""
    s = load(set_title)
    if s is None:
        typer.secho(f"Could not find set `{set_title}`", fg="red")
        return

    if idx < len(s):
        s.delete(idx)
        save(s)
        typer.echo(f"Deleted card {idx}")
    else:
        reason = None
        if idx < 0:
            reason = "cannot be less than 0"
        elif idx >= len(s):
            reason = "greater than set size"
        typer.secho(f"Invalid index: {idx} ({reason})", fg="red", err=True)


class Set:
    """
    Contains cards to be studied.
    Each set is labelled by a name and an optional description.
    """

    def __init__(self, title, description, cards=[]):
        """
        Constructs a new Set

        :param title: Title of the set
        :param description: Description of the set
        :param cards: Cards in the set (empty by default)
        """
        self._title = title
        self._description = description
        self._cards = deepcopy(cards)

    def __len__(self):
        """
        Implements built-in `len()` function

        :returns: Number of cards in the set
        """
        return len(self._cards)

    def __iter__(self):
        """Implements built-in iterator"""
        return iter(self._cards)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, new_cards):
        self._cards = new_cards

    def add(self, card):
        """
        Adds a card from set

        :param card: Instance of Card to be added
        """
        self._cards.append(card)

    def delete(self, idx):
        """
        Deletes a card from set

        :param idx: Index of card to be be deleted
        """
        self._cards.pop(idx)

    def list(self):
        """
        Prints a formatted table of cards within the set to stdout

        Card information includes
          - Index (0-based)
          - Term
          - Definition
        """
        style_width = 9  # Number of additional characters used for typer.style
        idx_width = 6
        term_width = 32
        definition_width = 32

        title_idx_str = f"{'': <{idx_width}}"
        title_term_str = f"{'TERM': <{term_width}}"
        title_definition_str = f"{'DEFINITION': <{definition_width}}"
        typer.echo(f"{title_idx_str}{title_term_str}{title_definition_str}")

        for i, card in enumerate(self._cards):
            term, definition = card.term, card.definition
            idx = f"[{typer.style(i, fg='blue')}]"
            idx_str = f"{idx: <{idx_width + style_width}}"
            term_str = f"{term: <{term_width}}"
            definition_str = f"{definition: <{definition_width}}"
            typer.echo(f"{idx_str}{term_str}{definition_str}")
