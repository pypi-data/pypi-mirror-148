import typer
from qzlt import sets
from qzlt.sessions import Session

app = typer.Typer()

sets_app = typer.Typer()
sets_help = "Manage all sets"
app.add_typer(sets_app, name="sets", help=sets_help)

set_app = typer.Typer()
set_help = "Manage an individual set"
app.add_typer(set_app, name="set", help=set_help)


@app.command()
def study(set_title: str, study_mode: str = "write", shuffle: bool = False):
    """
    Begin a study session
    """
    deck = sets.load(set_title)
    if deck is None:
        typer.secho(f"Could not find deck titled `{set_title}`", fg="red")
        return

    session = Session(deck, shuffle)
    if study_mode == "write":
        session.write()
    elif study_mode == "learn":
        session.learn()


@sets_app.callback(invoke_without_command=True)
def sets_default(ctx: typer.Context):
    """
    List all sets as the default action for `sets` command
    """
    if ctx.invoked_subcommand is None:
        sets.list()


@sets_app.command("list")
def sets_list():
    """
    List all sets
    """
    sets.list()


@sets_app.command("create")
def sets_create():
    """
    Create a new set
    """
    sets.create()


@sets_app.command("delete")
def sets_delete(set_title: str):
    """
    Delete a set
    """
    sets.remove(set_title)


@set_app.command("add")
def set_add(set_title: str):
    """
    Add cards to a set
    """
    sets.add(set_title)


@set_app.command("delete")
def set_delete(set_title: str, card_id: int):
    """
    Delete a card from a set
    """
    sets.delete(set_title, card_id)


@set_app.command("list")
def set_list(set_title: str):
    """
    List all cards in the set
    """
    deck = sets.load(set_title)
    if deck is None:
        typer.secho(f"Could not find deck titled `{set_title}`", fg="red")
        return
    deck.list()


if __name__ == "__main__":
    app()
