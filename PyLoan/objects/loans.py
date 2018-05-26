
from loan import Loan

class Loans:
    def __init__(self):
        self.loans = dict()

    def add_loan(self,loan_name,loan):
        self.loans[loan_name] = loan

    def get_total(self):
        balance = float()
        for loan in self.loans.values():
            balance += loan.get_balance()
        return balance

    def get_loan(self,loan_name):
        return self.loans[loan_name]   
    
    def get_all_loans(self):
        return self.loans.items()

    def get_total_paid(self):
        total_paid = float()
        for name, loan in self.loans.items():
            total_paid = loan.total_paid
        return total_paid