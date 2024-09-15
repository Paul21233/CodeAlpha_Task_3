import tkinter as tk
from random import shuffle
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import pygame


class MemoryPuzzle:
    def __init__(self, root):
        self.timer_label = None
        self.root = root
        self.root.title("Welcome to Memory Puzzle Game")
        self.root.resizable(False, False)

        self.cards = list(range(8)) * 2  # 8 pairs of matching cards
        shuffle(self.cards)
        self.buttons = []
        self.flipped_cards = []
        self.matched_card = []
        self.start_time = time.time()
        self.time_limit = 60  # 60 sec to win the game

        # use pygame for sound
        pygame.mixer.init()
        self.flip_sound = pygame.mixer.Sound("assets/flip.mp3")
        self.match_sound = pygame.mixer.Sound("assets/90s-game-ui-6-185099.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/game_over_funny.mp3")

        # load images of cards
        self.images = [ImageTk.PhotoImage(Image.open(f"assets/image/img_{i}.png").resize((100, 100))) for i in range(8)]
        self.back_img = ImageTk.PhotoImage(Image.open("assets/image/card_back.png").resize((100, 100)))

        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        for i in range(4):
            row = []
            for j in range(4):
                btn = tk.Button(self.root, image=self.back_img, width=100, height=100,
                                command=lambda x=i, y=j: self.flip_card(x, y))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        self.timer_label = tk.Label(self.root, text="Time: 60", font=("Sans serif", 14))
        self.timer_label.grid(row=4, column=0, columnspan=4)


    def update_time(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.time_limit - elapsed_time
        self.timer_label.config(text=f"Time: {remaining_time}")

        if remaining_time <= 0:
            pygame.mixer.Sound.play(self.game_over_sound)
            self.game_over("Time's up! You lost", win=False)
        else:
            self.root.after(1000, self.update_time)

    def check_match(self):
        x1, y1 = self.flipped_cards[0]
        x2, y2 = self.flipped_cards[1]

        if self.cards[x1 * 4 + y1] == self.cards[x2 * 4 + y2]:
            pygame.mixer.Sound.play(self.match_sound)
            self.matched_card.extend(self.flipped_cards)
            self.win_condition()
        else:
            self.buttons[x1][y1].config(image=self.back_img)
            self.buttons[x2][y2].config(image=self.back_img)

        self.flipped_cards = []

    def win_condition(self):
        if len(self.matched_card) == 16:
            pygame.mixer.Sound.play(self.game_over_sound)
            self.game_over("You Won!!!", win=True)

    def game_over(self, msg, win):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

        if win:
            messagebox.showinfo("Congratulations!!!", msg)
        else:
            messagebox.showinfo("Game Over...:(", msg)
        self.reset_game()


    def reset_game(self):
        shuffle(self.cards)
        self.matched_card = []
        self.flipped_cards = []
        self.start_time = time.time()

        for row in self.buttons:
            for btn in row:
                btn.config(image=self.back_img, state="normal")

    def flip_card(self, x, y):
        if len(self.flipped_cards) < 2 and (x, y) not in self.matched_card:
            self.buttons[x][y].config(image=self.images[self.cards[x * 4 + y]])
            pygame.mixer.Sound.play(self.flip_sound)
            self.flipped_cards.append((x, y))
            if len(self.flipped_cards) == 2:
                self.root.after(500, self.check_match)


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryPuzzle(root)
    root.mainloop()
