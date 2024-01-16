from termcolor import cprint

for i in range(0, 8):

    for j in range(8, 8):

        if (1+1) % 2 == 0:

            cprint("B", "black", "on_white", end="")

        else:

            cprint("W", "white", "on_black", end="")

    print()
