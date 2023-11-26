#!/usr/bin/env python3
"""
This module contains the RockPaperScissorsApp class.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import choice as random_choice

class RockPaperScissorsApp:
    """
    Constants and Attributes:

    FONT_NAME (str): The font name used for text elements in the application.
        It is set to 'Times New Roman'.

    CANVAS_BF (str): The background color of the canvas widget.
        It is set to 'indigo'.

    MODE_1P (str): Constant representing the single-player mode.
        Used to specify the game mode where the player competes against the computer.

    MODE_2P (str): Constant representing the two-player mode.
        Used to specify the game mode where two players take turns competing against each other.

    mode (str): Represents the current game mode.
        It is initialized with MODE_1P by default.

    ROCK (str): Constant representing the rock throw in the game.
        Used to identify the 'rock' hand gesture in the game.

    PAPER (str): Constant representing the paper throw in the game.
        Used to identify the 'paper' hand gesture in the game.

    SCISSORS (str): Constant representing the scissors throw in the game.
        Used to identify the 'scissors' hand gesture in the game.

    PLAYER1_WIN (str): Constant representing the result when Player 1 wins a round.
        Used to identify the outcome of a round where Player 1 emerges as the winner.

    PLAYER2_WIN (str): Constant representing the result when Player 2 wins a round.
        Used to identify the outcome of a round where Player 2 emerges as the winner.

    PLAYERS_DRAW (str): Constant representing a draw result in a round.
        Used to identify the outcome of a round where both players achieve the same result.

    best_of (int): The total number of rounds in a game session.
        Determines how many rounds will be played in a single game session. It is set to 5 by default.

    player1_score (int): The score of Player 1 in the ongoing game.
        Represents the number of rounds won by Player 1.

    player2_score (int): The score of Player 2 in the ongoing game.
        Represents the number of rounds won by Player 2.

    player1_hand (str): The current hand thrown by Player 1.
        Stores the hand gesture chosen by Player 1 for the current round. It is initially set to None.

    player2_hand (str): The current hand thrown by Player 2.
        Stores the hand gesture chosen by Player 2 for the current round. It is initially set to None.

    current_turn (bool): Indicates whose turn it is to play.
        True represents Player 1's turn, and False represents Player 2's turn.

    round_number (int): The current round number in the ongoing game.
        Keeps track of the number of rounds played.

    round_results (dict): A dictionary storing the results of each round.
        The keys are round numbers, and values represent the outcome of each round.

    who_wins (int): A counter representing the cumulative result of all rounds played.
        Positive values indicate Player 1's overall win, negative values indicate Player 2's overall win, and 0 indicates a draw.
    """

    FONT_NAME = 'Times New Roman'
    CANVAS_BF = 'indigo'

    # Modes
    MODE_1P = '1_PLAYER'
    MODE_2P = '2_PLAYER'
    mode = MODE_1P

    # Throws
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

    # Results
    PLAYER1_WIN = 'PLAYER1_WIN'
    PLAYER2_WIN = 'PLAYER2_WIN'
    PLAYERS_DRAW= 'PLAYERS_DRAW'

    # Best of how many games.
    best_of = 5

    # Holds player scores.
    player1_score = 0
    player2_score = 0

    # Holds player hands
    player1_hand = None
    player2_hand = None

    # Hold turn
    current_turn = True

    # Rounds
    round_number = 1  # Holds current round number
    round_results = {}  # Holds round result

    # Minimax kinda
    who_wins = 0

    def __init__(self):
        """
        Initialize the RockPaperScissorsApp.
        """
        self.root = ttk.Window(themename='darkly', title='Rock, Paper, Scissors', iconphoto=r'CODSOFT\Task 4 - Rock, Paper, Scissors\assets\logo.png')
        self.root.geometry('500x550')
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface.

        Returns:
        - None
        """
        self.create_canvas_widgets()
        self.create_button_widgets()
        self.root.mainloop()

    def create_canvas_widgets(self):
        """
        Creates the canvas widgets to display the throws made by players.

        Returns:
        - None
        """
        # Canvas widget - layer things on top of another
        self.canvas = ttk.Canvas(width=500, height=400, highlightthickness=0, bg=self.CANVAS_BF, autostyle=False)

        # Scoreboard
        self.player1_scoreboard = self.canvas.create_text(50, 50, text="0", fill="white", font=(self.FONT_NAME, 20, "bold"))
        self.player2_scoreboard = self.canvas.create_text(450, 50, text="0", fill="white", font=(self.FONT_NAME, 20, "bold"))

        # Logo
        self.logo = ttk.PhotoImage(file=r'CODSOFT\Task 4 - Rock, Paper, Scissors\assets\logo.png').subsample(4, 4)
        self.logo_id = self.canvas.create_image(250, 150, image=self.logo)  # Applies id to it so we can delete it later.

        # Messagebox
        self.message_box = self.canvas.create_text(250, 300, text="Player 1's turn!", fill="white", font=(self.FONT_NAME, 20, "bold"))

        self.canvas.grid(row=1, column=1, columnspan=3)

    def create_button_widgets(self):
        """
        Creates the button widgets for throwing hands.

        Returns:
        - None
        """
        # Anonymous functions used to pass intended arguments for each button.
        buttons = [
            ["Rock", lambda: self.throw_hand(hand='Rock'), "primary-outline"],
            ["Paper", lambda: self.throw_hand(hand='Paper'), "warning-outline"],
            ["Scissors", lambda: self.throw_hand(hand='Scissors'), "danger"],
            ["Another Game?", lambda: self.start_another_round(game=True), "primary-outline"],
        ]

        self.button_objects = []  # to store references to the button objects

        for index, (text_info, command_info, bootstyle_info) in enumerate(buttons):
            button = ttk.Button(self.root, text=text_info, command=command_info, style=bootstyle_info)
            if text_info == "Another Game?":
                button.grid(row=3, column=2)  # Creates reset button
                button["state"] = "disabled"  # Set the initial state to disabled
            else:
                button.grid(row=2, column=index + 1, pady=30)
            self.button_objects.append(button)  # Store the button reference

    def show_hands_thrown(self):
        """
        Updates the image used to display the tossed hand.

        Parameters:
            player(bool): Used to differentiate the player. True for P1, False for P2.
            hand(str): The hand thrown by the player.
        """
        # Player one
        self.player1_hand_image = ttk.PhotoImage(file=r"CODSOFT\Task 4 - Rock, Paper, Scissors\assets\{}.png".format(self.player1_hand)).subsample(4, 4)
        self.player1_hand_image_id = self.canvas.create_image(150, 150, image=self.player1_hand_image)

        # Player two
        self.player2_hand_image = ttk.PhotoImage(file=r"CODSOFT\Task 4 - Rock, Paper, Scissors\assets\{}.png".format(self.player2_hand)).subsample(4, 4)
        self.player2_hand_image_id = self.canvas.create_image(350, 150, image=self.player2_hand_image)

    def update_p1hand_and_current_turn(self, hand):
        """
        Updates hand thrown by player 1 and passes the turn to player 2.

        Parameters:
            hand(str): player 1's thrown hand.

        Returns:
        - None.
        """
        self.player1_hand = hand
        self.current_turn = False  # Passes turn to player 2
        print(f"Player 1: {self.player1_hand}")
        self.canvas.itemconfig(self.message_box, text="Player 2's turn")

    def throw_hand(self, hand):
        """
        Sets players current thrown hand

        Parameters:
            hand(str): player's thrown hand.

        Returns:
        - None.
        """
        hand = hand.lower()

        if self.mode == self.MODE_1P:
            self.update_p1hand_and_current_turn(hand)

            self.player2_hand = random_choice(['rock', 'paper', 'scissors'])
            self.show_hands_thrown()
            print(f"Player 2: {self.player2_hand}")
            self.check_round_winner()
        else:
            if self.player1_hand is None or self.player2_hand is None:
                if self.current_turn:
                    self.update_p1hand_and_current_turn(hand)
                else:
                    self.player2_hand = hand
                    print(f"Player 2: {self.player2_hand}")
                    self.check_round_winner()

    def check_round_winner(self):
        """
        Determines the winner of the round.

        Returns:
        - None.
        """
        # Deactivates the button so as no one can play
        for button in self.button_objects:
            button["state"] = DISABLED

        if self.player1_hand == self.ROCK and self.player2_hand == self.SCISSORS:
            self.update_result(self.PLAYER1_WIN)
        elif self.player1_hand == self.SCISSORS and self.player2_hand == self.PAPER:
            self.update_result(self.PLAYER1_WIN)
        elif self.player1_hand == self.PAPER and self.player2_hand == self.ROCK:
            self.update_result(self.PLAYER1_WIN)
        elif self.player1_hand == self.player2_hand:
            self.update_result(self.PLAYERS_DRAW)
        else:
            self.update_result(self.PLAYER2_WIN)

    def update_result(self, result):
        """
        Updates result of the round or game.

        Parameters:
            result(str): the outcome of the game.
        """
        self.round_results[self.round_number] = result
        self.canvas.delete(self.logo_id)
        self.show_hands_thrown()

        # Logs who is the winner
        if result == self.PLAYER1_WIN:
            self.canvas.itemconfig(self.message_box, text="Player 1 WINS!")
            self.player1_score += 1
            self.round_number += 1
            self.canvas.itemconfig(self.player1_scoreboard, text=self.player1_score)
        elif result == self.PLAYER2_WIN:
            self.canvas.itemconfig(self.message_box, text="Player 2 WINS!")
            self.player2_score += 1
            self.round_number += 1
            self.canvas.itemconfig(self.player2_scoreboard, text=self.player2_score)
        elif result == self.PLAYERS_DRAW:
            self.canvas.itemconfig(self.message_box, text="DRAW!")
            self.canvas.itemconfig(self.player1_scoreboard, text=self.player1_score)
            self.canvas.itemconfig(self.player2_scoreboard, text=self.player2_score)

        print(result)
        print("Game end")
        self.root.after(1300, self.reset_game)

    def reset_game(self):
        """
        Resets the game.
        """
        if self.round_number <= self.best_of:
            self.start_another_round(game=False)  # Initiates another round.
        else:
            # Totals the results
            for round_result in self.round_results:
                if self.round_results[round_result] == self.PLAYER1_WIN:
                    self.who_wins += 1
                elif self.round_results[round_result] == self.PLAYER2_WIN:
                    self.who_wins -= 1
                else:
                    self.who_wins += 0

            # Check to see who won
            if self.who_wins > 0:
                self.canvas.itemconfig(self.message_box, text="Player 1 wins best of " + str(self.best_of))
            elif self.who_wins < 0:
                self.canvas.itemconfig(self.message_box, text="Player 2 wins best of " + str(self.best_of))
            else:
                self.canvas.itemconfig(self.message_box, text="Players draw best of " + str(self.best_of))

            self.button_objects[3]["state"] = NORMAL  # Activates the reset button

    def start_another_round(self, game):
        """
        Starts another game or round.

        Parameters:
            game(bool): True if we want to initiate another game. False if round.

        Returns:
        - None
        """
        self.current_turn = True

        # Deletes the throw images on frame
        self.canvas.delete(self.player1_hand_image_id)
        self.canvas.delete(self.player2_hand_image_id)

        # Sets the logo again
        self.logo = ttk.PhotoImage(file=r'CODSOFT\Task 4 - Rock, Paper, Scissors\assets\logo.png').subsample(4,4)
        self.logo_id = self.canvas.create_image(250,150,image=self.logo) # Applies id to it so we can delete it later.

        # Setting hands to None
        self.player1_hand = None
        self.player2_hand = None

        self.canvas.itemconfig(self.message_box, text="Player 1's turn")

        if game:
            # Resets player scores.
            self.player1_score = 0
            self.player2_score = 0

            # Reset rounds
            self.round_number = 1 # Holds current round number
            self.round_results = {}

            # Resets player scoreboards
            self.canvas.itemconfig(self.player1_scoreboard, text=self.player1_score)
            self.canvas.itemconfig(self.player2_scoreboard, text=self.player2_score)

        # Activates the button so as players can play
        for button in self.button_objects:
            if button == self.button_objects[3]:
                continue
            else:
                button["state"] = NORMAL





if __name__ == '__main__':
    app = RockPaperScissorsApp()
