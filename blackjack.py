"""
Welcome to BlackJack! Get as close to 21 as you can without going over!

Game dynamics (1 dealer vs 1 player):

    1. We start with two cards face up for the player and two cards,
    one face down and one face up, for the dealer.

    2. If the player is dealt an Ace and a ten-value card, and the dealer does not,
        the player wins

    3. Dealer asks the player if he wants to Hit (get more cards)
        or Stand (stop receving)

    4. If the player exceeds a sum of 21 ("busts"), the player loses,
        even if the dealer also exceeds 21.

    5. Once the player Stands, it's the dealer's turn.

    6. The dealer then reveals the hidden card and must hit until the cards
        total up to 17 points.

    7. If the dealer exceeds 21 ("busts") and the player does not; the player wins.

    9. If the player attains a final sum higher than the dealer and does not bust;
        the player wins (and vice versa).

    10. If both dealer and player have the same sum, called a "push", no one wins
"""

import random

DECK_SUITS = 4


class ChipAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.bet = 0

    def deposit(self, bet):
        self.balance += bet

    def withdraw(self, bet):
        self.balance -= bet

    def ask_bet(self):
        while True:
            try:
                self.bet = int(input("\tWhat's your bet: "))
            except ValueError:
                print("\nInvalid input. Please enter a number")
            else:
                if not 0 < self.bet <= self.balance:
                    print("\nUnavailable balance!")
                else:
                    break


class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.sum = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)

        # Calculates the sum of cards
        if card in {"Jack", "Queen", "King"}:
            self.sum += 10
        elif card == "Ace":
            self.aces += 1
            self.sum += 11
        else:
            self.sum += card

    def adjust_sum(self):
        # Adjust the sum for any Ace in the hand
        while self.sum > 21 and self.aces:
            self.sum -= 10
            self.aces -= 1


def print_hands(player_hand, dealer_hand, hide=True):
    if hide:
        print("\nDealer's hand is: | < Hidden Card >", dealer_hand.cards[1], sep=" | ")
        print(f"{player_hand.name}'s hand is:", *player_hand.cards, sep=" | ")
    else:
        print("\nDealer's hand is:", *dealer_hand.cards, sep=" | ")
        print(f"{player_hand.name}'s hand is:", *player_hand.cards, sep=" | ")


def ask_hit_stand():
    hit_stand = ""
    while hit_stand not in {"h", "s"}:
        hit_stand = input(
            "\n\tDo you want to hit or stand? (insert 'h' or 's'): "
        ).lower()

    return hit_stand


def is_blackjack(player_hand: Hand) -> bool:
    return player_hand.sum == 21 and len(player_hand.cards) == 2


def check_win(
    player_hand: Hand,
    player_chips: ChipAccount,
    dealer_hand: Hand,
) -> bool:
    if player_hand.sum > dealer_hand.sum:
        if is_blackjack(player_hand):
            player_chips.deposit(3 / 2 * player_chips.bet)
            print("\n\t*************************************")
            print(f"\t    {player_chips.owner}, you got a BlackJack")
            print("\t You get a bonus of 3/2 times your bet")
            print("\t***************************************")

        else:
            player_chips.deposit(player_chips.bet)
            print("\n\t********************")
            print(f"\t  {player_chips.owner}, you win!")
            print("\t********************")

        return True

    elif player_hand.sum == dealer_hand.sum:
        blackjack_msg = " of BlackJacks" if is_blackjack(player_hand) else ""
        print("\n\t********************************")
        print(f"\tUff, that's a TIE{blackjack_msg}!")
        print("\t********************************")
        return True

    else:
        player_chips.withdraw(player_chips.bet)
        print("\n\t************")
        print("\tDealer Wins!")
        print("\t************")
        return True

    return False


def ask_if_should_play_again() -> bool:
    player_response = ""
    while not (player_response.startswith("y") or player_response.startswith("n")):
        player_response = input(
            "\nDo you want to play again? Enter Yes or No: "
        ).lower()
    return player_response.startswith("y")


def run():
    starting_balance = 100

    print("Welcome to BlackJack!")
    player_name = input("\tPlease, enter your name: ").capitalize()

    # Main Loop
    while True:
        print("\n" * 50)  # Add a space to the terminal window

        deck = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"] * DECK_SUITS
        random.shuffle(deck)

        # Initialize player's chips account and ask for bet:
        player_chips = ChipAccount(player_name, starting_balance)
        print(f"\nHey {player_chips.owner}, you have {player_chips.balance} chips")
        player_chips.ask_bet()

        # Initialize player and dealer's hand, and deal cards
        player_hand = Hand(player_name)
        player_hand.add_card(deck.pop())
        player_hand.add_card(deck.pop())

        dealer_hand = Hand("Dealer")
        dealer_hand.add_card(deck.pop())
        dealer_hand.add_card(deck.pop())

        # Print Cards to start game
        print_hands(player_hand, dealer_hand)

        player_hand.sum = 21
        # Check for Instant BlackJack
        if is_blackjack(player_hand):
            print_hands(player_hand, dealer_hand, hide=False)
            check_win(player_hand, player_chips, dealer_hand)
        else:
            # Player's turn
            while ask_hit_stand() == "h":
                print("\n" * 10)
                player_hand.add_card(deck.pop())
                print_hands(player_hand, dealer_hand)

                # Check for bust
                player_hand.adjust_sum()
                if player_hand.sum > 21:
                    player_chips.withdraw(player_chips.bet)
                    print("\n\t************")
                    print("\t You bust!")
                    print("\tDealer wins!")
                    print("\t************")
                    print_hands(player_hand, dealer_hand, hide=False)
                    break

            # Dealer's turn
            if player_hand.sum <= 21:
                print("\n" * 10)
                print("\n\t*** It's the Dealer's Turn! ***")
                print_hands(
                    player_hand, dealer_hand, hide=False
                )  # Reveals dealer's hidden cards

                while dealer_hand.sum < 17:
                    dealer_hand.add_card(deck.pop())
                    print_hands(player_hand, dealer_hand, hide=False)

                    # Check for bust
                    dealer_hand.adjust_sum()
                    if dealer_hand.sum > 21:
                        player_chips.deposit(player_chips.bet)
                        print("\n\t*************")
                        print("\tDealer busts!")
                        print("\t  You win!")
                        print("\t*************")
                        break

                if not dealer_hand.sum > 21:
                    check_win(player_hand, player_chips, dealer_hand)

        print(f"\nDealer's hand sum is: {dealer_hand.sum}")
        print(f"{player_name}'s hand sum is: {player_hand.sum}")

        # Print player's available balance
        starting_balance = player_chips.balance
        print(f"\n\t**** Your available balance is now: {player_chips.balance} ****")

        # Ask to play again!
        if not ask_if_should_play_again():
            print("\nBye!\n")
            return


if __name__ == "__main__":
    run()
