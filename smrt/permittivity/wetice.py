# coding: utf-8

import numpy as np
from ..core.layer import layer_properties
from .ice import ice_permittivity_maetzler06
from .water import water_permittivity


@layer_properties("temperature", "liquid_water")
def wetice_permittivity_bohren83(frequency, temperature, liquid_water):
    """ calculate the dielectric constant of wet particules of ice using Bohren and Huffman 1983 according to Ya Qi Jin, eq 8-69, 1996 p282

    :param frequency: frequency in Hz
    :param temperature: temperature in K
    :param liquid_water (fractional volume of water with respect to ice+water volume).
    :returns: Complex permittivity of pure ice

    """
    # from http://books.google.com/books?id=Y_-113zIvgkC&pg=PA142&lpg=PA142&dq=effective+dielectric+constant+sphere+coated+small&source=bl&ots=ZVfwvkA0K1&sig=P7fHb0Jff8C-7-GrlEnWRZkkxY8&hl=en&ei=RHfDTrmjJYXj8AO3v7ScCw&sa=X&oi=book_result&ct=result&resnum=3&ved=0CDYQ6AEwAg#v=onepage&q=effective%20dielectric%20constant%20sphere%20coated%20small&f=false
    # see also: K L CHOPRA and G B REDDY, Praman.a- Optically selective coatings, J. Phys., Vol. 27, Nos 1 & 2, July & August 1986, pp. 193-217.

    epsice = ice_permittivity_maetzler06(frequency, temperature)

    if np.all(liquid_water <= 0.0):
        return epsice

    epswater = water_permittivity(frequency, temperature)

    S = 1 - liquid_water

    Cplus = epsice + 2 * epswater
    Cminus = (epsice - epswater) * S

    Ewi = (Cplus + 2 * Cminus) / (Cplus - Cminus) * epswater

    return Ewi