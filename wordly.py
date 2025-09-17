"""A command-line tool to help solve Wordle puzzles.

This script provides a simple interactive solver for the popular word game Wordle.
It suggests the best word to guess next based on letter frequency and filters
the list of possible words based on user feedback about correct letters,
incorrect letters, and letters in the wrong position.
"""
# Wordle Solver
# quick and dirty wordle solver. Very picky about input format - HCE
import pandas as pd
from collections import Counter

def nextword(df):
    """Calculates the best word to guess next.

    This function analyzes the remaining possible words and suggests the
    one that is most likely to narrow down the options, based on letter
    frequency.

    Args:
        df (pd.DataFrame): A DataFrame containing the list of possible words.
            It must have a 'word' column.

    Returns:
        str: The suggested word to play next.
    """
    # Create a list of all letters in the words
    letterlist = [char for word in df.word for char in word]
    # Find the most common letters
    commonletters = [tup[0] for tup in Counter(letterlist).most_common(26)]
    # Score each word based on the sum of the indices of its letters in the list of common letters
    df['score'] = df.word.apply(lambda word: sum(commonletters.index(c) if c in commonletters else 0 for c in word)
                                + 26 * len(word) - len(set(word)))
    # Propose the word with the lowest score
    proposal = df.loc[df['score'].idxmin()].word
    print(proposal)
    return proposal

def wordle(df):
    """Runs the interactive Wordle solver game.

    This function guides the user through the process of solving a Wordle
    puzzle by repeatedly suggesting the best next word and filtering the
    word list based on user feedback.

    Args:
        df (pd.DataFrame): A DataFrame containing the initial list of
            possible words. It must have a 'word' column.
    """
    # Continue the game until there is only one word left
    while len(df) > 1:
        print(f'There are {len(df)} words')
        print(f'Best Next word: {nextword(df)}')
        # Ask the user for the green matches
        green = input('Enter Green matches as .X...\n')
        if green:
            # Filter the DataFrame based on the green matches
            df = df[df.word.str.match(f'({green})')]
        # Ask the user for the grey misses
        grey = input('Enter Grey misses as A|B|C\n')
        if grey:
            # Filter the DataFrame based on the grey misses
            df = df[df.word.str.match(f"(?!.*[{grey}]).*")]
        # Ask the user for the yellow misses
        yellow1 = input('Enter Yellow misses as A|B|C\n')
        while yellow1:
            # Filter the DataFrame based on the yellow misses
            df = df[df.word.str.match(f"(.*[{yellow1}]).*")]
            # Ask the user for the yellow positions
            yellow2 = input('Enter Yellow positions as ..[^A|B][^[C].\n')
            # Filter the DataFrame based on the yellow positions
            df = df[df.word.str.match(f"{yellow2}")]
            # Ask the user for the yellow misses again
            yellow1 = input('Enter Yellow misses as A|B|C\n')
        print(df)

if __name__ == '__main__':
    # Main execution block
    # This part of the script runs when it is executed directly. It loads the
    # word list from 'words.txt' into a pandas DataFrame and then starts the
    # interactive Wordle solver.
    df = pd.read_fwf('words.txt', names=['word'], header=None, converters={'word': str})
    wordle(df)