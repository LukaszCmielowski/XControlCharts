import pandas as pd
import numpy as np


class XControlCharts:
    """
        Calculates X Control Charts.

        :param x: list with baseline measurements
        :type x: list
    """
    def __init__(self, x, is_greater_better=True):
        self.control_consts = pd.read_csv("constants_table.csv")
        self.x = x
        self.n = len(self.x)
        self.is_greater_better = is_greater_better
        self.UCL = self.calculate_UCL()
        self.LCL = self.calculate_LCL()
        self.threshold = self.get_threshold()

    def get_threshold(self):
        return self.UCL if self.is_greater_better else self.LCL

    def get_A2_const(self):
        consts_for_n = self.control_consts[self.control_consts['n'] == self.n]
        return consts_for_n.A2.values[0]

    def calculate_UCL(self):
        return np.mean(self.x) + (np.max(self.x) - np.min(self.x)) * self.get_A2_const()

    def calculate_LCL(self):
        return np.mean(self.x) - (np.max(self.x) - np.min(self.x)) * self.get_A2_const()

    def check_limits(self, y):
        y_mean = np.mean(y)

        if self.is_greater_better:
            if y_mean > self.UCL:
                return (1-self.UCL/np.mean(y))*100
            elif self.LCL <= y_mean <= self.UCL:
                return 0
            else:
                return (1 - self.LCL / np.mean(y)) * 100
        else:
            raise NotImplementedError()


def main():
    x = [11, 13, 14]
    y = [22, 15, 20]
    xc = XControlCharts(x)
    print(xc.UCL)
    print(xc.LCL)
    print(xc.threshold)
    print(np.mean(y))
    print(xc.check_limits(y))

if __name__ == "__main__":
    main()
