# wordly

A quick and dirty Wordle© solver.

When Wordle became a thing, my immediate reaction was "This looks like work; I should just have a computer solve it". There have subsequently been much more rigorous solvers developed (including by the NYTimes), but this works well for a quick effort.

## File Descriptions

- `wordly.py`: The main script for the Wordle solver. It contains the logic for suggesting words and filtering the word list based on user input.
- `words.txt`: A list of 5-letter words used by the solver. This is derived from the standard Linux `words` file.

## Setup

This script requires the `pandas` library. You can install it using pip:

```bash
pip install pandas
```

## Usage

To run the solver, execute the `wordly.py` script from your terminal:

```bash
python wordly.py
```

The script will then prompt you for information about the state of your Wordle game.

1.  **Green Matches**: Enter the letters that are in the correct position. Use a `.` for any unknown letter. For example, if the word is "WATER" and you know "A" is the second letter and "E" is the fourth, you would enter `.A.E.`.
2.  **Grey Misses**: Enter any letters that are not in the word, separated by `|`. For example, if "S", "O", and "U" are not in the word, you would enter `S|O|U`.
3.  **Yellow Misses**: Enter any letters that are in the word but in the wrong position, separated by `|`. For example, if "R" and "T" are in the word but in the wrong spot, you would enter `R|T`.
4.  **Yellow Positions**: For the yellow letters, specify the positions where they are *not* located. For example, if "R" is not the first letter and "T" is not the third, you would enter `[^R].[^T]..`.

The solver will continue to suggest the best word to play next and narrow down the possibilities until only one word remains.
