from abc import ABC, abstractmethod

class Student:
    def __init__(self,name):
        self.name=name
        self.state='Fericit'

    def change_state(self, new_state):
        print(f"{self.name} si a schimbat starea din {self.state} in {new_state}")
        self.state=new_state

class Command(ABC):
    @abstractmethod
    def executa(self):
        pass

class Fericit(Command):
    def __init__(self,student):
        self.student=student

    def executa(self):
        self.student.change_state("Fericit")
