from invoice import generate_invoice
from pricing import calculate_total

def track_revenue(amount):
    return generate_invoice(amount)