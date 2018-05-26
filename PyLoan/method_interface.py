
import os, sys
import configparser

sys.path.insert(0,"objects")
from objects.loan import Loan
from objects.loans import Loans
from objects.payment import Payment

class Method_Interface():
    def __init__(self):
        print "__init__: Not yet implemented"

    def create_payment_plan(self,loans,outputFile,monthly_payment):
        print "create_payment_plan: Not yet implemented"

    def print_results(self,loans):
        print "print_results: Not yet implemented"