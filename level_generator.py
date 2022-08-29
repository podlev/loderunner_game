import random


def level_generator():
    level_list = []

    with open('level.txt', 'w') as level:
        for y in range(1, 1000):
            if y % 3 != 0:
                s = '0' * 16
            else:
                correct = False
                while not correct and y >= 3:
                    n_b = random.randint(3, 8)
                    n_s = random.randint(0, 16 - n_b)
                    s = n_s * '0' + n_b * 'b' + (16 - n_b - n_s) * '0'
                    if level_list[y - 4].find('b') <= s.find('b') and level_list[y - 4].rfind('b') >= s.rfind('b'):
                        correct = False
                    elif level_list[y - 4].rfind('b') < s.find('b') and s.find('b') - level_list[y - 4].rfind('b') > 2:
                        correct = False
                    elif level_list[y - 4].find('b') > s.rfind('b') and level_list[y - 4].find('b') > s.rfind('b') > 2:
                        correct = False
                    else:
                        correct = True

            level_list.append(s)
        for i in range(len(level_list) - 1, 0, -1):
            left = level_list[i].find('b')
            right = level_list[i].rfind('b')
            if left != right:
                p = random.randint(left, right)
                level_list[i - 1] = p * '0' + 'g' + (16 - p - 1) * '0'

        level_list.extend(['0000000p00000000', 'b' * 16])
        level.write('\n'.join(level_list))


if __name__ == "__main__":
    level_generator()
