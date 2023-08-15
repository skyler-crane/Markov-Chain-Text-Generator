"""
    Author: Skyler Crane

    This program takes in a .txt file as input, and builds a markov text generator based on the contents of the file

    Use:
    python3 markov.py path_to_txt_file #_words_to_generate[optional]

    Example:
    python3 markov.py independence.txt 30
    python3 markov.py independence.txt

"""

import sys
import random

def main():
    txt_file, num_words = input_file()
    word_dict = process_file(txt_file)
    sentence = generate_text(word_dict, int(num_words))

    print(sentence)

"""
Return file-name and word-count arguments after reading from command line
"""
def input_file():
    try:
        txt = sys.argv[1]
        assert txt.split(".")[-1] == "txt"
        try:
            num_words = sys.argv[2]
        except: 
            num_words = 15
        return txt, num_words

    except:
        raise Exception("Need .txt file as command-line arg")

"""
Read txt file and return a markov dictionary created from the file contents.
"""
def process_file(txt):
    # Dictionary is in form:
    # {word:[[word1, word2], [#occurences_of_word1, #occurences_of_word2]]}
    word_dict = {}
    # stores last word in line, to be held until next line of file is read
    carryover = ""
    with open(txt, "r") as f:
        for line in f:
            line_list = line.split(" ")
            # If carryover not empty string, add to beginning of list of words in line
            if carryover != "":
                line_list.insert(0, carryover)
            wc = len(line_list)
            # Go through line and format words
            for i in range(wc):
                line_list[i] = line_list[i].lower().strip(".,?!\n\t \"()[]{}:';")
            # Loop through words in line, and update markov dictionary 
            for i, word in enumerate(line_list):
                if word == "":
                    continue
                if i >= wc-1:
                    # Store word for processing in next line
                    carryover = word
                else:
                    next_word = line_list[i+1]
                    # Checks for any empty strings in list
                    if next_word == "":
                        j = i + 2 # +2 because 1 for going to next word, and 1 more for skipping the '' element
                        # loop through rest of line to try to find a valid next word
                        while j < wc and next_word == "":
                            next_word = line_list[j]
                            j+=1
                        if next_word == "":
                            carryover = word
                            break # go to next line early, no more valid words in line
                    if word in word_dict:
                        # Following word has followed this word before, so add one to its occurences
                        if next_word in word_dict[word][0]:
                            index = word_dict[word][0].index(next_word)
                            word_dict[word][1][index] = word_dict[word][1][index] + 1
                        # Following word has never followed this word before, so add new word with one occurence
                        else:
                            word_dict[word][0].append(next_word)
                            word_dict[word][1].append(1)
                    # Add new word to dictionary with whatever word follows having one occurence
                    else:
                        word_dict[word] = [[next_word], [1]]

    return word_dict

"""
Generate a string of text using a markov dictionary.

Parameters:
    word_dict (dict) -- dictionary in the following form:
        {word:[[word1, word2], [#occurences_of_word1, #occurences_of_word2]]}
    num_words (int) -- number representing number of words to generate
"""
def generate_text(word_dict, num_words=10):
    for i in range(num_words):
        # randomly choose a first word by picking a random key from dictionary
        if i == 0:
            keys = list(word_dict.keys())
            current_word = random.choice(keys)
            sentence = current_word + ' '
        # For each word, choose a following word from the list of possible following words.
        # The probability a word is chosen is weighted based on the number of times it was seen to follow that word.
        else:
            current_word = random.choices(word_dict[current_word][0], weights=word_dict[current_word][1], k=1)[0]
            sentence += current_word + ' '
    return sentence

if __name__ == "__main__":
    main()
