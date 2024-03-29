import numpy as np


def buck_duty_cycle(Vo, Vin):
    return np.divide(int(Vo), int(Vin))


def boost_duty_cycle(Vo, Vin):
    return np.divide(int(Vo), np.subtract(int(Vo), int(Vin)))


def buckboost_duty_cycle(Vo, Vin):
    return np.divide(int(Vo), np.add(int(Vo), int(Vin)))
