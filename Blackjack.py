"""
Welcome to BlackJack! Get as close to 21 as you can without going over! This is the dynamic of the game:

    * There is 1 dealer and 1 player. 

    1. We start with two cards face up for the player and two cards, 
    one face down and one face up for the dealer.

    2. If the player is dealt an Ace and a ten-value card, and the dealer does not, the player wins.

    3. Dealer asks the player if he wants to Hit (get more cards) or Stand (stop receving)

    4. If the player exceeds a sum of 21 ("busts"), the player loses, even if the dealer also exceeds 21.

    5. Once the player Stands, it's the dealer's turn.

    6. The dealer then reveals the hidden card and must hit until the cards total up to 17 points. 
    
    7. If the dealer exceeds 21 ("busts") and the player does not; the player wins.

    9. If the player attains a final sum higher than the dealer and does not bust; the player wins (and vice versa).

    10. If both dealer and player a hand with the same sum, called a "push", no one wins.
"""

import random
starting_balance = 100
replay_Flag = 0

class Chips_Account:

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
            except:
                print("\nSorry, that's not a correct input. Insert a number")
            else:
                if self.bet > self.balance:  
                    print('\nNot availabel balance!')
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
        if card in {'Jack', 'Queen', 'King'}:
            self.sum += 10
        elif card == 'Ace':
            self.aces += 1
            self.sum += 11
        else:
            self.sum += card

    def adjust_sum(self):
        # Adjust the sum for any Ace in the hand
        while self.sum > 21 and self.aces:
            self.sum -= 10
            self.aces -= 1

def print_hands(playerHand, dealerHand, hide = True):
    if hide:
        print("\nDealer's hand is: / < Hidden Card >", dealerHand.cards[1], sep=' / ')
        print(f"{playerHand.name}'s hand is:", *playerHand.cards, sep=' / ')
    else:
        print("\nDealer's hand is:", *dealerHand.cards, sep=' / ')
        print(f"{playerHand.name}'s hand is:", *playerHand.cards, sep=' / ')

def ask_hit_stand(playerHand):
    hit_stand = ''
    while hit_stand not in {'h', 's'}:
        hit_stand = input(
            "\n\tDo you want to hit or stand? (insert 'h' or 's'): ").lower()

    return hit_stand

def check_win(playerHand, playerChips, dealerHand, instant_BlackJack=False):

    if playerHand.sum > dealerHand.sum:
        if instant_BlackJack:
            playerChips.deposit(3/2 * playerChips.bet)
            print("\n\t*************************************")
            print(f"\t    {playerChips.owner}, you got a BlackJack")
            print(f"\t You get a bonus of 3/2 times your bet")
            print("\t***************************************")

        else:
            playerChips.deposit(playerChips.bet)
            print("\n\t********************")
            print(f"\t  {playerChips.owner}, you win!")
            print("\t********************")

    elif playerHand.sum == dealerHand.sum:

        if not instant_BlackJack:
            print("\n\t**************")
            print('\tThat is a TIE!')
            print("\t**************")
        else:
            print("\n\t*******************************")
            print("\tUff, that's a TIE of BlackJacks")
            print("\t*******************************")

    else:
        playerChips.withdraw(playerChips.bet)
        print("\n\t************")
        print('\tDealer Wins!')
        print("\t************")
   
def replay():
    replay = ''
    while not (replay.startswith('y') or replay.startswith('n')):
        replay = input(
            '\nDo you want to play again? Enter Yes or No: ').lower()

    return replay.startswith('y')

# Main Loop
while True:
    print('\n'*50)
   
    # Declare and shuffle deck
    deck = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King'] * 4
    random.shuffle(deck)

    # Welcome the game:
    print("Welcome to BlackJack!")
    if not replay_Flag:
        player_name = input("\tPlease, enter your name: ").capitalize() # Asks for player's name

    # Initialize player's chips account and ask for bet:
    player_chips = Chips_Account(player_name, starting_balance)
    print(f"\nHey {player_chips.owner}, you have {player_chips.balance} chips available")
    player_chips.ask_bet()
   
    # Initialize player and dealer's hand, and deal cards
    player_hand = Hand(player_name)
    player_hand.add_card(deck.pop())
    player_hand.add_card(deck.pop())

    dealer_hand = Hand('Dealer')
    dealer_hand.add_card(deck.pop())
    dealer_hand.add_card(deck.pop())

    # Print Cards to start game
    print_hands(player_hand, dealer_hand)

    # Check for Instant BlackJack
    if player_hand.sum == 21:
        print_hands(player_hand, dealer_hand, hide=False)
        check_win(player_hand, player_chips, dealer_hand, True)

    # This is the normal pace of the game, unless a BlackJack exits
    else:
        # Player's turn
        while ask_hit_stand(player_hand) == 'h':
            print("\n"*10)
            player_hand.add_card(deck.pop())
            print_hands(player_hand, dealer_hand)
            
            # Check for bust
            player_hand.adjust_sum()
            if player_hand.sum > 21:
                player_chips.withdraw(player_chips.bet)
                print("\n\t************")
                print('\t You bust!')
                print('\tDealer wins!')
                print("\t************")
                print_hands(player_hand, dealer_hand, hide=False)
                break

        # Start dealer's turn
        if player_hand.sum <= 21:
            
            print("\n"*10)
            print("\n\t*** It's the Dealer's Turn! ***")
            print_hands(player_hand, dealer_hand, hide=False) # Reveals dealer's hidden cards

            while dealer_hand.sum < 17:
                dealer_hand.add_card(deck.pop())
                print_hands(player_hand, dealer_hand, hide=False)

                # Check for bust
                dealer_hand.adjust_sum()
                if dealer_hand.sum > 21:                 
                    player_chips.deposit(player_chips.bet)
                    print("\n\t*************")
                    print('\tDealer busts!')
                    print('\t  You win!')
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
    if replay():
        replay_Flag = 1
        continue
    else:
        print('\nBye!\n')
        break
