import random


def make_generals(size):
    gen = []
    for i in range(size):
        gen.append(bool(random.getrandbits(1)))
    return gen


def main():
    print(make_generals(5))


if __name__ == "__main__":
    main()
