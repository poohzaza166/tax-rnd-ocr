def calculate_income_tax(income):
    if income <= 150000:
        tax_rate = 0
    elif income <= 300000:
        tax_rate = 0.05
    elif income <= 500000:
        tax_rate = 0.10
    elif income <= 750000:
        tax_rate = 0.15
    elif income <= 1000000:
        tax_rate = 0.20
    elif income <= 2000000:
        tax_rate = 0.25
    elif income <= 4000000:
        tax_rate = 0.30
    else:
        tax_rate = 0.35

    tax = income * tax_rate
    return tax

income = float(input("Enter your annual income in Baht: "))
tax = calculate_income_tax(income)
print(f"Your income tax is: {tax} Baht")
