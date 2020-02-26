import random
import pdb


class Player:
    def __init__(self, chips):
        self._chips = chips
        self.points = 0
        self._picked_cards = []
        self.bet = 0
        self.ace = 0
        self.stand = False
        self.double = True

    @property
    def chips(self):
        return self._chips

    @chips.setter
    def chips(self, value):
        if value < 0:
            print('Too big amount!')
            self.bet_coins()
        elif value == self.chips:
            print('You must have a bigger amount than zero!')
            self.bet_coins()
        else:
            self._chips = value

    def bet_coins(self):
        self.bet = input(f'Place your bet ({self.chips} available): ')
        print()
        try:
            if 0 < int(self.bet):
                self.chips -= int(self.bet)
            else:
                print('Wrong amount!')
                self.bet_coins()
        except (TypeError, ValueError):
            print('Wrong input!')
            self.bet_coins()

    def pick_card(self):
        self._picked_cards.append(cards.pop())
        self.points += values[self._picked_cards[-1].split()[0]]
        if self._picked_cards[-1].split()[0] == 'Ace':
            self.ace += 1
        if self.points == 21:
            print()
            self.show_info()
            check_win()

    def show_info(self):
        if self.ace:
            if self.points > 21:
                print('Player:', ', '.join(self._picked_cards), f'({self.points - 10 * self.ace} points)')
            elif self.points == 21:
                print('Player:', ', '.join(self._picked_cards), f'({self.points} points)')
            else:
                print('Player:', ', '.join(self._picked_cards), f'({self.points} or'
                                                                f' {self.points - 10 * self.ace} points)')
        else:
            print('Player:', ', '.join(self._picked_cards), f'({self.points} points)')

    def hit_or_stand(self):
        if self.double:
            choice = input("Press 'h' to hit, 's' to stand or 'd' to double: ")
        else:
            choice = input("Press 'h' to hit, 's' to stick: ")
        if choice == 'h':
            self.double = False
            self.pick_card()
            print()
            self.show_info()
            check_win()
        elif choice == 's':
            self.double = False
            self.stand = True
            print()
            check_win()
        elif choice == 'd':
            if self.chips - int(self.bet) >= 0:
                self.stand = True
                self.pick_card()
                print()
                self.show_info()
                check_win()
            else:
                print("You don't have enough money to double!")
                print()
                self.hit_or_stand()
        else:
            print('Unknown command!')
            self.hit_or_stand()


class Dealer:
    def __init__(self):
        self.points = 0
        self._picked_cards = []
        self.first = True
        self.ace = 0

    def pick_card(self):
        # pdb.set_trace()
        self._picked_cards.append(cards.pop())
        self.points += values[self._picked_cards[-1].split()[0]]
        if self._picked_cards[-1].split()[0] == 'Ace':
            self.ace += 1

    def show_info(self):
        if self.first:
            print('Dealer:', '<hidden card>,', self._picked_cards[-1],
                  f'({values[self._picked_cards[-1].split()[0]]} points)')
        else:
            print('Dealer:', ', '.join(self._picked_cards), f'({self.points} points)')


def check_win():
    # pdb.set_trace()
    if player.points <= 21:
        if player.points == 21:
            player.stand = True
        if not player.stand:
            player.hit_or_stand()
        else:
            if dealer.points > player.points:
                if dealer.points > 21:
                    if dealer.ace:
                        dealer.points -= 10 * dealer.ace
                        dealer.ace = 0
                        check_win()
                    dealer.first = False
                    dealer.show_info()
                    if player.double:
                        print(f'Dealer busts! You win {int(player.bet) * 3} coins.')
                        player.chips += int(player.bet) * 3
                    else:
                        print(f'Dealer busts! You win {int(player.bet)*2} coins.')
                        player.chips += int(player.bet)*2
                    play_again()
                else:
                    dealer.first = False
                    dealer.show_info()
                    if player.double:
                        print(f'Dealer wins! You lose {int(player.bet)*2} coins.')
                        player.chips -= int(player.bet)
                    else:
                        print(f'Dealer wins! You lose {player.bet} coins.')
                    play_again()
            else:
                if dealer.points < 17:
                    dealer.pick_card()
                    check_win()
                elif dealer.points == player.points:
                    dealer.first = False
                    dealer.show_info()
                    print('Push! You get your money back!')
                    player.chips += int(player.bet)
                    play_again()
    elif player.points > 21:
        if player.ace:
            player.points -= 10 * player.ace
            player.ace = 0
            check_win()
        dealer.first = False
        dealer.show_info()
        if player.double:
            print(f'You bust! You lose {int(player.bet)*2} coins.')
            player.chips -= int(player.bet)
        else:
            print(f'You bust! You lose {player.bet} coins.')
        play_again()
    dealer.first = False
    dealer.show_info()
    if player.double:
        print(f'You win! You have won {int(player.bet)*3} coins.')
        player.chips += int(player.bet)*3
    else:
        print(f'You win! You have won {int(player.bet)*2} coins.')
        player.chips += int(player.bet)*2
    play_again()


def play():
    reset()
    player.bet_coins()
    player.pick_card()
    player.pick_card()
    player.show_info()
    dealer.pick_card()
    dealer.pick_card()
    dealer.show_info()
    player.hit_or_stand()


def play_again():
    if player.chips != 0:
        again = input("\nDo you want to play again?\nPress 'y' to play again or 'n' to quit. ")
        if again == 'y':
            print()
            play()
        elif again == 'n':
            quit()
        else:
            print('Unknown command!')
            play_again()
    else:
        print('Oh no, you just lost all your money!')
        quit()


def reset():
    global cards
    player._picked_cards = []
    dealer._picked_cards = []
    player.points = 0
    dealer.points = 0
    dealer.first = True
    player.stand = False
    player.double = True
    player.ace = 0
    dealer.ace = 0
    cards = [f'{rank} of {suit}' for suit in suits for rank in ranks]
    random.shuffle(cards)


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Ace', 'Jack', 'Queen', 'King')
values = {**{ranks[i]: i + 2 for i in range(10)}, **{ranks[i + 10]: 10 for i in range(3)}}
cards = [f'{rank} of {suit}' for suit in suits for rank in ranks]
# cards = ['Six of Diamonds', 'Ten of Spades', 'Seven of Diamonds', 'Six of Clubs', 'Three of Clubs', 'Ace of Clubs', 'Two of Clubs', 'Five of Clubs']
# cards = ['Four of Spades', 'Seven of Spades', 'Two of Diamonds', 'Two of Hearts', 'Jack of Diamonds', 'Ace of Spades', 'Queen of Spades', 'Four of Spades', 'King of Clubs', 'Four of Diamonds']
player = Player(100)
dealer = Dealer()
play()
