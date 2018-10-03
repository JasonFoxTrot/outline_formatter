#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from io import StringIO

MINUS = '-'
ADDITION = '+'
INDENTATION = ' '


class BulletSequences:
    def __init__(self):
        self._sequences = []

    @property
    def sequences(self):
        return self._sequences

    @property
    def num_of_sequences(self):
        return len(self.sequences)

    def add_sequences(self, num=0):
        for x in range(num):
            self._sequences.append(0)

    def remove_sequences(self, num=0):
        self._sequences = self._sequences[:num]

    def increment_sequence(self, index=-1):
        self._sequences[index] += 1


def outline_formatter(outline):
    # Remove blank lines
    outline_sans_blank_lines = StringIO()
    for line in outline:
        if line.rstrip():
            outline_sans_blank_lines.write(line)
    outline_sans_blank_lines.seek(0)

    # Create a copy of the outline to be used for searches during the looping process
    # This will help us determine the correct bullet icon to use
    searchable_outline = StringIO(outline_sans_blank_lines.getvalue())

    # Format bullets
    output = ""
    sequences = BulletSequences()  # Should allow us to handle an 'infinite' amount of asterisks
    for current_line in outline_sans_blank_lines:
        if current_line.startswith("*"):
            # Split the line separating the bullet identifier from the actual sentence
            asterisks, sentence = current_line.split(" ", 1)

            # Ensure our sequence holder is the correct length
            difference = len(asterisks) - sequences.num_of_sequences
            if difference > 0:
                sequences.add_sequences(difference)
            elif difference < 0:
                sequences.remove_sequences(difference)
            sequences.increment_sequence()

            # Assemble line
            output += ' '.join(['.'.join([str(n) for n in sequences.sequences]), sentence])
        elif current_line.startswith("."):
            # Get indentation of next line
            searchable_outline.seek(outline_sans_blank_lines.tell())
            next_line = next((line for line in searchable_outline if line.startswith('*') or line.startswith('.')),
                             None)
            if next_line and next_line.startswith("."):
                next_line_periods, _ = next_line.split(" ", 1)
            else:
                next_line_periods = ''

            # Get current line information
            periods, sentence = current_line.split(" ", 1)
            num_of_periods = len(periods)
            bullet_icon = ADDITION if num_of_periods < len(next_line_periods) else MINUS

            # Assemble line
            output += f" {INDENTATION*num_of_periods}{bullet_icon} {sentence}"
        else:
            # Assemble line
            # Should inherit indentation from previous line
            output += f" {INDENTATION*num_of_periods}  {current_line}"
    return output


if __name__ == "__main__":
    outline = outline_formatter(sys.stdin)
    sys.stdout.write(outline)
