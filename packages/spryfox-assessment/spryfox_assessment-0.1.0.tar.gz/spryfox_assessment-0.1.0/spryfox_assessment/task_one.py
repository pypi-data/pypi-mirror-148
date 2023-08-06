from datetime import datetime


class Dummy:

    def __init__(self):
        self.__bias = None
        self.__baseline = 1/3

    @property
    def bias(self):
        return self.__bias

    def baseline(self, baseline):
        self.__baseline = baseline
    baseline = property(None, baseline)

    def calculate(self, multiplier):
        result = multiplier * self.__baseline + self.__bias
        return round(result, 3)

    def get_date(self):
        return datetime.now().strftime("%H:%M:%S %d/%m/%Y")


if __name__ == "__main__":

    d = Dummy()
    print(d.get_date())

    d.baseline = 1/12
    print("OK")
