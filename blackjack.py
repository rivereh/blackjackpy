from tkinter import *
import random
import pickle
import os

# for developers only -- shows a console version of the game used for debugging things
SHOW_DEBUG = True


# class for individual cards containing the card's
# suit, rank, and number within the unshuffled deck
class Card:
    def __init__(self, suit, rank, count):
        self.suit = suit
        self.rank = rank
        self.count = count

    def get_card(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_count(self):
        return self.count


# class for hands used in keeping track of dealer and player's
# set of cards
class Hand:
    def __init__(self):

        # assign values to each rank, used in assigning a value to a card
        self.values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
                       'Q': 10, 'K': 10}
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

    def get_cards(self):
        return self.cards

    # TODO fix ace bug
    def get_value(self):
        value = 0
        contains_ace = False

        for card in self.cards:
            rank = card.get_rank()
            value += self.values[rank]

            if rank == 'A':
                contains_ace = True

        if value < 11 and contains_ace:
            value += 10

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
        self.player_hand = 0
        self.dealer_hand = 0
        self.deck = 0
        self.in_game = False

        self.player_score = 0
        self.dealer_score = 0
        self.scoresFile = "scores.data"

        if os.path.getsize(self.scoresFile) > 0:
            scorePickle = open(self.scoresFile, 'rb')
            savedScores = pickle.load(scorePickle)
            self.dealer_score = savedScores[0]
            self.player_score = savedScores[1]


        self.player_card_hit_count = 1
        self.dealer_card_hit_count = 1

        self.window = Tk()
        self.window.title("Blackjack")

        self.frame = Frame(self.window)
        self.frame.pack()
        self.safe_to_clear = False

        bt_deal = Button(self.frame, width = 20, height = 10, text="Deal", command = self.deal)
        bt_hit = Button(self.frame, width = 20, height = 10, text="Hit", command = self.hit)
        bt_stand = Button(self.frame, width = 20, height = 10, text="Stand", command = self.stand)

        bt_deal.grid(row = 1, column = 1, pady = 10)
        bt_hit.grid(row = 1, column = 2, pady = 10)
        bt_stand.grid(row = 1, column = 3, pady = 10)

        self.dealer_frame = Frame(self.window)
        self.dealer_frame.pack()

        self.player_image_list = []
        self.player_label_list = []

        self.player_frame = Frame(self.window)
        self.player_frame.pack()

        self.dealer_image_list = []
        self.dealer_label_list = []

        # game status GUI
        self.game_status = Label(self.window, text="Press Deal to start!")
        self.game_status.pack()

        # frame for dealer / player status
        self.status_frame = Frame(self.window)
        self.status_frame.pack(side = LEFT)

        # dealer status GUI
        self.dealer_status = Label(self.status_frame, text = "")
        self.dealer_status.pack()

        # player status GUI
        self.player_status = Label(self.status_frame, text = "")
        self.player_status.pack()

        # frame for dealer / player score
        self.score_frame = Frame(self.window)
        self.score_frame.pack(side = RIGHT)

        # dealer score GUI
        self.dealer_score_label = Label(self.score_frame, text="Dealer score: %d" % self.dealer_score)
        self.dealer_score_label.pack()

        # player score GUI
        self.player_score_label = Label(self.score_frame, text="Player score: %d" % self.player_score)
        self.player_score_label.pack()

        self.window.mainloop()

    # function to clear the cards from the canvas
    # and reset label text
    def clear(self):

        self.dealer_status["text"] = ""
        self.player_status["text"] = ""
         
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

        self.player_card_hit_count = 1
        self.dealer_card_hit_count = 1

    # function for deal button which resets UI elements and creates a new
    # deck for the dealer and player
    def deal(self):
        # clear screen after first time dealing or else scary things happen
        self.game_status["text"] = ""
        if self.safe_to_clear:
            self.clear()

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

        # TODO describe this better
        # by using the cards "count" number we can find the appropriate image from the
        # cards folder, then we add the images to the player's image list
        # which is then looped through and added to the label list which is drawn onto the canvas
        for i in range(len(self.dealer_hand.cards)):
            self.dealer_image_list.append(PhotoImage(file="cards/" +
                                                          str(self.dealer_hand.cards[i].get_count()) + ".gif"))
            self.dealer_label_list.append(Label(self.dealer_frame, image=self.dealer_image_list[i]))
            self.dealer_label_list[i].pack(side = LEFT)

        for i in range(len(self.player_hand.cards)):
            self.player_image_list.append(PhotoImage(file="cards/" +
                                                          str(self.player_hand.cards[i].get_count()) + ".gif"))
            self.player_label_list.append(Label(self.player_frame, image = self.player_image_list[i]))
            self.player_label_list[i].pack(side = LEFT)

        self.update_values()

        self.safe_to_clear = True

    def hit(self):
        if self.in_game:
            if self.player_hand.get_value() <= 21:
                self.player_hand.add_card(self.deck.deal_card())

            self.player_card_hit_count += 1
            self.player_image_list.append(PhotoImage(file="cards/" + str(
                self.player_hand.cards[self.player_card_hit_count].get_count()) + ".gif"))
            self.player_label_list.append(Label(self.player_frame, image = self.player_image_list[self.player_card_hit_count]))
            self.player_label_list[self.player_card_hit_count].pack(side= LEFT)

            self.update_values()

            if self.player_hand.get_value() > 21:
                self.dealer_score += 1
                self.update_game_status("red", "Player busted, dealer wins!")
                self.in_game = False
        else:
            self.game_status["fg"] = "red"
            self.game_status["text"] = "ERROR: Please deal a new deck to continue!"
            if SHOW_DEBUG:
                print("ERROR: Please deal a new deck to continue!")

    def update_values(self):
        self.dealer_status["text"] = "Dealer total: " + str(self.dealer_hand.get_value())
        self.player_status["text"] = "Player total: " + str(self.player_hand.get_value())
        if SHOW_DEBUG:
            print("\nDealer:", self.dealer_hand.get_hand(), "total:", self.dealer_hand.get_value())
            print("Player:", self.player_hand.get_hand(), "total:", self.player_hand.get_value())

    def update_game_status(self, color, text):
        self.game_status["fg"] = "%s" % color
        self.game_status["text"] = "%s" % text
        self.dealer_score_label["text"] = "Dealer score: %s" % self.dealer_score
        self.player_score_label["text"] = "Player score: %s" % self.player_score

        scoresToSave = [self.dealer_score, self.player_score]
        scorePickle = open(self.scoresFile, "wb")
        pickle.dump(scoresToSave, scorePickle)
        scorePickle.close()

        if SHOW_DEBUG:
            print("\n%s" % text)
            print("\nDealer:", self.dealer_score, "\nPlayer:", self.player_score)

    def stand(self):
        if self.in_game:
            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.deal_card())
                self.dealer_card_hit_count += 1

                print(self.dealer_hand.cards[self.dealer_card_hit_count].get_count())
                self.dealer_image_list.append(
                    PhotoImage(file="cards/" + str(self.dealer_hand.cards[self.dealer_card_hit_count].get_count()) + ".gif"))

                self.dealer_label_list.append(Label(self.dealer_frame, image=self.dealer_image_list[self.dealer_card_hit_count]))
                self.dealer_label_list[self.dealer_card_hit_count].pack(side=LEFT)

            self.update_values()

            if self.dealer_hand.get_value() > 21:
                self.player_score += 1
                self.update_game_status("green", "Dealer busted, Player wins!")
                self.in_game = False
            else:
                if self.dealer_hand.get_value() == self.player_hand.get_value():
                    self.dealer_score += 1
                    self.player_score += 1
                    self.update_game_status("black", "Tie!")
                    self.in_game = False
                elif self.dealer_hand.get_value() >= self.player_hand.get_value() or self.player_hand.get_value() > 21:
                    self.dealer_score += 1
                    self.update_game_status("red", "Dealer wins!")
                else:
                    self.player_score += 1
                    self.update_game_status("green", "Player wins!")
        else:
            self.game_status["fg"] = "red"
            self.game_status["text"] = "ERROR: Please deal a new deck to continue!"
            if SHOW_DEBUG:
                print("ERROR: Please deal a new deck to continue!")



Blackjack().deal()

