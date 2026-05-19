from analytics import track_revenue

def calculate_tax(amount):
    return amount * 0.18


def calculate_total(amount):
    tax = calculate_tax(amount)
    return amount + tax