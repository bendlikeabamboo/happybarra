from happybarra.models import Bank

BPI = Bank("Bank of the Philippine Islands")
UNIONBANK = Bank("Unionbank")
SECURITY_BANK = Bank("Security Bank")
EASTWEST = Bank("Eastwest")
METROBANK = Bank("Metrobank")
RCBC = Bank("RCBC")
HSBC = Bank("HSBC")

if __name__ == "__main__":
    Sample = Bank("Sample")
    Sample2 = Bank("Sample2")
    print(Bank.registry)
