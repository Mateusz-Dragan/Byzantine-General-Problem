import random
import hashlib
import general_gui
from tkinter import *


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


# klasa zawierająca informacje o generałach
class General:

    def __init__(self, id, is_traitor=False):
        self.id = id
        self.isTraitor = is_traitor
        self.isKing = False
        self.message = ""
        self.received_message = ""
        self.decision = True
        self.decisions = []
        self.king_decision = False
        self.other_generals = []
        self.majority = False
        self.majority_count = 0

    #funkcja na rozsyłanie wiadomosći pomiędzy generałami
    def send_message(self, choices):
        if not self.isTraitor:
            choices.remove(self.message)
            self.message = random.choice(choices)
            return self.message
        else:
            return self.message

    #funkcja na rozsyłanie wiadomosći pomiędzy generałami w algorytmie króla
    def king_send_message(self):
        if not self.isTraitor:
            return self.message
        else:
            return self.message

    # funkcja na sprawdzenie decyzji króla w algorytmie króla
    def check_king_decision(self):
        if self.majority_count > 3:
            if bool(self.message) == self.majority:
                return 1
            else:
                return 0
        else:
            return 0

    # funkcja na podjęcia decyzji przez generała
    def make_decision(self):
        self.decision = (bool(random.getrandbits(1)))
        return self.decision

    def count_majority(self):
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


# funkcja służąca do wynalezienia ilości możliwych zdrajców wśród generałów
def FindTraitorAmount(il):
    if il % 4 == 0:
        il = il - 1
    traitor = str(il / 4)
    return int(traitor[0])


# funkcja uruchamiająca gui do bizantyjskich generałów
def start(gen, amount_of_generals):
    window = Tk()

    window.config(background='Green')
    window.title('Pole Bitwy')
    window.geometry('800x800')
    e = general_gui.GeneralGUI(window, gen, amount_of_generals)
    window.mainloop()
    i = 0


def main():
    traitor = FindTraitorAmount(6)  # ilość możliwych zdrajców wśród generałów
    print("Największa możliwa ilość zdrajców wśród generałów:", traitor)
    gen = make_generals(6, traitor)  # wywołanie funkcji wybierającej spośród generałów kto jest zdrajcą a kto nie i
    print("Ilość lojalnych generałów:", count_generals(gen)[0])
    print("Ilość zdrajców wśród generałów:", count_generals(gen)[1])
    amount_of_generals = count_generals(gen)[2]

    start(gen, amount_of_generals)


if __name__ == "__main__":
    main()