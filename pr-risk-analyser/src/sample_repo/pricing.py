def calculate_total(items):
    return sum(item["price"] for item in items)

def apply_discount(total, discount):
    return total - discount