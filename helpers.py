import os
import random
from sys import platform as _platform


def clear_console():
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        os.system("clear")
    elif _platform == "win32" or _platform == "win64":
        os.system("cls")
    else:
        print("Your platform is unfortunately not supported, see helpers.py")


def validated_input():
    try:
        player = int(input("Please input your choice in a form of number ranging from 1 to 3: "))
        while player not in range(1, 4):
            player = int(input("Please input your choice in a form of number ranging from 1 to 3: "))
        return player
    except ValueError:
        print("Wrong value")
        validated_input()


def rock_paper_scissors():
    print("You are playing a game of rock-paper-scissors!")
    bot = random.randint(1, 3)
    player = validated_input()

    if bot == player:
        print("Draw, play again please")
        rock_paper_scissors()
    elif bot == 1 and player == 2:
        return False
    elif bot == 2 and player == 3:
        return False
    elif bot == 3 and player == 1:
        return False
    else:
        return True


def get_terminal_size():
    """ Snippet for getting size of console window. """
    """ Copied from https://stackoverflow.com/a/566752 and modified to suit my needs """
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])


if __name__ == "__main__":
    a, b = get_terminal_size()
    print(a, b)
