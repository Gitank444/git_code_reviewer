from pricing import apply_discount

def send_receipt(total):
    discounted = apply_discount(total, 10)
    print(f"Receipt sent. Final amount: {discounted}")

def send_email(user, message):
    print(f"Email sent to {user}: {message}")