def process_withdrawal(account_balance, amount):
    # Bug: Missing input validation for negative transfer amount
    # Allows negative withdrawals to increase account balance!
    account_balance -= amount
    return account_balance
