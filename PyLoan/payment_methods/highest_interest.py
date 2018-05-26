
import os, sys
import configparser
import datetime
sys.path.insert(0,"..")
from method_interface import Method_Interface 

sys.path.insert(0,os.path.join('..','objects'))
from objects.payment import Payment
from objects.loan import Loan

NOW = datetime.datetime.now()

class PaymentStrategy(Method_Interface):
    def __init__(self):
        print "Highest Interest Plugin Loaded"
        self.repayment_time = int (0)

    def create_payment_plan(self,loans,outputFile,monthly_payment):
        
        month = NOW.month
        year = NOW.year

        while loans.get_total() > 0:
            highest_interest_loan = self.get_highest_interest(loans)
            print "\nNEW PAYMENT:", month, "/", year
            print "TOTAL BEFORE:", loans.get_total()
            
            remaining_payment = monthly_payment
            # pay all not highest interest loans first
            for name, loan in loans.get_all_loans():
                balance = loan.get_balance()

                if balance > 0:
                    if loan is not highest_interest_loan:
                        print "Balance on loan:",name,":",balance
                        payment = Payment(year,month,loan,loan.minimum_payment)
                        loan.make_payment(payment)
                        remaining_payment -= loan.minimum_payment
                    else:
                        highest_interest_loan_name = name
            print "Higest Interest Loan balance:", highest_interest_loan_name, ":",highest_interest_loan.get_balance()
            # use remaining payment balance to pay highest interest loan
            payment = Payment(year,month,highest_interest_loan,remaining_payment)
            left_over = highest_interest_loan.make_payment(payment)
            # if there is any payment left over, apply it to the next highest interest loan
            if left_over:
                next_highest_interest_loan = self.get_highest_interest(loans)
                if next_highest_interest_loan:
                    payment = Payment(year,month,next_highest_interest_loan,left_over)
                    next_highest_interest_loan.make_payment(payment)
                else:
                    print "Remaining balance",left_over
            print "TOTAL AFTER:", loans.get_total()
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
            
            self.repayment_time += 1
            
    def get_highest_interest(self,loans):
        highest_interest_loan = ["",float(0)]
        for name, loan in loans.get_all_loans():
            if loan.get_balance() > 0 and loan.interest_rate > highest_interest_loan[1] :
                highest_interest_loan = [ name, loan.interest_rate]
        if highest_interest_loan[0] is not "":
            return loans.get_loan(highest_interest_loan[0])

    def print_results(self,loans):
        print "Total months taken", self.repayment_time
        print "Total paid", loans.get_total_paid()