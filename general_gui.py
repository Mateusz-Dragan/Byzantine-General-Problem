from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from project import Blockchain
import random


# funkcja na szukanie generała pod odpowiednim id
def search_general(arr, id):
    for x in arr:
        if x.id == id:
            return x.id, x.isTraitor


# funkcja na podjęcie decyzji i rozsyłania wiadomości do następnego generała
def send_message(arr, message, id):
    for x in arr:
        if x.id == id:
            x.message = message
            x.make_decision()
            # message = x.change_message()
            return x.id, x.send_message(choices)


# funkcja na rozsyłanie wiadomości od króla do innych generałów
def king_send_message(arr, message, id):
    for x in arr:
        if x.id == id:
            x.message = message
            return x.id, x.king_send_message(), x.check_king_decision()


# funkcja na otrzymanie wiadomości przez generałów
def receive_message(arr, id, message):
    for x in arr:
        if x.id == id:
            x.received_message = message
            return x.id, x.received_message


# funkcja na wybranie króla
def make_king(arr, id):
    for x in arr:
        if x.id == id:
            x.isKing = True
            return x.id


# funkcja na wyszukanie króla
def search_king(arr):
    for x in arr:
        if x.isKing:
            return x.id


# funkcja na usunięcie króla
def delete_king(arr):
    for x in arr:
        if x.isKing:
            x.isKing = False


# lista decyzji jakie generałowie mogą się podjąć
choices = ['Atak o 8 rano', 'Atak o 7 rano', 'Atak o 6 rano', 'Atak o 5 rano', 'Atak o 4 rano', 'Atak o 3 rano',
           'Atak o 9 rano', 'Atak o 5 w nocy', 'Atak o 6 w nocy', 'Atak o 7 w nocy', 'Atak o północy',
           'Atak o 11 w nocy', 'Powrót']


# klas gui i całość symulacji problemu bizantyjskich generałów
class GeneralGUI:
    def __init__(self, master, gen, amount_of_generals):
        myFrame = Frame(master)
        myFrame.pack()

        coordsx = [0, 530, 530, 530, 0, 0]
        lcoordsy = [0, 0, 290, 550, 550, 290]
        scoordsy = [24, 24, 314, 574, 574, 314]
        rcoordsy = [48, 48, 338, 598, 598, 338]
        self.message = ''
        self.myblockchain = Blockchain()
        self.gen = gen
        self.decision = ''
        self.check = 1
        self.checkTraitor = True
        self.count = 0
        self.genlabel = []
        self.gensend = []
        self.genreceive = []
        self.i = 0
        self.X = []
        self.Yfalse = []
        self.Ztrue = []
        self.king = 0
        self.baza = Label(master,
                          text='********\n'
                               'Obóz Wroga\n'
                               '********',
                          font='20',
                          bg='#FF0000',
                          fg='#000000')
        self.baza.place(x=250, y=290)

        i = 0
        while i < amount_of_generals:
            self.genlabel.append(Label(master,
                                       text="General " + str(search_general(self.gen, i + 1)[0]),
                                       font='20',
                                       bg='#808080',
                                       fg='#FFFFFF'))
            self.genlabel[i].place(x=coordsx[i], y=lcoordsy[i])
            self.gensend.append(Label(master,
                                      text='                 ',
                                      font='20',
                                      bg='blue',
                                      fg='white'))
            self.gensend[i].place(x=coordsx[i], y=scoordsy[i])
            self.genreceive.append(Label(master,
                                         text='                 ',
                                         font='20',
                                         bg='blue',
                                         fg='white'))
            self.genreceive[i].place(x=coordsx[i], y=rcoordsy[i])

            i += 1
        self.decisionLabel = Label(master, text='                 ',
                                   font='20',
                                   bg='white')
        self.decisionLabel.place(x=260, y=130)
        self.finalLabel = Label(master, text='                 ',
                                font='20',
                                bg='white')
        self.finalLabel.place(x=260, y=160)
        self.myButton = Button(master, text="Click", command=self.clicker)
        self.myButton.place(x=280, y=100)
        self.myButton2 = Button(master, text="Show Traitor", command=self.show_loyalty)
        self.myButton2.place(x=260, y=200)
        self.myButton3 = Button(master, text="Get Statistics", command=self.show_statistics)
        self.myButton3.place(x=257, y=500)

    # funkcja na czyszczenie symulacji
    def clean(self):
        i = 0
        while i < 6:
            self.gensend[i].configure(text='                 ')
            self.genreceive[i].configure(text='                 ')

            i += 1

    # funkcja która jest przypisana do przycisku i za każdym kliknięciem przycisku odbywa się kolejny krok symulacji rozsyłania wiadomości pomiędzy generałami
    def clicker(self):
        if self.i < 6:
            if self.i == 0:
                self.message = random.choice(choices)
            sender = send_message(self.gen, self.message, self.i + 1)
            receiver = receive_message(self.gen, self.i + 2, sender[1])
            self.gensend[self.i].configure(text=sender[1])
            if self.i == 5:
                value = self.genreceive[0]
                value = value.configure(text=sender[1])
            else:
                self.genreceive[self.i + 1].configure(text=receiver[1])
            if self.i == 5:
                self.myblockchain.create_block_from_transaction(
                    ["Generał", str(sender[0]), "sent", str(sender[1]), "to Generał",
                     str(receive_message(self.gen, 1, sender[1])[0])],
                    self.message)
            else:
                self.myblockchain.create_block_from_transaction(
                    ["Generał", str(sender[0]), "sent", str(sender[1]), "to Generał", str(receiver[0])], self.message)
            self.message = sender[1]
        if self.i == 6:
            f = 0
            t = 0
            for x in self.gen:
                if x.decision:
                    t += 1
                else:
                    f += 1
            decision = []
            for x in self.gen:
                decision.append(x.decision)
            for x in self.gen:
                x.other_generals = decision
                x.count_majority()
            if t / f > 1:
                self.decisionLabel.configure(text=self.message)
                self.finalLabel.configure(text="Decyzja została wybrana")
                self.i = 0
                self.clean()
                self.decision = self.message
                self.myButton.configure(text='Spróbuj jeszcze raz', command=self.retry)
            else:
                self.decisionLabel.configure(text='Nie podjęto decyzji o ataku')
                self.i = 0
                self.decision = self.message
                self.clean()
                self.myButton.configure(text='Wybierz króla', command=self.choose_king)
            self.myblockchain.display_chain()
            self.X.append(self.message)
            self.Yfalse.append(f)
            self.Ztrue.append(t)
        else:
            self.i += 1

    # funkcja na pokazanie który generał jest zdrajcą poprzez wyświetlanie go na czerwono
    def show_loyalty(self):
        i = 0
        if self.checkTraitor == True:
            while i < 6:
                if search_general(self.gen, i + 1)[1] is not True:
                    self.gensend[i].configure(bg='red')
                    self.genreceive[i].configure(bg='red')
                i += 1
            self.checkTraitor = False
        else:
            while i < 6:
                if search_general(self.gen, i + 1)[1] is not True:
                    self.gensend[i].configure(bg='blue')
                    self.genreceive[i].configure(bg='blue')
                i += 1
            self.checkTraitor = True

    # funkcja tworząca wykresy podjętych decyzji generałów
    def show_statistics(self):

        X_axis = np.arange(len(self.X))

        plt.bar(X_axis - 0.2, self.Yfalse, 0.4, label='False')
        plt.bar(X_axis + 0.2, self.Ztrue, 0.4, label='True')

        plt.xticks(X_axis, self.X)
        plt.xlabel("Groups")
        plt.ylabel("Liczba głosów")
        plt.title("Liczba głosów przy danym poleceniu")
        plt.legend()
        plt.show()

    # funkcja na wybranie króla
    def choose_king(self):
        # for x in self.gen:
        #     if x.id == 1:
        #         print(x.other_generals)
        self.decisionLabel.configure(text="                 ")
        self.king = make_king(self.gen, random.randint(1, 6))
        self.genlabel[self.king - 1].configure(text='Król')
        self.myButton.configure(text='Rozpocznij', command=self.king_algorithm)
        self.i = self.king - 1

    # algorytm króla
    def king_algorithm(self):
        if self.i < 6:
            if self.i == self.king - 1 and self.check == 1:
                self.count = 0
                self.message = bool(random.getrandbits(1))
                self.myButton.configure(text='Click')
                self.check = 2
            sender = king_send_message(self.gen, self.message, self.i + 1)
            self.count += sender[2]
            receiver = receive_message(self.gen, self.i + 2, sender[1])
            text = sender[1]
            if text == 1:
                text = "True"
            else:
                text = "False"
            self.gensend[self.i].configure(text=text)
            if self.i == 5:
                value = self.genreceive[0]
                text = sender[1]
                if text == 1:
                    text = "True"
                else:
                    text = "False"
                value = value.configure(text=text)
                self.myblockchain.create_block_from_transaction(
                    ["Generał", str(sender[0]), "sent", str(sender[1]), "to Generał",
                     str(receive_message(self.gen, 1, sender[1])[0])],
                    self.message)
                self.i = 0
            else:
                text = receiver[1]
                if text == 1:
                    text = "True"
                else:
                    text = "False"
                self.genreceive[self.i + 1].configure(text=text)
                self.myblockchain.create_block_from_transaction(
                    ["Generał", str(sender[0]), "sent", str(sender[1]), "to Generał", str(receiver[0])], self.message)
                self.i += 1
            if self.i == self.king - 1 and self.check == 2:
                if self.count > 3:
                    self.check = 1
                    self.delete_king()
                    self.confirm()
                    self.myButton.configure(text='Spróbuj jeszcze raz', command=self.retry)
                else:
                    self.clean()
                    self.check = 1
                    self.i = 0
                    self.delete_king()
                    self.gensend[self.king - 1].configure(bg='blue')
                    self.genreceive[self.king - 1].configure(bg='blue')
                    self.myButton.configure(text='Powtórz wybory', command=self.retry)
            self.message = sender[1]

    def confirm(self):
        self.decisionLabel.configure(text=self.decision)
        self.finalLabel.configure(text="Decyzja została wybrana")

    def retry(self):
        self.decisionLabel.configure(text="                 ")
        self.finalLabel.configure(text="                 ")
        self.clean()
        self.myButton.configure(text='Click', command=self.clicker)

    def delete_king(self):
        delete_king(self.gen)
        self.genlabel[self.king - 1].configure(text="General " + str(search_general(self.gen, self.king)[0]))