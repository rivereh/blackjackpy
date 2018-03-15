"""
    CS121 W18
    BLACKJACK
    RIVER, ARON, JIN
    3/13/18
    PYTHON 3.6.4
"""

# import modules used by this program
from tkinter import *
import random
import pickle
import os

# for developers only -- shows a console version of the game used for debugging things
SHOW_DEBUG = False


# class for individual cards containing the card's
# suit, rank, and number within the unshuffled deck
class Card:
    # initialize cards values, when a card is created in the Deck
    # class, it will store the cards suit, rank, and number within the deck
    def __init__(self, suit, rank, count):
        self.suit = suit
        self.rank = rank
        self.count = count
        self.ace_value = 1
        self.ace_set = False

    # return cards suit and rank. ex. ('S5' for five of spades)
    def get_card(self):
        return self.suit + self.rank

    # return the cards rank, used later in evaluating the cards value
    def get_rank(self):
        return self.rank

    # returns the cards number within an ordered deck
    def get_count(self):
        return self.count

    # sets the card's ace value, either 1 or 11
    def set_ace_value(self, value):
        self.ace_value = value

    # returns the value that has been set for the card, if it
    # is an ace, automatically depening on the hand's total score
    # the cards value will either be 1 or 11
    def get_ace_value(self):
        return self.ace_value

    # returns whether the card has been checked as an ace card
    def get_ace_set(self):
        return self.ace_set

    # sets the card, if it contains an ace, as checked, used in fixing
    # a bug where aces that were initally added to a hand as 11 would
    # change to 1 if the hand's score got above 21
    def set_ace_set(self):
        self.ace_set = True


# class for hands used in keeping track of dealer and player's
# set of cards
class Hand:
    def __init__(self):
        # assign values to each rank, used in assigning a value to a card
        self.values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
                       'Q': 10, 'K': 10}
        
        # initialize empty cards array, used in storing hand's cards
        self.cards = []

    # function to get the current cards in the hand
    def get_hand(self):
        current_hand = ""
        for card in self.cards:
            current_hand += card.get_card()
            if card != self.cards[-1]:
                current_hand += ", "

        return current_hand

    # adds card to end of hand
    def add_card(self, card):
        self.cards.append(card)

    # function to find the value of the hand
    def get_value(self):
        value = 0
        # compare the rank of each card with the values variable and add it
        # to the hand's value
        for card in self.cards:
            rank = card.get_rank()
            value += self.values[rank]

            # check if the card is an ace, if so and if the player is under 11 in score and
            # the current card has not been checked before than add 11 to the value
            # otherwise add 1
            if rank == 'A':
                value -= 1
                if value < 11 and not card.get_ace_set():
                    card.set_ace_value(11)
                    card.set_ace_set()
                value += card.get_ace_value()

        return value


# class for handling a game's deck
class Deck:
    def __init__(self):
        # suit and ranks used in card creation
        self.suits = ['S', 'H', 'D', 'C']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        # initialize the deck's card array
        self.cards = []

        # card count is used in assigning the card image from
        # the cards folder
        card_count = 1
        # for each suit and rank create a new Card object
        # in the decks cards array with each suit and rank respectively
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank, card_count))
                card_count += 1

    # function to shuffle the current deck
    def shuffle(self):
        random.shuffle(self.cards)

    # deal_card returns the first card in the cards array
    def deal_card(self):
        return self.cards.pop(0)

    # function to return the current cards in the deck
    def get_deck(self):
        deck_list = ""
        for card in self.cards:
            deck_list += " " + card.get_card()

        return deck_list


# class containing all of the game's functions
class Blackjack:
    def __init__(self):
        # initialize game variables
        self.player_hand = 0
        self.dealer_hand = 0
        self.deck = 0
        self.player_score = 0
        self.dealer_score = 0

        self.in_game = False
        self.safe_to_clear = False

        # used with pickle in saving the dealer / player scores
        self.scores_file = "scores.data"

        # check if the scores.data file exists and if not, create an new one
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w'): pass

        # check if the scores files is larger than 0 meaning it contains data,
        # if so then set the scores saved inside the file to the dealer and
        # players score
        if os.path.getsize(self.scores_file) > 0:
            score_pickle = open(self.scores_file, 'rb')
            saved_scores = pickle.load(score_pickle)
            self.dealer_score = saved_scores[0]
            self.player_score = saved_scores[1]

        # these are used in determining what card in the hand should be
        # drawn to the screen
        self.player_card_hit_count = 1
        self.dealer_card_hit_count = 1

        # initialize the playing window
        self.window = Tk()
        self.window.title("Blackjack")

        # create menu bar
        menubar = Menu(self.window)
        self.window.config(menu=menubar)  # set windows Menu to menubar

        # create pull-down for options with Rules, Clear Scores, and Quit
        option_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=option_menu)
<<<<<<< HEAD
        option_menu.add_command(label="Blackjack Rules", command=self.show_rules)
=======
>>>>>>> c5184910608ac7d5cef357ea895f9b55695b8cad
        option_menu.add_command(label="Clear Scores", command=self.clear_scores)
        option_menu.add_separator()
        option_menu.add_cascade(label="Quit", command=self.window.quit)

        # frame and buttons for the deal/hit/stand functions
        self.button_frame = Frame(self.window)
        self.button_frame.pack()

<<<<<<< HEAD
        bt_deal = Button(self.button_frame, width = 20, height = 10, text = "Deal", command = self.deal)
        bt_hit = Button(self.button_frame, width = 20, height = 10, text = "Hit", command = self.hit)
        bt_stand = Button(self.button_frame, width = 20, height = 10, text = "Stand", command = self.stand)

        # aligning buttons in a row
        bt_deal.grid(row = 1, column = 1, pady = 10)
        bt_hit.grid(row = 1, column = 2, pady = 10)
        bt_stand.grid(row = 1, column = 3, pady = 10)
=======

        bt_deal = Button(self.frame, width=20, height=10, text="Deal", command=self.deal)
        bt_hit = Button(self.frame, width=20, height=10, text="Hit", command=self.hit)
        bt_stand = Button(self.frame, width=20, height=10, text="Stand", command=self.stand)

        bt_deal.grid(row=1, column=1, pady=10)
        bt_hit.grid(row=1, column=2, pady=10)
        bt_stand.grid(row=1, column=3, pady=10)
>>>>>>> c5184910608ac7d5cef357ea895f9b55695b8cad

        # frame for the dealer and players cards and the label 
        # and image lists, used in holding which cards should be
        # drawn to the screen
        self.dealer_frame = Frame(self.window)
        self.dealer_frame.pack()
        self.dealer_label_list = []
        self.dealer_image_list = []

        self.player_frame = Frame(self.window) 
        self.player_frame.pack()
        self.player_label_list = []
        self.player_image_list = []

        # game status GUI
        self.game_status = Label(self.window, text = "Press Deal to start!")
        self.game_status.pack()

        # frame for dealer / player status
        self.status_frame = Frame(self.window)
        self.status_frame.pack(side=LEFT)

        # dealer status GUI
        self.dealer_status = Label(self.status_frame, text="")
        self.dealer_status.pack()

        # player status GUI
        self.player_status = Label(self.status_frame, text="")
        self.player_status.pack()

        # frame for dealer / player score
        self.score_frame = Frame(self.window)
        self.score_frame.pack(side=RIGHT)

        # dealer score GUI
        self.dealer_score_label = Label(self.score_frame, text="Dealer score: %d" % self.dealer_score)
        self.dealer_score_label.pack()

        # player score GUI
        self.player_score_label = Label(self.score_frame, text="Player score: %d" % self.player_score)
        self.player_score_label.pack()

        self.window.mainloop()

    # show the rules of Blackjack
    def show_rules(self):
        help_window = Tk()  # Create a second window
        help_window.title("Rules")

        label = Label(help_window, text="\t\t\tGoal:\n\n"
                                      "Beat the dealer by gathering a hand that's as close to 21"
                      , justify=LEFT, pady=15)
        label2 = Label(help_window, text="\t\t\t               Rules:\n\n"
                                       "1. Aces can be worth 1 or 11, if the hand's hand is under 10\n"
                                       "   then 11 will be added to the hand, otherwise 1 will be added\n\n"
                                       "2. Face cards (King, Queen, Jack) are worth 10 points\n\n"
                                       "3. A player will bust when their hand exceeds 21\n\n"
                                       "4. The Dealer will deal two cards at the beginning that make up your hand\n\n"
                                       "5. The player can hit to add cards to his hand\n\n"
                                       "6. The player can stand if they are content with their hand\n\n"
                                       "7. The player can deal to start a new game", justify=LEFT, padx=50, pady=20)

        label.pack()  # Place the object of the game label in the window
        label2.pack()  # Place the rules label in the window

    # function to clear the cards from the canvas
    # and reset label text
    def clear(self):
        # start off by clearing the dealer and player
        # status UI elements
        self.dealer_status["text"] = ""
        self.player_status["text"] = ""

<<<<<<< HEAD
        # clears the player and dealers image/label list
        # and goes through each element in the label list and
        # forgets it's grid position and destroys it, otherwise
        # problems with the UI will happen when the player deals
        # a new deck
=======
>>>>>>> c5184910608ac7d5cef357ea895f9b55695b8cad
        self.player_image_list.clear()
        for i in range(0, len(self.player_hand.cards)):
            self.player_label_list[i].grid_forget()
            self.player_label_list[i].destroy()
        self.player_label_list.clear()

        self.dealer_image_list.clear()
        for i in range(0, len(self.dealer_hand.cards)):
            self.dealer_label_list[i].grid_forget()
            self.dealer_label_list[i].destroy()
        self.dealer_label_list.clear()

        # reset the card hit counts, used in figuring out which
        # card in a hand should be drawn to the screen
        self.player_card_hit_count = 1
        self.dealer_card_hit_count = 1

    # function for the clear scores option in the menu bar
    # resets dealer and player's scores and clears the
    # scores.data file and GUI labels
    def clear_scores(self):
        self.dealer_score_label["text"] = "Dealer score: 0"
        self.player_score_label["text"] = "Player score: 0"
        self.dealer_score = 0
        self.player_score = 0
        scores_to_save = [0, 0]
        score_pickle = open(self.scores_file, "wb")
        pickle.dump(scores_to_save, score_pickle)
        score_pickle.close()

    # function for deal button which resets UI elements and creates a new
    # deck for the dealer and player
    def deal(self):

        # clear the intro status text after the player deals
        self.game_status["text"] = ""

        # only allow the screen to clear after the first
        # time dealing or else scary things happen
        if self.safe_to_clear:
            self.clear()

        # set in_game to true which allows the user to
        # active the hit and stand buttons
        self.in_game = True

        # create new deck and shuffle it
        self.deck = Deck()
        self.deck.shuffle()

        # initialize the dealer and players hand
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        # start the game off by adding two cards to each hand
        for i in range(2):
            self.player_hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())

        # by using the cards "count" number we can find the appropriate image from the
        # cards folder, then we add the images to the player's image list
        # which is then looped through and added to the label list which is drawn onto the canvas
        for i in range(len(self.dealer_hand.cards)):
            self.dealer_image_list.append(PhotoImage(file="cards/" +
                                                          str(self.dealer_hand.cards[i].get_count()) + ".gif"))
            self.dealer_label_list.append(Label(self.dealer_frame, image=self.dealer_image_list[i]))
            self.dealer_label_list[i].pack(side=LEFT)

        for i in range(len(self.player_hand.cards)):
            self.player_image_list.append(PhotoImage(file="cards/" +
                                                          str(self.player_hand.cards[i].get_count()) + ".gif"))
            self.player_label_list.append(Label(self.player_frame, image=self.player_image_list[i]))
            self.player_label_list[i].pack(side=LEFT)

        # after the cards have been dealt, update the dealer and player values
        # to represent the newly added cards
        self.update_values()

        # set safe to clear to true after the first deck is dealed which allows
        # the clear function to reset the UI elements
        self.safe_to_clear = True

    # if the game is currently active then hit
    def hit(self):
        if self.in_game:
            # if the player is under 21 than add a new card to their hand
            if self.player_hand.get_value() <= 21:
                self.player_hand.add_card(self.deck.deal_card())

            # draw the newly added card to the screen
            self.player_card_hit_count += 1
            self.player_image_list.append(PhotoImage(file="cards/" + str(
                self.player_hand.cards[self.player_card_hit_count].get_count()) + ".gif"))
            self.player_label_list.append(
                Label(self.player_frame, image=self.player_image_list[self.player_card_hit_count]))
<<<<<<< HEAD
            self.player_label_list[self.player_card_hit_count].pack(side = LEFT)
=======
            self.player_label_list[self.player_card_hit_count].pack(side=LEFT)
>>>>>>> c5184910608ac7d5cef357ea895f9b55695b8cad

            # update the score UI for the dealer and player
            self.update_values()

            # check if the player busted which lets the dealer win
            if self.player_hand.get_value() > 21:
                self.dealer_score += 1
                self.update_game_status("red", "Player busted, dealer wins!")
                self.in_game = False
        # if the game is not in play than prompt the user to deal a new deck to play
        else:
            self.game_status["fg"] = "red"
            self.game_status["text"] = "ERROR: Please deal a new deck to continue!"
            if SHOW_DEBUG:
                print("\nERROR: Please deal a new deck to continue!")

    # function used in updating the hand values and the UI representing it
    def update_values(self):
        self.dealer_status["text"] = "Dealer total: " + str(self.dealer_hand.get_value())
        self.player_status["text"] = "Player total: " + str(self.player_hand.get_value())
        if SHOW_DEBUG:
            print("\nDealer:", self.dealer_hand.get_hand(), "total:", self.dealer_hand.get_value())
            print("Player:", self.player_hand.get_hand(), "total:", self.player_hand.get_value())

    # function used in updating the game status and score UI
    def update_game_status(self, color, text):
        self.game_status["fg"] = "%s" % color
        self.game_status["text"] = "%s" % text
        self.dealer_score_label["text"] = "Dealer score: %s" % self.dealer_score
        self.player_score_label["text"] = "Player score: %s" % self.player_score

        # save dealer / player scores in scores.data file
        scores_to_save = [self.dealer_score, self.player_score]
        score_pickle = open(self.scores_file, "wb")
        pickle.dump(scores_to_save, score_pickle)
        score_pickle.close()

        if SHOW_DEBUG:
            print("\n%s" % text)
            print("\nDealer:", self.dealer_score, "\nPlayer:", self.player_score)

    # if the game is active then update the dealers hand and compare scores
    def stand(self):
        if self.in_game:
            # if the dealers value is under 17 than add a new card to their hand
            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.deal_card())
                # add one to the dealers card hit count, used in determining what card needs
                # to be added to the screen
                self.dealer_card_hit_count += 1

                # draw the newly added cards to the UI canvas
                self.dealer_image_list.append(
                    PhotoImage(
                        file="cards/" + str(self.dealer_hand.cards[self.dealer_card_hit_count].get_count()) + ".gif"))

                self.dealer_label_list.append(
                    Label(self.dealer_frame, image=self.dealer_image_list[self.dealer_card_hit_count]))
                self.dealer_label_list[self.dealer_card_hit_count].pack(side=LEFT)

            # update the score values
            self.update_values()

            # dealer busts if over 21
            if self.dealer_hand.get_value() > 21:
                self.player_score += 1
                self.update_game_status("green", "Dealer busted, Player wins!")
                self.in_game = False
            else:
                # if both dealer and player have equal scores than it's a tie
                if self.dealer_hand.get_value() == self.player_hand.get_value():
                    self.dealer_score += 1
                    self.player_score += 1
                    self.update_game_status("black", "Tie!")
                    self.in_game = False
                # if the dealer has a score close to 21 than the player than the dealer wins
                elif self.dealer_hand.get_value() >= self.player_hand.get_value() or self.player_hand.get_value() > 21:
                    self.dealer_score += 1
                    self.update_game_status("red", "Dealer wins!")
                # otherwise the player wins
                else:
                    self.player_score += 1
                    self.update_game_status("green", "Player wins!")
        # if the game is not in play than alert the player to deal a new deck to play
        else:
            self.game_status["fg"] = "red"
            self.game_status["text"] = "ERROR: Please deal a new deck to continue!"
            if SHOW_DEBUG:
                print("\nERROR: Please deal a new deck to continue!")


<<<<<<< HEAD
# start the game
=======
>>>>>>> c5184910608ac7d5cef357ea895f9b55695b8cad
Blackjack().deal()
