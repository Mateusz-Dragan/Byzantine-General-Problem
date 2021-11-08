import random


# funkcja nadająca który generał jest zdrajcą
def make_generals(size, traitor):
    gen = {}  # słownik zachowujący który z generałów jest zdrajcą a który nie
    i = 0
    while i < size:
        if traitor > 0:
            gen["Generał", i + 1] = (bool(random.getrandbits(1)))
            if not gen["Generał", i + 1]:
                traitor -= 1
            else:
                pass
        else:
            gen["Generał", i + 1] = True
        i += 1
    return gen


def count_generals(gen):
    t = 0  # liczba zdrajców
    l = 0  # liczba lojalnych
    i = 0
    while i < len(gen):
        if gen["Generał", i + 1]:
            l += 1
        else:
            t += 1
        i += 1
    return l, t


# funkcja do rozsyłania komunikaty generałom
def Command(gen, command):
    decisions = []
    i = 0
    while i < len(gen):
        if gen["Generał", i + 1] == True:
            decisions.append(True)
        else:
            decisions.append(False)
        i += 1
    return gen,decisions


# funkcja służąca do wynalezienia ilości możliwych zdrajców wśród generałów
def FindTraitorAmount(il):
    if il % 4 == 0:
        il = il - 1
    traitor = str(il / 4)
    return int(traitor[0])


def main():
    check = True
    while check:
        il = int(input("Podaj liczbę generałów (conajmniej 5): "))
        if il < 5:
            print("Podaj większą liczbę generałów\n")
        else:
            check = False

    traitor = FindTraitorAmount(il)  # ilość możliwych zdrajców wśród generałów
    gen = make_generals(il, traitor)  # wywołanie funkcji wybierającej spośród generałów kto jest zdrajcą a kto nie i
    # przypisywanie ich do słownika
    print("Generałowie:\n", gen)
    print("Ilość lojalnych generałów:", count_generals(gen)[0])
    print("Ilość zdrajców wśród generałów:", count_generals(gen)[1])
    check = True
    while check:
        command = input("Podaj komendę: ")
        print(Command(gen, command))


if __name__ == "__main__":
    main()
