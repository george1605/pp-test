# Adapter

class OldPrinter:
    def print_text(self, text):
        print(f"OLD: {text}")

class NewPrinterInterface:
    def print(self, text):
        pass

class PrinterAdapter(NewPrinterInterface):
    def __init__(self, old_printer):
        self.old_printer = old_printer

    def print(self, text):
        self.old_printer.print_text(text)


# Observer

class Subject:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, data):
        for obs in self.observers:
            obs.update(data)


class Observer:
    def update(self, data):
        pass

class EmailObserver(Observer):
    def update(self, data):
        print(f"Email: {data}")
