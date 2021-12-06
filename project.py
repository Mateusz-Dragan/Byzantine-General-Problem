import random


class General:

    def __init__(self, id, is_traitor=False):
        self.id = id
        self.isTraitor = is_traitor
        self.decisions = []
        self.other_generals = []
        self.majority = False
        self.majority_count = 0

    def MakeDecision(self):
        self.decision = (bool(random.getrandbits(1)))
        return self.decision

    def CountMajority(self):
        rt=0
        at=0
        for i in self.other_generals:
            if i:
                at += 1
            else:
                rt += 1
        if at > rt:
            self.majority = True
            self.majority_count = at
        else:
            self.majority = False
            self.majority_count = rt


def make_generals(size, traitor):
    gen = []
    i = 1
    while i <= size:
        if traitor > 0:
            isTraitor = (bool(random.getrandbits(1)))
            if not isTraitor:
                traitor -= 1
            else:
                pass
        else:
            isTraitor = True
        gen.append(General(i, isTraitor))
        i += 1
    for obj in gen:
        print("Generał", obj.id, obj.isTraitor)
    return gen


def count_generals(gen):
    t = 0  # liczba zdrajców
    l = 0  # liczba lojalnych
    for obj in gen:
        if obj.isTraitor:
            l += 1
        else:
            t += 1
    return l, t


def RoundOne(gen):
    collect = []
    order=False
    orders=0
    for obj in gen:
        collect.append(obj.MakeDecision())

    print(collect)
    for obj in gen:
        obj.other_generals = collect
        print(obj.other_generals)
        obj.CountMajority()
        order=obj.majority
        orders=obj.majority_count
    if orders == len(collect)/2:
        return RoundOne(gen)
    return order,orders



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
    print("Największa możliwa ilość zdrajców wśród generałów:", traitor)
    gen = make_generals(il, traitor)  # wywołanie funkcji wybierającej spośród generałów kto jest zdrajcą a kto nie i
    # przypisywanie ich do słownika
    print("Ilość lojalnych generałów:", count_generals(gen)[0])
    print("Ilość zdrajców wśród generałów:", count_generals(gen)[1])
    results = RoundOne(gen)
    order = results[0]
    order_count = results[1]
    print(order, order_count)
    command = ""
    if order:
        command = "Atakuj"
    else:
        command = "Wycofaj"
    print(command)


if __name__ == "__main__":
    main()
