from abc import ABC, abstractmethod

class Observable:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)


class DisplayObserver:
    def update(self, money: float):
        print(f"[DISPLAY] Suma curenta: {money:.2f} lei")


class ChoiceObserver:
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def update(self):
        print("[OBSERVER] A fost selectat un produs. Se anunta VendingMachineSTM")
        self.vending_machine.proceed_to_checkout()


class TakeMoneyState(ABC):
    pass


# Stare - Asteptare client
class WaitingForClient(TakeMoneyState):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def client_arrived(self):
        print("[TAKE MONEY] Clientul a sosit. Introduceti bancnote sau monede.")


class InsertMoney(TakeMoneyState):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def insert_10ban(self):
        self.state_machine.update_amount_of_money(0.1)

    def insert_50ban(self):
        self.state_machine.update_amount_of_money(0.5)

    def insert_1leu(self):
        self.state_machine.update_amount_of_money(1.0)

    def insert_5lei(self):
        self.state_machine.update_amount_of_money(5.0)

    def insert_10lei(self):
        self.state_machine.update_amount_of_money(10.0)


class TakeMoneySTM(Observable):
    def __init__(self):
        super().__init__()
        self.money = 0.0
        self.waiting_state = WaitingForClient(self)
        self.insert_money_state = InsertMoney(self)
        self.current_state = self.waiting_state

    def add_money(self, value: float):
        self.money += value
        self.notify_all(self.money)

    def update_amount_of_money(self, value: float):
        self.add_money(value)


class SelectProductState(ABC):
    @abstractmethod
    def choose(self):
        pass


class SelectProduct(SelectProductState):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def choose(self):
        print("[SELECT] Alegeti un produs.")


class CocaCola(SelectProductState):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.price = 5.5

    def choose(self):
        print(f"[SELECT] Ati selectat Coca Cola. Pret: {self.price} lei.")


class Pepsi(SelectProductState):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.price = 5

    def choose(self):
        print(f"[SELECT] Ati selectat Pepsi. Pret: {self.price} lei.")


class Sprite(SelectProductState):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.price = 4.5

    def choose(self):
        print(f"[SELECT] Ati selectat Sprite. Pret: {self.price} lei.")


class SelectProductSTM(Observable):
    def __init__(self):
        super().__init__()
        self.select_product_state = SelectProduct(self)
        self.coca_cola_state = CocaCola(self)
        self.pepsi_state = Pepsi(self)
        self.sprite_state = Sprite(self)
        self.current_state = self.select_product_state

    def choose_another_product(self, product_name: str):
        if product_name == "CocaCola":
            self.current_state = self.coca_cola_state
        elif product_name == "Pepsi":
            self.current_state = self.pepsi_state
        elif product_name == "Sprite":
            self.current_state = self.sprite_state
        else:
            self.current_state = self.select_product_state
        
        self.current_state.choose()
        self.notify_all()

class VendingMachineSTM:
    def __init__(self):
        self.take_money_stm = TakeMoneySTM()
        self.select_product_stm = SelectProductSTM()

        self.display_observer = DisplayObserver()
        self.choice_observer = ChoiceObserver(self)

        self.take_money_stm.attach(self.display_observer)
        self.select_product_stm.attach(self.choice_observer)

    def proceed_to_checkout(self):
        chosen_product = self.select_product_stm.current_state

        # Verificam daca produsul selectat este de tipul SelectProduct
        if isinstance(chosen_product, SelectProduct):
            return

        product_price = getattr(chosen_product, 'price', 0.0)
        inserted_money = self.take_money_stm.money

        if inserted_money >= product_price:
            print(f"\n--- [VENDING] Tranzactie reusita! ---")
            rest = inserted_money - product_price
            if rest > 0:
                print(f"[VENDING] Rest returnat: {rest:.2f} lei.")
            
            self.take_money_stm.money = 0.0
            self.select_product_stm.current_state = self.select_product_stm.select_product_state
        else:
            lipsa = product_price - inserted_money
            print(f"\n--- [VENDING] Fonduri insuficiente. Mai aveti nevoie de {lipsa:.2f} lei ---")
            self.take_money_stm.current_state = self.take_money_stm.insert_money_state


if __name__ == "__main__":
    automat_sucuri = VendingMachineSTM()

    print("--- Pasul 1: Inserare bani ---")
    automat_sucuri.take_money_stm.waiting_state.client_arrived()
    automat_sucuri.take_money_stm.insert_money_state.insert_5lei()
    automat_sucuri.take_money_stm.insert_money_state.insert_1leu() 

    print("\n--- Pasul 2: Selectare produs (CocaCola) ---")
    automat_sucuri.select_product_stm.choose_another_product("CocaCola")