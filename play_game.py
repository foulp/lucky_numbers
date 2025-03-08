from lucky_numbers import LuckyNumbers

if __name__ == '__main__':
    s = 0
    for i in range(1000):
        lucky_numbers = LuckyNumbers(nb_humans=0, nb_bots=2)
        s += lucky_numbers.play_game()
    print(s)
