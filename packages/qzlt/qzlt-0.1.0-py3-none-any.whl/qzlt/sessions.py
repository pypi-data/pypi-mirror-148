from qzlt.utils import sample
import random
import typer


class Session:
    """
    A Session contains logic allowing the user to cycle and study cards in a
    provided Set.

    Several study modes are available:
      1. Write - type out each definition to test
      2. Learn - multiple choice questions
    """

    def __init__(self, deck, shuffle=False):
        """
        Constructs a new Session

        :param deck: Deck to be studied
        :param shuffle: Shuffles cards in deck if true (default: false)
        """
        self._deck = deck
        if shuffle:
            random.shuffle(self._deck.cards)
        self.correct = set()
        self.incorrect = set()

    def write(self):
        """Begins a writing session"""
        for i, card in enumerate(self._deck):
            typer.secho(f"Card {i+1}/{len(self._deck)}", fg="magenta")

            # Output term
            typer.secho(card.term, fg="bright_white", bold=True)

            # Prompt for answer
            answer = typer.prompt(
                typer.style("Answer", fg="bright_black"), default="", show_default=False
            ).strip()

            # Check answer
            if answer == card.definition:
                self.correct.add(card)
                typer.secho("Correct!", fg="green")
            else:
                self.incorrect.add(card)
                typer.secho(f"Incorrect", fg="red")
                typer.secho(
                    f"The correct answer was '{card.definition}'", fg="bright_black"
                )

                # Prompt for correction
                while answer != card.definition:
                    answer = typer.prompt(
                        typer.style("Retype correction", fg="bright_black"),
                        default="",
                        show_default=False,
                    ).strip()
            typer.echo()

        self.output_results()

        if len(self.incorrect) > 0 and typer.confirm("Review incorrect cards?"):
            self._deck.cards = [*self.incorrect]
            self.correct = set()
            self.incorrect = set()
            self.write()

    def learn(self):
        """Begins a learning session"""
        for i, card in enumerate(self._deck):
            typer.secho(f"Card {i+1}/{len(self._deck)}", fg="magenta")
            typer.secho(card.term, fg="bright_white", bold=True)

            num_choices = 4
            all_choices = list(map(lambda x: x.definition, self._deck.cards))

            # Populate choices
            choices = sample(num_choices - 1, all_choices)
            while card.definition in choices:
                choices = sample(num_choices - 1, all_choices)
            choices.append(card.definition)
            random.shuffle(choices)

            # Output choices to terminal
            for i, choice in enumerate(choices):
                typer.echo(f"{i + 1}. {choice}")

            # Prompt for answer
            index = typer.prompt(
                typer.style("Select the correct term", bold=True),
                default="",
                show_default=False,
            ).strip()

            # Check answer
            if choices[int(index) - 1] == card.definition:
                self.correct.add(card)
                typer.secho("Correct!", fg="green")
            else:
                self.incorrect.add(card)
                typer.secho("Incorrect", fg="red")
                typer.secho(
                    f"The correct answer was '{card.definition}'", fg="bright_black"
                )
            typer.echo()

        self.output_results()

        if len(self.incorrect) > 0 and typer.confirm("Review incorrect cards?"):
            self._deck.cards = [*self.incorrect]
            self.correct = set()
            self.incorrect = set()
            self.learn()

    def output_results(self):
        """Prints study results to stdout"""
        typer.secho(
            f"You got {len(self.correct)}/{len(self._deck)} cards correct",
            bold=True,
            fg="bright_white",
        )
