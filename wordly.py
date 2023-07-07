import pandas as pd
from collections import Counter


def nextword(df):
    letterlist = []
    wdf = df.copy()
    wdf = wdf.reset_index(drop=True)

    wordlist = wdf.word.to_list()
    for word in wordlist:
        for char in word:
            letterlist.append(char)
    cletter = (Counter(letterlist).most_common(26))

    commonletters = [tup[0] for tup in cletter]

    wdf['score'] = 0

    for index, row in wdf.iterrows():
        testword = row['word']
        letterdups = []
        for c in testword:
            row['score'] += commonletters.index(c) if c in commonletters else 0
            if c in letterdups:  # if letter already in list
                wdf.at[index, 'score'] += 26
            letterdups.append(c) 

    proposal = wdf.iloc[wdf['score'].idxmin()]
    print(proposal[0])
    del wdf
    return proposal


def wordle(df):
    while len(df) > 1:
        print(f'There are {len(df)} words')
        print(f'Best Next word: {nextword(df)}')
        green = input('Enter Green matches as .X...\n')
        if green:
            df = df[df.word.str.match(f'({green})')]
            print(f'There are {len(df)} words')
        grey = input('Enter Grey misses as A|B|C\n')
        if grey:
            df = df[df.word.str.match(f"(?!.*[{grey}]).*")]
        print(f'There are {len(df)} words')
        yellow1 = input('Enter Yellow misses as A|B|C\n')
        while yellow1:
            df = df[df.word.str.match(f"(.*[{yellow1}]).*")]
            yellow2 = input('Enter Yellow positions as ..[^A|B][^[C].\n')
            df = df[df.word.str.match(f"{yellow2}")]
            yellow1 = input('Enter Yellow misses as A|B|C\n')

        print(df)
 

if __name__ == '__main__':
    header = ['word']
    df = pd.read_fwf('words.txt', names=header, types=['str'], header=None,
                     converters={h:str for h in header})
    wordle(df)
    exit()
