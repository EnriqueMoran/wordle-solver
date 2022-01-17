import tkinter as tk

from traitlets import HasTraits, link, Unicode
from lib.WordleSolver import *


class GUI(HasTraits):

    __author__ = "EnriqueMoran"

    __version__ = "v0.1"

    _characters = Unicode()

    def __init__(self, size=(800, 530), title=None, icon=None):
        self._solver = WordleSolver("./wordlists/english_wordlist_popularity.txt")
        self._width = size[0]
        self._height = size[1]
        self._title = title
        self._icon = icon
        self._buttons = []
        self._window = tk.Tk()
        self._initialize()

    def _initialize_buttons(self):
        for i in range(6):
            buttons = []
            for j in range(5):
                button = tk.Button(self._window, text="", width=8, height=3, command=lambda row=i, column=j: self.change_code(row, column))
                button.grid(row=i, column=j, padx=1, pady=1)
                buttons.append(button)
            self._buttons.append(buttons)
        button = tk.Button(self._window, text=f"submit", width=8, height=3, command=self.submit)
        button.grid(row=7, column=2, padx=1, pady=1)
        buttons.append(button)


    def _initialize(self):
        self._window.title = self._title
        self._window.resizable(False, False)
        #self._window.iconbitmap(self._icon)
        self._initialize_buttons()
        self.initialize_solver()
        self._window.mainloop()

    def change_code(self, i, j):
        try:
            code = self._solver.tried_words[i].characters[j].code
            if code == -1 or code == 0:
                self._solver.tried_words[i].characters[j].code = 1
            elif code == 1:
                self._solver.tried_words[i].characters[j].code = 2
            elif code == 2:
                self._solver.tried_words[i].characters[j].code = -1
            self.update_buttons()
        except:
            pass

    def initialize_solver(self):
        self._solver.add_word(Word("beast"))  # Add first word
        self.update_buttons()

    def update_buttons(self):
        for i in range(len(self._solver.tried_words)):
            word = self._solver.tried_words[i]
            for j in range(5):
                color = None
                if word.characters[j].code == -1:
                    color = 'red'
                elif word.characters[j].code == 1:
                    color = 'green'
                elif word.characters[j].code == 2:
                    color = 'yellow'
                elif word.characters[j].code == 0:
                    color = 'grey'
                self._buttons[i][j].config(text=word.characters[j].char, bg=color)

    def submit(self):
        word = self._solver.get_next_word()
        if word:
            self._solver.add_word(Word(word))
        else:
            print("No word found!")
        self.update_buttons()


def main():
    gui = GUI("titulo")

if __name__ == "__main__":
    main()
    
