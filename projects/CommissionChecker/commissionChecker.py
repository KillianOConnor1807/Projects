def main():
    hourlyRate = float(input("Enter your hourly rate: "))
    hoursWorked = float(input("Enter your total hours worked for the week: "))
    sundayHours = float(input("Enter your Sunday hours worked: "))
    weeklySales = float(input("Enter your weekly sales: "))
    
    regPayHours = hoursWorked - sundayHours
    
    # get commission rate
    rate = commission(hoursWorked, weeklySales)
    
    # calculate pays
    regPay = regPayHours * hourlyRate
    sundayPay = sundayHours * hourlyRate * 1.33 
    commPay = hoursWorked * rate       # commission from sales
    totalPay = regPay + sundayPay + commPay
    
    print("\n")
    print("--- Pay ---")
    print(f"Regular Hours Pay : €{regPay:.2f}")
    print(f"Sunday Hours Pay  : €{sundayPay:.2f}")
    print(f"Commission Earned : €{commPay:.2f} (commission per hour {rate:.2f})")
    print(f"TOTAL PAY         : €{totalPay:.2f}")

def commission(total_hours, weeklySales):
    productivity = weeklySales / total_hours
    
    if total_hours >= 30:
        min_prod = 180
        min_rate = 0.2
        max_rate = 12.6
    else:
        min_prod = 210
        min_rate = 0.2
        max_rate = 12
    
    rate = 0
    if productivity >= min_prod:
        steps = (productivity - min_prod) // 10
        rate = min_rate + steps * 0.2
        rate = min(rate, max_rate)
    
    return rate
main()
