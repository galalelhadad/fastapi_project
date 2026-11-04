def add(num1:int,num2:int):
    return num1+num2


class insuffiecient_amount(Exception):
    pass
class Bank_account():
    def __init__(self,balance:int=0):
        self.balance=balance

    def deposit(self,amount):
        self.balance+=amount

    def withdrew(self,amount):
        if amount> self.balance:
            raise insuffiecient_amount("insuffiecient amount in account")
            # raise ZeroDivisionError
        self.balance-=amount
    