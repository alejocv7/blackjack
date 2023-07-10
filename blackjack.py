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

import os
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
                self.bet = int(input("\tWhat's your bet?: "))
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
        self.score = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.update_score_with_card(card)

    def update_score_with_card(self, card):
        """Updates the score adjusting for any aces"""
        if card in {"Jack", "Queen", "King"}:
            self.score += 10
        elif card == "Ace":
            self.aces += 1
            self.score += 11
        else:
            self.score += card

        # Adjust for aces
        while self.score > 21 and self.aces:
            self.score -= 10
            self.aces -= 1


def print_hands(player_hand, dealer_hand, hiden_dealer=True):
    if hiden_dealer:
        dealer_cards = f"< Hidden Card > | {dealer_hand.cards[1]}"
    else:
        dealer_cards = " | ".join(str(c) for c in dealer_hand.cards)

    print(f"\nDealer's hand is:\n\t{dealer_cards}")
    print(
        f"{player_hand.name}'s hand is:\n\t"
        f"{' | '.join(str(c) for c in player_hand.cards)}"
    )


def should_hit():
    user_ans = ""
    while user_ans not in {"h", "s"}:
        user_ans = input("\n\tDo you want to hit or stand? (type 'h' or 's'): ").lower()
    return user_ans == "h"


def should_play_again() -> bool:
    player_response = ""
    while not (player_response.startswith("y") or player_response.startswith("n")):
        player_response = input(
            "\nDo you want to play again? Enter Yes or No: "
        ).lower()
    return player_response.startswith("y")


def check_win(
    player_hand: Hand,
    player_chips: ChipAccount,
    dealer_hand: Hand,
) -> None:
    if player_hand.score == dealer_hand.score:
        print("\n\t**** Uff, that's a tie! ****")

    elif dealer_hand.score == 21 and len(dealer_hand.cards) == 2:
        print("\n\t**** 😢 Dealer wins with a blackjack! 😢 ****")
        player_chips.withdraw(player_chips.bet)

    elif player_hand.score == 21 and len(player_hand.cards) == 2:
        pay = 3 / 2 * player_chips.bet
        print(f"\n\t**** 🎉 {player_chips.owner}, you win with a BlackJack! 🎉 ****")
        print(f"\t  You get 3/2 * your bet, so {pay} chips")
        player_chips.deposit(pay)

    elif player_hand.score > 21:
        print("\n\t**** 😢 You bust! Dealer wins! 😢 ****")
        player_chips.withdraw(player_chips.bet)

    elif dealer_hand.score > 21:
        print("\n\t**** 🎉 Dealer busts! You win! 🎉 ****")
        player_chips.deposit(player_chips.bet)

    elif dealer_hand.score > player_hand.score:
        player_chips.withdraw(player_chips.bet)
        print("\n\t**** 😢 Dealer Wins! 😢 ****")

    else:
        player_chips.deposit(player_chips.bet)
        print(f"\n\t**** 🎉 {player_chips.owner}, you win! 🎉 ****")


def run():
    print("Welcome to BlackJack!")
    player_name = input("\tPlease, enter your name: ").capitalize()
    starting_balance = 100

    # Main Loop
    while True:
        os.system("clear" if os.name == "posix" else "cls")

        deck = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"] * DECK_SUITS
        random.shuffle(deck)

        # Initialize player's chips account and ask for bet:
        player_chips = ChipAccount(player_name, starting_balance)
        print(f"\nHey {player_chips.owner}, you have {player_chips.balance} chips")
        player_chips.ask_bet()

        # Initialize player and dealer's hand, and deal cards
        player_hand = Hand(player_name)
        dealer_hand = Hand("Dealer")
        for _ in range(2):
            player_hand.add_card(deck.pop())
            dealer_hand.add_card(deck.pop())
        print_hands(player_hand, dealer_hand)

        # If a natural blackjack exists then we don't need to deal anything
        if not player_hand.score == 21 or dealer_hand.score == 21:
            # Player's turn
            while player_hand.score < 21 and should_hit():
                player_hand.add_card(deck.pop())
                print_hands(player_hand, dealer_hand)

            # Dealer's turn. Reveal dealer's card
            print("\n -- Dealer's turn! --")
            while dealer_hand.score < 17 and player_hand.score <= 21:
                print_hands(player_hand, dealer_hand, hiden_dealer=False)
                dealer_hand.add_card(deck.pop())

        print_hands(player_hand, dealer_hand, hiden_dealer=False)
        check_win(player_hand, player_chips, dealer_hand)

        print(f"\nDealer's final hand sum is: {dealer_hand.score}")
        print(f"{player_name}'s final hand sum is: {player_hand.score}")

        # Print player's available balance
        starting_balance = player_chips.balance
        print(f"\n\t**** Your available balance is now: {player_chips.balance} ****")

        if not should_play_again():
            print("\nBye!\n")
            return


if __name__ == "__main__":
    run()
