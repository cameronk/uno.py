from Deck import Deck
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self):
        self.deck = Deck()
        self.turn_count = 0
        self.player_count = 1
        self.index = 1
        self.hands = []

    def text_header(self):
        clear()
        print("UNO!\n")
        draw_pile_count = self.deck.get_draw_pile_count()
        top_card = self.deck.get_top_card()

        if len(self.hands) == self.player_count + 1:
            com_hand_count = len(self.hands[0])
            print("COM hand: {} cards".format(com_hand_count))
        if draw_pile_count >= 0:
            print("Draw pile: {} cards".format(draw_pile_count))
        if top_card:
            print("Top card: {}".format(top_card))
        print("")

    def start(self):
        self.text_header()
        self.deal()

        has_won = False
        while has_won != True:
            self.turn_count += 1
            has_won = self.turn()

            if has_won == False:
                # Nobody won this turn, see what to do next
                next_player = self.index + 1
                if next_player > self.player_count:
                    next_player = 0 # start back at the beginning

                self.index = next_player

        player_name = "Player {}".format(self.index)
        if self.index == 0:
            player_name = "Computer"
        print("\n")
        print("{} won after {} turns!".format(player_name, self.turn_count))
        print("GG :-)\n")

    def deal(self):
        deck = self.deck

        # Number of human players
        # TODO: adapt deal function to handle more players
        for j in range(0, self.player_count+1):
            self.hands.append([])

        for i in range(0, 14):
            if i % 2 == 1:
                # give human the card
                self.hands[0].append(deck.draw())
            else:
                # give player the card
                self.hands[1].append(deck.draw())

        deck.discard(deck.draw())

    def turn(self):
        self.text_header()
        if self.index == 1:
            return self.human_turn()
        else:
            return self.computer_turn()


    def human_turn(self, message=None):
        self.text_header()

        my_hand = self.hands[self.index]
        my_hand_count = len(my_hand)

        if message:
            print(message)
        else:
            print("It's your turn. You have {} cards.".format(my_hand_count))

        self.view_hand(my_hand)
        action_str = str(input("Type a number to choose a card or action: "))

        if action_str == "D":
            new_card = self.deck.draw()
            my_hand.append(new_card)
            self.confirm("drew", my_hand, new_card)
            return self.human_turn("You drew {} last turn.".format(new_card))
        if action_str == "S":
            return self.confirm("skipped", my_hand, "your turn")
        else:
            action_int = None
            try:
                action_int = int(action_str)
            except ValueError:
                print("something went wrong")

            if action_int != None and action_int >= 0 and action_int <= my_hand_count - 1:
                # Picking a card
                card = my_hand[action_int]

                # Try to discard this card
                attempt = self.deck.discard(card)

                if attempt == True:
                    # Toss the card out of my hand
                    del my_hand[action_int]
                    if my_hand_count - 1 == 0:
                        # GG
                        return True
                    else:
                        # Not yet GG
                        return self.confirm("played", my_hand, card)
                else:
                    return self.human_turn("You can't play this card, try another!")

            else:
                return self.human_turn("This isn't a valid action!")

    def computer_turn(self):

        com_hand = self.hands[self.index]
        has_won = False
        has_played_card = False

        # Try to play available cards
        for index, card in enumerate(com_hand):
            attempt = self.deck.discard(card)

            if attempt == True:
                # Toss the card out of my hand
                del com_hand[index]
                if len(com_hand) == 0:
                    # GG
                    has_won = True
                    has_played_card = True
                    break # the for loop
                else:
                    # Not yet GG
                    has_played_card = True
                    break # the for loop

        # If the computer hasn't played a card,
        # keep drawing until we can play one
        if has_played_card == False:

            # Draw more cards until we get a match
            while has_played_card == False:
                # Draw and try to discard this card
                new_card = self.deck.draw()
                attempt = self.deck.discard(new_card)
                if attempt == True:
                    has_played_card = True
                else:
                    com_hand.append(new_card)

            return self.confirm2("Computer", "drew and played a card")

        else:
            self.confirm2("Computer", "played a card")
            return has_won

    # --- #

    def view_hand(self, hand):
        print("D: Draw a card")
        print("S: Skip your turn")
        for index, card in enumerate(hand):
            print("{}: {}".format(index, card))
        print("")

    def confirm(self, word, hand, card):
        self.text_header()
        print("You {} {}, and now have {} cards.".format(word, card, len(hand)))
        next = input("Press any key to continue...")
        return False

    def confirm2(self, who, word):
        self.text_header()
        print("{} {}.".format(who, word))
        next = input("Press any key to continue...")
        return False

def run():
    game = Game()
    game.start()

if __name__ == '__main__':
    run()
