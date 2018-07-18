import scipy
from scipy import constants
import numpy as np
import math

"""Sample Implementations of Equations from Nehori (1994)"""

def function_22(fft, freq):
    """Equations 2.2 include a relationship between 'E' and 'H', the 'vector-phasor' representations of E and B fields.
    This function attempts to leverage that relationship to return a B field computed from the provided FFT of an E field.
    Pass in the unmodified array FFT output, as well as the linear frequency of the data as an integer"""

    direction = [x, y, z] #PLACEHOLDER NEEDS TO BE CORRECT AND PASSED IN direction vector from sensor to source of measurement
    fft_plus = np.split(fft, 2)[0] #get the positive frequency component
    w = 2 * np.pi * freq #angular frequency from linear frequency of e field
    e = 2 * fft_plus * math.exp(-w * 1j) #is this the correct way to do multiplicaton of an imaginary number?
    n = (constants.mu_0 / constants.epsilon_0) ** 0.5 #intrinsic impedance (mu and epsilon of material should be passed in)

    h_calc = (np.cross(direction, e) / -n) #euqation solved for H
    b_calc = np.real(h_calc * math.exp(w * 1j)) #B pulled from H
    #b_ifft = np.fft.ifft(b_calc) #do an ifft on the resulting field if need be
    return b_calc #return fft-like array of b-field
