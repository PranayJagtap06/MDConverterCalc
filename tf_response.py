import numpy as np
import control as ct


def buck_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float):
    """
    Buck Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """
    # num_vd = np.array([vin/d])
    # den_vd = np.array([(np.sqrt(inductor*capacitor))**2, np.sqrt(inductor*capacitor)/(resistor*np.sqrt(capacitor/inductor)), 1])
    # num_vd = np.array([vin/(d*inductor*capacitor)])
    # den_vd = np.array([1, 1/(resistor*capacitor), 1/(inductor*capacitor)])

    num_vg = np.array([d*vin/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), 1/(inductor*capacitor)])
    sys = ct.tf(num_vg, den_vg)
    print('H(s) = ', sys)
    t, y = ct.step_response(sys)
    return [t, y, sys]


def boost_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float):
    """
    Boost Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """
    # num_vd = np.array([-(vin/(1-d))*(inductor/((1-d)**2)*resistor), vin/(1-d)])
    # den_vd = np.array([(np.sqrt(inductor*capacitor)/(1-d))**2, np.sqrt(inductor*capacitor)/((1-d)**2*resistor*np.sqrt(capacitor/inductor)), 1])
    # num_vd = np.array([-vin/((1-d)*resistor*capacitor), (vin*(1-d))/(inductor*capacitor)])
    # den_vd = np.array([1, 1/(resistor*capacitor), (1-d)**2/(inductor*capacitor)])

    num_vg = np.array([(1-d)*vin/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), (1-d)**2/(inductor*capacitor)])
    sys = ct.tf(num_vg, den_vg)
    print('H(s) = ', sys)
    t, y = ct.step_response(sys)
    return [t, y, sys]


def buckboost_response(d: float, vin: float, inductor: float, capacitor: float, resistor: float):
    """
    Buck Boost Converter transfer function response.
    :param d: duty cycle.
    :param vin: input voltage of converter
    :param inductor: inductor value of converter
    :param capacitor: capacitor value of converter
    :param resistor: output resistor value
    :return: list of time vector and response of the system
    """
    # num_vd = np.array([-(vin/(d*(1-d)**2))*(inductor*d/((1-d)**2)*resistor), vin/(d*(1-d)**2)])
    # den_vd = np.array([(np.sqrt(inductor*capacitor)/(1-d))**2, np.sqrt(inductor*capacitor)/((1-d)**2*resistor*np.sqrt(capacitor/inductor)), 1])
    # num_vd = np.array([-1/((1-d)**2*resistor*capacitor), 1/(d*inductor*capacitor)])
    # den_vd = np.array([1, 1/(resistor*capacitor), (1-d)**2/(inductor*capacitor)])

    num_vg = np.array([-((1-d)*d)*vin/(inductor*capacitor)])
    den_vg = np.array([1, 1/(resistor*capacitor), (1-d)**2/(inductor*capacitor)])
    sys = ct.tf(num_vg, den_vg)
    print('H(s) = ', sys)
    t, y = ct.step_response(sys)
    return [t, y, sys]
