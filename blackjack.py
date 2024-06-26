import random
import sys

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)
BACKSIDE = 'backside'


def main():
    print('''
    Welcome to Blackjack!

    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.
        5-Card Charlie: Draw five cards without busting to win automatically.
        
    Let's start the game!
    ''')

    money = 5000

    while True:
        if money <= 0:
            print("You're broke!")
            print('Thanks for playing!')
            sys.exit()

        print(f'\nYour current balance: ${money}')
        bet = get_bet(money)

        deck = get_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        print(f'Your bet: ${bet}')
        while True:
            display_hands(player_hand, dealer_hand, False)
            print()

            if get_hand_value(player_hand) > 21:
                break

            if len(player_hand) == 5 and get_hand_value(player_hand) <= 21:
                print('5-Card Charlie! You automatically win.')
                money += bet
                break

            move = get_move(player_hand, money - bet)

            if move == 'D':
                additional_bet = get_bet(min(bet, (money - bet)))
                bet += additional_bet
                print(f'Your total bet increased to ${bet}')

            if move in ('H', 'D'):
                new_card = deck.pop()
                rank, suit = new_card
                print(f'You drew a {rank} of {suit}.')
                player_hand.append(new_card)

                if len(player_hand) == 5 and get_hand_value(player_hand) <= 21:
                    print('5-Card Charlie! You automatically win.')
                    money += bet
                    break

                if get_hand_value(player_hand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        if get_hand_value(player_hand) <= 21:
            while get_hand_value(dealer_hand) < 17:
                print('Dealer hits...')
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)

                if get_hand_value(dealer_hand) > 21:
                    break
                input('Press Enter to continue...')
                print('\n\n')
                continue

        display_hands(player_hand, dealer_hand, True)

        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)

        if dealer_value > 21:
            money = update_money(money, bet, "win")
        elif (player_value > 21) or (player_value < dealer_value):
            money = update_money(money, bet, "lose")
        elif player_value > dealer_value:
            money = update_money(money, bet, "win")
        elif player_value == dealer_value:
            print('It\'s a tie, the bet is returned to you.')

        print(f'Your current balance is now ${money}')
        input('Press Enter to continue...')
        print('\n\n')


def get_bet(max_bet):
    """Ask player how much to bet for this round."""
    return get_valid_input(
        prompt=f'How much do you bet? (1-{max_bet}), or type QUIT to exit.',
        error_message=f'Invalid bet amount. Please enter a number between 1 and {max_bet}.',
        validation=lambda x: x.isdecimal() and 1 <= int(x) <= max_bet,
        convert=int
    )


def get_valid_input(prompt, error_message, validation, convert=lambda x: x):
    """General function to get valid input from the user."""
    while True:
        print(prompt)
        response = input('> ').upper().strip()
        if response == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if validation(response):
            return convert(response)
        else:
            print(error_message)


def get_deck():
    """Return a list of tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    """Show the player's and the dealer's cards. Hide the dealer's first card if ShowDealer is False"""
    print()
    if show_dealer_hand:
        print('DEALER:', get_hand_value(dealer_hand))
        display_cards(dealer_hand)
    else:
        print('DEALER: ???')
        # Hide the dealer's first card.
        display_cards([BACKSIDE] + dealer_hand[1:])

    print('PLAYER:', get_hand_value(player_hand))
    display_cards(player_hand)


def get_hand_value(cards):
    """Returns the value of the cards."""
    value = 0
    number_of_aces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            number_of_aces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    value += number_of_aces
    for i in range(number_of_aces):
        if value + 10 <= 21:
            value += 10

    return value


def display_cards(cards):
    """Display all the cards in the cards list."""
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___  '
        if card == BACKSIDE:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)


def get_move(player_hand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for stand, and 'D' for double down."""
    while True:
        moves = ['(H)it', '(S)tand']
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')

        return get_valid_input(
            prompt=', '.join(moves) + '> ',
            error_message='Invalid move. Please enter H, S, or D.',
            validation=lambda x: x in ('H', 'S', 'D') and not (x == 'D' and '(D)ouble down' not in moves)
        )


def update_money(money, bet, result):
    """Update and display the player's money based on the game result."""
    if result == "win":
        print(f'Dealer busts! You win ${bet}')
        money += bet
    elif result == "lose":
        print('You lost!')
        money -= bet
    elif result == "win":
        print(f'You won ${bet}')
        money += bet
    return money


if __name__ == '__main__':
    main()
