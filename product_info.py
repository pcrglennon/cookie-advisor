class ProductInfo():

    def __init__(self, name, price, numOwned, totalCPS):
        self.name = name
        self.price = price
        self.numOwned = numOwned
        self.totalCPS = totalCPS

    def cps(self):
        try:
            return self.totalCPS / self.numOwned
        except:
            return "ERROR"

    def marginalBenefit(self):
        try:
            return self.cps() / self.price
        except:
            return "ERROR"

    def __str__(self):
        return "{0} >> CPS: {1}, Owned: {2}, Price: {3}\nMarginal Benefit: {4}".format(self.name, self.cps(), self.numOwned, self.price, self.marginalBenefit())
