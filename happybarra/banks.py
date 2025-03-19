from happybarra.models import Bank

BPI = Bank(name="BPI")
UNIONBANK = Bank(name="Unionbank")
SECURITY_BANK = Bank(name="Security Bank")
EASTWEST = Bank(name="Eastwest")
METROBANK = Bank(name="Metrobank")
RCBC = Bank(name="RCBC")
HSBC = Bank(name="HSBC")

if __name__ == "__main__":
    Sample = Bank("Sample")
    Sample2 = Bank("Sample2")
    print(Bank.registry)
