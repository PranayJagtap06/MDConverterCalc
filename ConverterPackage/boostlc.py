"""Specifications of Boost Converter.

Returning input current/ inductor current, critical inductance, inductor
rating, inductor ripple current, capcitor rating & capacitor ripple voltage
for Boost Converter.
"""

import numpy as np


def bst_duty_cycle(Vo, Vin):
    """
    Duty Cycle.
    ----------
    Vo : Output Voltage.

    Vin : Input Voltage.

    Returns
    -------
    Value of duty cycle.
    """
    return np.round(np.divide(np.subtract(float(Vo), float(Vin)), float(Vo)), decimals=3)


def bst_ind_current(D, Io):
    """
    Input Current/ Inductor Current in Boost Mode.

    Parameters
    ----------
    D : Duty cycle of converter.

    Io : Output current of converter.

    Returns
    -------
    Value of average inductor curent in converter. Roundup to two decimal places.
    """
    return np.round(np.divide(float(Io), 1-float(D)), decimals=2)


def bst_ripl_current(IL, Irp):
    """
    For Ripple Current in Boost Mode.

    Parameters
    ----------
    IL : Current through inductor in boost mode.

    Irp : Given percentage of ripple current.

    Returns
    -------
    Value of ripple current for given value of precentage ripple current.
    """
    return np.format_float_scientific(np.multiply(float(IL), float(Irp)/100), unique=False, precision=2, trim='-', exp_digits=1)


def bst_Irp(Vin, D, fsw, L):
    """
    Inductor Ripple Current.

    Parameters
    ----------
    Vin : float
        Input Voltage.
    D : float
        Duty Cycle.
    fsw : float
        Frequency.
    L : float
        Inductor value.

    Returns
    -------
    Inductor ripple current value.

    """
    return np.format_float_scientific(np.divide(np.multiply(float(Vin), float(D)), np.multiply(float(L), float(fsw))), unique=False, precision=2, trim='-', exp_digits=1)


def bst_cr_ind(D, R, fsw):
    """
    Critical Inductance in Boost Mode.

    Parameters
    ----------
    D : Duty cycle of converter.

    R : Value of output resistance.

    fsw : Frequency.

    Returns
    -------
    Value of critical indcuatance or minimum value of inductance required for
    continuous current through the inductor.
    """
    return np.format_float_scientific(np.divide(np.multiply(float(D)*np.power(1-float(D), 2), float(R)), np.multiply(2, float(fsw))), unique=False, precision=4, trim='-', exp_digits=1)


def bst_cont_ind(Vin, D, fsw, I_ripple):
    """
    Inductor Value in Boost Mode.

    Parameters
    ----------
    Vo : Output Voltage.

    D : Duty cycle of converter.

    fsw : Frequency.

    I_ripple : Ripple current.

    Returns
    -------
    Required inductor value for maintaining continuous conduction mode of converter.
    """
    return np.format_float_scientific(np.divide(np.multiply(float(Vin), float(D)), np.multiply(float(fsw), float(I_ripple))), unique=False, precision=2, trim='-', exp_digits=1)


def bst_ind_ripl_(Vin, D, fsw, L):
    """
    Inductor Ripple Current in Boost Mode.

    Parameters
    ----------
    Vin : Input Voltage.float(

 )  float( D) : Duty cycle of converter.

    fsw : Frequency.

    L : inductor value.

    Returns
    -------
    Ripple current for a given value of inductor.
    """
    return np.round(np.divide(np.multiply(float(Vin), float(D)), np.multiply(float(fsw), float(L))), decimals=2)


def bst_cap_val(D, R, Vrp, fsw):
    """
    Capacitor Value in Boost Mode.

    Parameters
    ----------
    Vo : Output Voltage.

    D : Duty cycle of converter.

    R  : Resistance.

    Vrp : Ripple voltage.

    fsw : Frequency.

    Returns
    -------
    Value of output capacitor.
    """
    return np.format_float_scientific(np.divide(float(D), np.multiply(float(R)*float(Vrp/100), float(fsw))), unique=False, precision=2, trim='-', exp_digits=1)

def Esr(Vrp, Vo, ind_rp_crnt):
    """
    Effective Series Resistance of the filte capacitor.
    
    Parameters
    ----------
    Vrp : % Ripple Voltage.
    Vo : Output Voltage.
    ind_rp_crnt : Inductor ripple current.

    Returns
    -------
    Value of ESR.
    """
    return np.round(np.divide(np.multiply(float(Vrp/100), float(Vo)), float(ind_rp_crnt)), decimals=4)
