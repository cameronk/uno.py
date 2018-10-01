from Card import Card
from Constants import colors, numbers
import random

class Deck:
    def __init__(self):
        # Draw pile: lower indices are on top (0 is top card)
        self.draw_pile = self.build_and_shuffle()

        # Discard pile: higher indices are on top (n-1 is top card)
        self.discard_pile = []

    def build_and_shuffle(self):
        cards = [] # lower index = top of deck
        for color in colors:
            for number in numbers:
                if number == 0:
                    # Only create one of this card
                    cards.append(Card(number, color, len(cards)))
                else:
                    # Create two of this card
                    cards.append(Card(number, color, len(cards)))
                    cards.append(Card(number, color, len(cards)))

        # Shuffle
        random.shuffle(cards)
        return cards

    def get_draw_pile_count(self):
        return len(self.draw_pile)

    def get_top_card(self):
        count = len(self.discard_pile)
        if count == 0:
            return None
        return self.discard_pile[count - 1]

    def can_draw(self):
        return len(self.draw_pile) > 0

    def draw(self):
        if len(self.draw_pile) > 0:
            return self.draw_pile.pop(0)
        else:
            # Remove and re-shuffle all but the top discard pile card
            count_discard_pile = len(self.discard_pile)
            replacable_cards = self.discard_pile[0:count_discard_pile-2]

            random.shuffle(replacable_cards)
            self.draw_pile = self.draw_pile + replacable_cards
            
            del self.discard_pile[0:count_discard_pile-2]
            return self.draw_pile.pop(0)


    def discard(self, card):
        # Allow discarding for the first card
        if len(self.discard_pile) == 0:
            self.discard_pile.append(card)


        # Check to make sure we're allowed to discard
        top_card = self.get_top_card()
        if top_card.color == card.color or top_card.number == card.number:
            self.discard_pile.append(card)
            return True
        else:
            # print("You can't discard this card!")
            return False
