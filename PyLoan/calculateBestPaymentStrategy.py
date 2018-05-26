
import os, sys
import configparser
import datetime
import importlib

sys.path.insert(0,"objects")
from objects.loan import Loan
from objects.loans import Loans
from objects.payment import Payment

NOW = datetime.datetime.now()

def load_loans(file):
    config = configparser.RawConfigParser()
    LOANS_CONFIG = config
    LOANS_CONFIG.read(file)

    loans = Loans()

    for loan in LOANS_CONFIG.sections():
        loan_name =  loan.encode("utf-8")
        loan_object = Loan( 
                        None, #first parameter is for copy constructor
                        LOANS_CONFIG.getfloat(loan,"interest_rate"),
                        LOANS_CONFIG.getfloat(loan,"unpaid_principal"),
                        LOANS_CONFIG.getfloat(loan,"unpaid_interest"),
                        LOANS_CONFIG.getfloat(loan,"minimum_payment")
                        )
        loans.add_loan( loan_name,loan_object)
    return loans

def load_plugins(plugin_directory):
    plugins = dict()
    for name in os.listdir(plugin_directory):
        plugin_name, ext = os.path.splitext(name)
        if ext == '.py' and "__" not in plugin_name:
            path = os.path.dirname(sys.argv[0])
            if len(path) == 0:
                path = "."
                sys.path.append(os.path.join(path, plugin_directory))
                mod = __import__(plugin_name)
                # set the module name in the current global name space:
                plugins[plugin_name] = mod.PaymentStrategy()
    return plugins

def main():
    loans = load_loans('loans.ini')
    with open('Testfile.html','w') as outputFile:
        methods = load_plugins('payment_methods')
        
        print len(methods)
        for name in methods.keys():
            method = methods[name]
            print "\nCalculating payement plan using", name
            method.create_payment_plan(loans,outputFile,300)
            print "\nResults for", name
            method.print_results(loans)

if __name__ == '__main__':
    main()
    