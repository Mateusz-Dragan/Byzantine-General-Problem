import random


def make_generals(size):
    gen = []
    for i in range(size):
        gen.append(bool(random.getrandbits(1)))
    return gen


def count_generals(gen):
    t = 0
    l = 0
    i = 0
    while i < len(gen):
        if gen[i]:
            l += 1
        else:
            t += 1
        i += 1
    return l,t


def decide():
    decision = True

    return decision


def main():
    il = int(input("Podaj liczbę generałów: "))
    gen = make_generals(il)
    print(gen)
    print("Ilość lojalnych generałów:",count_generals(gen)[0])
    print("Ilość zdrajców wśród generałów:", count_generals(gen)[1])


if __name__ == "__main__":
    main()
