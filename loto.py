import os
import random
from time import sleep

import keyboard


class Card:
    def __init__(self, name, first=1, last=90):
        self._name = name
        self._in_game_numbers = random.sample(range(first, last+1), 15)
        self._table = [[],
                       [],
                       []]

        for line in self._table:
            for _ in range(5):
                x = random.choice(self._in_game_numbers)
                self._in_game_numbers.remove(x)
                line.append(x)
                line.sort()
            for _ in range(4):
                line.insert(random.randint(0, 9), '  ')

    def show_card(self):
        print(f'\n{self._name:-^26}')
        for table in self._table:
            print(*table)
        print('-' * 26, '\n')

    def _num_del(self, num):
        self._num = num

        def remove(num, line):
            i = line.index(num)
            line[i] = '--'

        for line in self._table:
            if self._num in line:
                remove(self._num, line)
                return True

    def get_del_result(self, num):
        return self._num_del(num)

    def card_check(self):
        for i in self._table[0] + self._table[1] + self._table[2]:
            if str(i).isdigit():
                return False
        return True


class LotoBagIndexCount(list):
    # теперь в мешке индекс бочонка соответствует номеру бочонка
    def __getitem__(self, number):
        return list.__getitem__(self, number - 1)


if __name__ == '__main__':
    print('''Приветствуем Вас в игре "Лото"!\n
    Правила просты: каждый ход тянется бочонок из мешка и если цифра на бочонке
    совпадает с одной из цифр на вашей карточке, смело зачёркивайте ее!
    Но будьте внимательны, если выпавшей цифры нет на вашей карточке, а вы её
    зачеркнули или наоборот, то вы автоматически проигрываете. Желаем удачи!
    \nДля выхода нажмите Q\n''')

    lotobag = LotoBagIndexCount([i for i in range(1, 91)])
    user_card = Card(input('Введите ваше имя: '))
    ai_card = Card('Компьютер')


    def user_choice():
        sleep(1)
        choice = None
        print('Зачёркиваем? [Y/N]', flush=True, end='')
        while choice not in ('y', 'н') or choice not in ('n', 'т'):
            choice = keyboard.read_shortcut()
            if choice == 'y':
                print('\rВы решили зачеркнуть цифру...' + ' ' * 40, flush=True, end=' ')
                sleep(1)
                print('\r' + ' ' * 26, flush=True)
                return 'yes'
            elif choice == 'n':
                print('\rВы решили не зачёркивать цифру...' + ' ' * 40, flush=True, end=' ')
                sleep(1)
                print('\r' + ' ' * 26, flush=True, end=' ')
                return 'no'
            elif choice == 'q':
                print('\nДо свидания!')
                sleep(1)
                exit()
            else:
                print('Примите решение нажав клавиши Y или N...')


    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')


    # Реализация самой игры довольно простая, я не стал оборачивать её в класс, на мой взгляд это избыточно
    while True:
        clear_console()
        user_card.show_card()
        ai_card.show_card()
        x = random.choice(lotobag)
        lotobag.remove(x)
        print(f'\rВыпал бочонок с числом {x}, осталось бочонков: {len(lotobag)} |', end=' ')
        a = user_choice()
        ai_card.get_del_result(x)
        if a == 'yes':
            if not user_card.get_del_result(x):
                print('\nТакого числа нет в вашей карте, вы проиграли...')
                print('Попробуйте ещё раз.')
                sleep(3)
                break
            else:
                user_card.get_del_result(x)
        elif a == 'no':
            if user_card.get_del_result(x):
                print('\nВыпавшее число есть на вашей карте, а вы его не зачеркнули...')
                print('Вы проиграли. Попробуйте ещё раз.')
                sleep(3)
                break
        if user_card.card_check():
            print('\rВы победили! Поздравляем. Приходите ещё.')
            sleep(5)
            break
        if ai_card.card_check():
            print('\rУвы, вы проиграли, компьютер заполнил карточку быстрее Вас. Приходите ещё.')
            sleep(5)
            break
