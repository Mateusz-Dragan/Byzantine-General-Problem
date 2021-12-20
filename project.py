import random
import hashlib


class Block:

    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = " ".join(transaction_list)
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.message = ""
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(Block("0", ['Genesis Block']))

    def create_block_from_transaction(self, transaction_list, message):
        previous_block_hash = self.last_block.block_hash
        self.message = message
        self.chain.append(Block(previous_block_hash, transaction_list))

    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            # print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    def display_order(self):
        print(self.message)

    @property
    def last_block(self):
        return self.chain[-1]


class General:

    def __init__(self, id, is_traitor=False):
        self.id = id
        self.isTraitor = is_traitor
        self.message = ""
        self.decisions = []
        self.other_generals = []
        self.majority = False
        self.majority_count = 0

    def change_message(self):
        if not self.isTraitor:
            return "Betrayal"
        else:
            return self.message

    def MakeDecision(self):
        self.decision = (bool(random.getrandbits(1)))
        return self.decision

    def CountMajority(self):
        rt = 0
        at = 0
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
        if i == 1:
            isTraitor = True
        else:
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
    total = t + l
    return l, t, total


# def RoundOne(gen):
#     collect = []
#     order = False
#     orders = 0
#     for obj in gen:
#         collect.append(obj.MakeDecision())
#
#     print(collect)
#     for obj in gen:
#         obj.other_generals = collect
#         print(obj.other_generals)
#         obj.CountMajority()
#         order = obj.majority
#         orders = obj.majority_count
#     if orders == len(collect) / 2:
#         return RoundOne(gen)
#     return order, orders


# funkcja służąca do wynalezienia ilości możliwych zdrajców wśród generałów
def FindTraitorAmount(il):
    if il % 4 == 0:
        il = il - 1
    traitor = str(il / 4)
    return int(traitor[0])


def send_message(arr, message, id):
    for x in arr:
        if x.id == id:
            x.message = message
            message = x.change_message()
            return x.id, message


def receive_message(arr, id):
    for x in arr:
        if x.id == id:
            return x.id


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
    amount_of_generals = count_generals(gen)[2]

    # print(gen)
    check = True
    while check:
        i = 0
        message = input("Wpisz komendę: ")
        myblockchain = Blockchain()

        while i < amount_of_generals - 1:
            sender = send_message(gen, message, i + 1)
            receiver = receive_message(gen, i + 2)
            myblockchain.create_block_from_transaction(
                ["Generał", str(sender[0]), "sent", str(sender[1]), "to Generał", str(receiver)], message)
            message = sender[1]
            i += 1

        myblockchain.display_chain()
    # results = RoundOne(gen)
    # order = results[0]
    # order_count = results[1]
    # print(order, order_count)
    # command = ""
    # if order:
    #     command = "Atakuj"
    # else:
    #     command = "Wycofaj"
    # print(command)


if __name__ == "__main__":
    main()
