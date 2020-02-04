from math import log, ceil, pow, floor
import argparse

'''The credit calculator helps us to calculate the differential payment, annuity payment, credit principal and total 
periods amount. We can also see how much we overpay after paying the whole credit. 
IMPORTANT: in this project you have to parse the input arguments in the command line'''


def differential_payment():
    principal = args['principal']
    n = args['periods']
    credit_interest = args['interest']
    i = (credit_interest / 10) / (12 * 10)
    total = 0
    for m in range(1, n + 1):
        result = ceil(principal / n + i * (principal - (principal * (m - 1)) / n))
        print('Month {}: paid out {}'.format(m, result))
        total += result
    print('\nOverpayment = {}'.format(total - principal))


def annuity_payment():
    principal = args['principal']
    n = args['periods']
    credit_interest = args['interest']
    i = (credit_interest / 10) / (12 * 10)
    result = ceil(principal * ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1)))
    print('Your annuity payment = {}!'.format(result))
    print('Overpayment = {}'.format(result * n - principal))


def credit_principal():
    monthly_payment = args['payment']
    n = args['periods']
    credit_interest = args['interest']
    i = (credit_interest / 10) / (12 * 10)
    result = floor(monthly_payment / ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1)))
    print('Your credit principal = {}!'.format(result))
    print('Overpayment = {}'.format(monthly_payment * n - result))


def periods():
    principal = args['principal']
    monthly_payment = args['payment']
    credit_interest = args['interest']
    i = (credit_interest / 10) / (12 * 10)

    n = ceil(log((monthly_payment / (monthly_payment - i * principal)), 1 + i))
    if n / 12 < 1:
        print('You need {} months to repay this credit!'.format(int(n % 12)))
    elif n % 12 == 0:
        print('You need {} years to repay this credit!'.format(int(n / 12)))
    else:
        print('You need {} years and {} months to repay this credit!'.format(int(n // 12), int(n % 12)))
    print('Overpayment = {}'.format(monthly_payment * n - principal))


parser = argparse.ArgumentParser(description='Credit calculator parameters')
parser.add_argument('--type', type=str, help='Type of operation (diff or annuity)')
parser.add_argument('--principal', type=int, help='Credit principal')
parser.add_argument('--periods', type=int, help='Total periods (usually months)')
parser.add_argument('--interest', type=float, help='Credit interest')
parser.add_argument('--payment', type=int, help='Payment per period')
args = vars(parser.parse_args())

if any((args.values())) < 0 or all((args['type'] == 'diff', args['payment']) or len(args) < 4):
    print('Incorrect parameters')
    pass
else:
    if args['type'] == 'diff':
        differential_payment()
    elif args['type'] == 'annuity':
        if all((args['principal'], args['periods'], args['interest'])):
            annuity_payment()
        elif all((args['payment'], args['periods'], args['interest'])):
            credit_principal()
        elif all((args['principal'], args['payment'], args['interest'])):
            periods()
        else:
            print('Incorrect parameters')
    else:
        print('Incorrect parameters')
