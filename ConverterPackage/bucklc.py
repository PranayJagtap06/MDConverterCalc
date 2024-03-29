"""Specifications of Buck Converter.

Returning input current/ inductor current, critical inductance, inductor
rating, inductor ripple current, capcitor rating & capacitor ripple voltage
for Buck Converter.
"""

import numpy as np


def bck_duty_cycle(Vo, Vin):
    """
    Duty Cycle.
    ----------
    Vo : Output Voltage.

    Vin : Input Voltage.

    Returns
    -------
    Value of duty cycle.
    """
    return np.round(np.divide(float(Vo), float(Vin)), decimals=3)


def bck_ip_current(D, Io):
    """
    Input Current/ Inductor Current in Buck Mode.

    Parameters
    ----------
    D : Duty cycle of converter.

    Io : Output current of converter.

    Returns
    -------
    Value of average inductor curent in converter. Roundup to two decimal places.
    """
    return np.round(np.multiply(float(D), float(Io)), decimals=3)


def bck_ripl_current(IL, Irp):
    """
    For Ripple Current in Buck Mode.

    Parameters
    ----------
    IL : Current through inductor in buck mode.

    Irp : Given percentage of ripple current.

    Returns
    -------
    Value of ripple current for given value of precentage ripple current.
    """
    return np.round(np.multiply(float(IL), float(Irp/100)), decimals=3)

def bck_Irp(Vo, D, fsw, L):
    """
    Inductor Ripple Current.

    Parameters
    ----------
    Vo: float
        Output Voltage.
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
    return np.format_float_scientific(np.divide(np.multiply(float(Vo), 1-float(D)), np.multiply(float(L), float(fsw))), unique=False, precision=2, trim='-', exp_digits=1)


def bck_cr_ind(D, R, fsw):
    """
    Critical Inductance in Buck Mode.

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
    return np.format_float_scientific(np.divide(np.multiply(1-float(D), float(R)), np.multiply(2, float(fsw))), unique=False, precision=4, trim='-', exp_digits=1)


def bck_cont_ind(Vo, D, fsw, I_ripple):
    """
    Inductor Value in Buck Mode.

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
    return np.format_float_scientific(np.divide(np.multiply(float(Vo), 1-float(D)), np.multiply(float(fsw), float(I_ripple))), unique=False, precision=2, trim='-', exp_digits=1)


def bck_ind_ripl_(Vo, D, fsw, L):
    """
    Inductor Ripple Current in Buck Mode.

    Parameters
    ----------
    Vo : Output Voltage.

    D : Duty cycle of converter.

    fsw : Frequency.

    L : inductor value.

    Returns
    -------
    Ripple current for a given value of inductor.
    """
    return np.round(np.divide(np.multiply(float(Vo), 1-float(D)), np.multiply(float(fsw), float(L))), decimals=2)


def bck_cap_val(D, L, Vrp, fsw):
    """
    Capacitor Value in Buck Mode.

    Parameters
    ----------
    Vo : Output Voltage.

    D : Duty cycle of converter.

    L  : inductor value.

    Vrp : Ripple voltage.

    fsw : Frequency.

    Returns
    -------
    Value of output capacitor.
    """
    return np.format_float_scientific(np.divide(1 - float(D), np.multiply(8*float(L), pow(float(fsw), 2)*float(Vrp/100))), unique=False, precision=2, trim='-', exp_digits=1)

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
