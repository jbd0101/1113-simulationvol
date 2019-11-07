#
#    Calculation of propeller thrust and torque
#
#    Based on Matlab program by H. Capart, 2019/09/08
#    Ch. Pecheur, 2019/10/30

import numpy as np

def thrustTorque(OmegaProp,Wvehicle,Nblades,bladeGeom,rhoAir=1.225):
    """
    Returns propeller thrust and torque given axial and angular speeds and propeller geometry.

    Args:
        OmegaProp: angular velocity [rad/s]
        Wvehicle: vehicle speed [m/s]
        Nblades: number of blades
        bladeGeom: geometry of a blade, as a 2-D array

            numpy.array([[r_1, beta_1, l_1], ..., [r_n, beta_n, l_n]])

            where:
                r_k: radius of the blade section [m], in ascending order (hub to tip),
                beta_k: angle of the blade at section [rad]
                l_k: width (cord length) of the blade at section [m]

        rhoAir: air density [kg/m^3], default = 1.225

    Returns: (T, Q) where:
        T: thrust [N]
        Q: torque [N*m]

    For example, for a propeller of radius 10 cm with a hub of radius 1 cm,
    with 3 trapezoidal blades, 1.5 cm wide at the hub and 3 cm wide at the tip,
    at angle 30°, starting at null speed and rotating at 50 rounds per second,
    the trust and torque are computed as:

    >>> bladeGeom = numpy.array([[0.010, numpy.pi/6, 0.015], [0.100, numpy.pi/6, 0.030]])
     bladeGeom = numpy.array([[0.010, numpy.pi/6, 0.015], [0.100, numpy.pi/6, 0.030]])
    >>> T, Q = thrustTorque(50*2*numpy.pi, 0, 3, bladeGeom)
    """
    Vinduced = 0 # start from zero induced velocity
    Vair = Wvehicle + Vinduced
    Rhub = bladeGeom[0,0] # [m] hub radius
    Rtip = bladeGeom[-1,0] # [m] blade tip radius
    Aprop = np.pi*(Rtip**2-Rhub**2) # [m^2] propeller disk area
    for iter in range(10): # 10 iterations seem sufficient
        # calculate thrust and torque:
        Tprop,Qprop = thrustTorqueFunctions(OmegaProp,Vair,rhoAir,Nblades,bladeGeom)
        # recalculate induced velocity:
        Vhover = np.sqrt( np.abs(Tprop)/(2*rhoAir*Aprop) )
        if Vhover < 1e-6:
            Vinduced = 0
        else:
            Vinduced = np.sign(Tprop)*Vhover*inducedVelocityFunction( Wvehicle/Vhover*np.sign(Tprop) )
        # keep record of previous value:
        VairPrev = Vair
        # update air velocity:
        Vair = Wvehicle + Vinduced

    if VairPrev*Vair < 0: # failure to converge
        Vair = 0
        _,Qprop = thrustTorqueFunctions(OmegaProp,Vair,rhoAir,Nblades,bladeGeom)
        Tprop = 0
    return Tprop, Qprop

def thrustTorqueFunctions(OmegaProp,Vair,rhoAir,Nblades,bladeGeom):
    """
     Calculation of propeller thrust and torque from angular
     velocity OmegaProp, air flow velocity Vair, air density rhoAir,
     number of blades Nblades, and blade geometry lookup table bladeGeom.
     H. Capart, 2019/09/08
    """
    # retrieve blade geometry:
    rLookup = bladeGeom[:,0]
    betaLookup = bladeGeom[:,1]
    LchordLookup = bladeGeom[:,2]
    Rhub = rLookup[0] # hub radius
    Rtip = rLookup[-1] # blade tip radius

    # discretize blade span:
    dr = (Rtip-Rhub)/50 # step
    r = np.arange(Rhub,Rtip,dr) # discrete position
    beta = np.interp(r,rLookup,betaLookup) # interpolate
    Lchord = np.interp(r,rLookup,LchordLookup) # interpolate

    # calculate coefficients along blade:
    gamma = np.arctan2( Vair , OmegaProp*r )
    alpha = beta - gamma
    cL,cD = liftDragCoefficients(alpha)
    cT = cL*np.cos(gamma) - cD*np.sin(gamma)
    cQ = cD*np.cos(gamma) + cL*np.sin(gamma)
    fT = (0.5*rhoAir*Nblades)*Lchord*cT*( Vair**2 + OmegaProp**2*r**2 )
    fQ = (0.5*rhoAir*Nblades)*Lchord*cQ*( Vair**2 + OmegaProp**2*r**2 )*r

    # integrate along blade using Simpson's rule:
    Tprop = sum( 0.5*( fT[0:-2] + fT[1:-1] ) )*dr
    Qprop = sum( 0.5*( fQ[0:-2] + fQ[1:-1] ) )*dr

    return Tprop,Qprop

def liftDragCoefficients(alpha):
    """
    Ideal lift and drag coefficients for flat plate
    at angle of attack alpha
    """
    alpha2 = -np.pi/2 + np.mod(alpha-np.pi/2,np.pi) # send to interval between -pi/2 and pi/2
    isSmallAngle = ( abs(alpha2) < np.pi/10 ) # limit of small angle of attack range
    cL = isSmallAngle * (2*np.pi*alpha2) + ~isSmallAngle * np.sin(2*alpha2) # lift coefficient
    cD = 2*np.sin(alpha)**2 # drag coefficient
    return cL,cD

def inducedVelocityFunction(x):
    """
    x = climb velocity ratio Wvehicle/Vhover
    y = induced velocity ratio Vinduced/Vhover
    """
    isWindmilling = (x<=-2)
    y = np.sqrt( 0.25*x**2 + 1 ) - 0.5*x if not isWindmilling \
        else - np.sqrt( 0.25*x**2 - 1 ) - 0.5*x
    return y
