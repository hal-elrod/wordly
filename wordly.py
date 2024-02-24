# Wordle Solver
# quick and dirty wordle solver. Very picky about input format - HCE
import pandas as pd
from collections import Counter

def nextword(df):
    """
    This function calculates the next word to be proposed in the Wordle game.

    Parameters:
    df (DataFrame): The DataFrame containing the words to be considered.

    Returns:
    str: The proposed word for the next round of the game.
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
    """
    This function runs the Wordle game.

    Parameters:
    df (DataFrame): The DataFrame containing the words to be considered.
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
    # Load the words from a text file into a DataFrame
    df = pd.read_fwf('words.txt', names=['word'], header=None, converters={'word': str})
    # Start the Wordle game
    wordle(df)