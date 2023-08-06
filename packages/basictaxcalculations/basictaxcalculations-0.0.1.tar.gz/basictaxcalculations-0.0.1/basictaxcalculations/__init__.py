while True:
    try:

        income = int(input("Please enter your taxable income in india: "))
    except ValueError:
        print("Please enter taxable income as a number")

        continue
    else:
        break
if income <= 250000:  #2 Lakh 50 thousand
    tax = 0
elif income <= 500000: #5 Lakh
    tax = (income - 250000) * 0.05
elif income <= 750000: #7 lakh 50 thousand
    tax = (income - 500000) * 0.10 + 12500 
elif income <= 1000000: #10 Lakh
    tax = (income - 750000) * 0.15 + 37500 
elif income <= 1250000: #12 lakh 50 thousand
    tax = (income - 1000000) * 0.20 + 75000 
elif income <= 1500000: #15 lakh
    tax = (income - 1250000) * 0.25 + 125000 
else:
    tax = (income - 1500000) * 0.30 + 187500
print("you owe", tax, "Rupees in tax!")