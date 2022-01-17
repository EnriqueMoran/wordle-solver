import re

class Char:

    def __init__(self, char, code):
        self.char = char
        self.code = code    # -1: not in word 1: correct pos 2: wrong spot


class Word():

    def __init__(self, word):
        self.characters = [Char(e, 0) for e in word]
        self.text = word

    def __str__(self):
        res =  ""
        for e in self.characters:
            res += e.char
        return res

    def __eq__(self, other):
        w1 = ""
        w2 = ""
        for e in self.characters:
            w1 += e.char

        for e in other.characters:
            w2 += e.char
        return w1 == w2


class WordleSolver:

    def __init__(self, words_list_file):
        self.words_list_file = words_list_file
        self.words_list = []
        self.tried_words = []
        self.discarded_chars = []
        self.read_words_list()
        self.regexp = ""
    
    def read_words_list(self):
        with open(self.words_list_file, 'r') as f:
            self.words_list = f.read().split(',')

    def add_word(self, word):
        self.tried_words.append(word)

    def get_regexp(self):
        if self.tried_words[-1].characters[0].code == 1:
            self.regexp += f"(?=^{self.tried_words[-1].characters[0].char})"
        elif self.tried_words[-1].characters[0].code == 2:
            self.regexp += f"(?=.*{self.tried_words[-1].characters[0].char})"
            self.regexp += f"(?=^[^{self.tried_words[-1].characters[0].char}])"
        elif self.tried_words[-1].characters[0].code == -1:
            self.regexp += f"(?=^[^{self.tried_words[-1].characters[0].char}])"

        for i in range(1, 5):
            if self.tried_words[-1].characters[i].code == 1:
                self.regexp += f"(?=.{{{i}}}{self.tried_words[-1].characters[i].char})"
            elif self.tried_words[-1].characters[i].code == 2:
                self.regexp += f"(?=.*{self.tried_words[-1].characters[i].char})"
                self.regexp += f"(?=.{{{i}}}[^{self.tried_words[-1].characters[i].char}].{{{4 - i}}})"
            elif self.tried_words[-1].characters[i].code == -1:
                self.regexp += f"(?=.{{{i}}}[^{self.tried_words[-1].characters[i].char}].{{{4 - i}}})"

        processed_chars = []
        for i in range(5):
            char = self.tried_words[-1].characters[i].char
            count = 0
            for j in range(5):
                if self.tried_words[-1].characters[j].char == char and self.tried_words[-1].characters[j].code != -1:
                    count += 1
            if count > 1 and char not in processed_chars:
                self.regexp += f"(?=(.*{self.tried_words[-1].characters[i].char}){{{count},}})"
            processed_chars.append(char)
        return self.regexp

    def get_next_word(self):
        regexp = self.get_regexp() + ".*$"
        for i in range(0, 5):
            if self.tried_words[-1].characters[i].code == -1:
                self.discarded_chars.append(self.tried_words[-1].characters[i].char)

        for word in self.words_list:
            word = word.lower()
            print(regexp)
            found = re.search(regexp, word)
            if found:
                if Word(word) not in self.tried_words:
                        return word
        return None
 
if __name__ == "__main__":

    word = Word("beast")

    solver = WordleSolver("D:\\Programacion\\Python\\Wordle-solver\\wordlists\\english_wordlist.txt")
    solver.add_word(word)
    solver.discarded_chars = []
    print(solver.get_regexp())
    print(solver.get_next_word())

