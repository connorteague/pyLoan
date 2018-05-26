
import os, sys
import configparser
from calendar import monthrange

class Loan:
    def __init__(
            self,
            loan = None,
            interest_rate = None,
            unpaid_principal = None,
            unpaid_interest = None,
            minimum_payment = None
            ):
        if loan is not None:
            self.copy_constructor(loan)
            
        else:
            self.non_copy_constructor(interest_rate, unpaid_principal, unpaid_interest, minimum_payment)

    def copy_constructor(self,loan):
        self = loan

    def non_copy_constructor(self,
            interest_rate,
            unpaid_principal,
            unpaid_interest ,
            minimum_payment):
        self.interest_rate = interest_rate
        self.unpaid_principal = unpaid_principal
        self.unpaid_interest = unpaid_interest
        self.minimum_payment = minimum_payment
        self.total_paid = float()
            
    def to_string(self):
        loan_string = ",".join([
            str(self.interest_rate),
            str(self.unpaid_principal),
            str(self.unpaid_interest),
            str(self.minimum_payment),
            str(self.total_paid)
            ])
        return loan_string

    def calculate_accrued_interest(self,year,month):
        days_in_month = float(len(monthrange(year,month)))
        return  (
            self.unpaid_principal *
            days_in_month **
            (self.interest_rate / 365.25)
            )
        
    def make_payment(self, payment):
        print "Payment amount:", payment.total

        if payment.total < self.unpaid_interest:
            self.unpaid_interest -= payment.total
        else:
            remaining_payment = payment.total - self.unpaid_interest
            self.unpaid_interest = 0
            self.unpaid_principal -= remaining_payment
        remaining_balance = self.get_balance()
        if remaining_balance < 0:
            self.unpaid_interest = 0
            self.unpaid_principal = 0
            return remaining_balance * -1

        self.total_paid += payment.total

    def get_balance(self):
        return self.unpaid_principal + self.unpaid_interest

