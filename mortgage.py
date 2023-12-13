"""Perform fixed-rate mortgage calculations."""
from argparse import ArgumentParser
import math
import sys

def get_min_payment(balance, apr, term=30, payments=12):
    """_summary_

    Args:
        balance (_type_): _description_
        apr (_type_): _description_
        term (int, optional): _description_. Defaults to 30.
        payments (int, optional): _description_. Defaults to 12.

    Returns:
        _type_: _description_
    """    ''''''
    P = float(balance)
    apr = float(apr)
    r = apr/payments
    n = term * payments
    A = (P*r*(1+r)**n)/((1+r)**n - 1)
    return math.ceil(A)

def interest_due(balance, apr, payments=12):
    """_summary_

    Args:
        balance (_type_): _description_
        apr (_type_): _description_
        payments (int, optional): _description_. Defaults to 12.

    Returns:
        _type_: _description_
    """    ''''''
    r = apr/payments
    i = balance * r
    return i

def remaining_payments(balance, apr, target_payment, payments=12):
    """_summary_

    Args:
        balance (_type_): _description_
        apr (_type_): _description_
        target_payment (_type_): _description_
        payments (int, optional): _description_. Defaults to 12.

    Returns:
        _type_: _description_
    """    ''''''
    pay_count = 0
    while balance > 0:
        interest = interest_due(balance, apr, payments)
        monthly_payment = target_payment - interest
        balance = balance - monthly_payment
        pay_count += 1
    return pay_count
def main(balance, apr, term=30, payments=12, target_payment=None):
    """_summary_

    Args:
        balance (_type_): _description_
        apr (_type_): _description_
        term (int, optional): _description_. Defaults to 30.
        payments (int, optional): _description_. Defaults to 12.
        target_payment (_type_, optional): _description_. Defaults to None.
    """    ''''''
    
    min_payment = get_min_payment(balance, apr, term, payments)
    print("Your recommended starting minimum payment is: $",min_payment,)
    if target_payment == None:
        target_payment = min_payment
    elif target_payment < min_payment:
        print("Your target payment is less than the minimum payment"
              "for this mortgage")
        target_payment = remaining_payments(balance, apr, target_payment, 
                                            payments)
        print("If you make payments of $",target_payment, ",", 
              "you will pay off the mortgage in",payments,".")
        
        
    
        
    
    
def parse_args(arglist):
    """Parse and validate command-line arguments.
    
    This function expects the following required arguments, in this order:
    
        mortgage_amount (float): total amount of a mortgage
        annual_interest_rate (float): the annual interest rate as a value
            between 0 and 1 (e.g., 0.035 == 3.5%)
        
    This function also allows the following optional arguments:
    
        -y / --years (int): the term of the mortgage in years (default is 30)
        -n / --num_annual_payments (int): the number of annual payments
            (default is 12)
        -p / --target_payment (float): the amount the user wants to pay per
            payment (default is the minimum payment)
    
    Args:
        arglist (list of str): list of command-line arguments.
    
    Returns:
        namespace: the parsed arguments (see argparse documentation for
        more information)
    
    Raises:
        ValueError: encountered an invalid argument.
    """
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")
    
    return args
if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)