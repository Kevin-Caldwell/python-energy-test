import math
import random

######### Universal Constants ##################################################

G = 9.8                 # Acceleration Due to Gravity (m/s)
RHO = 1.293             # Air Density (kg/m3)
C_AIR = 0.5             # Air Drag

MAX_ITERATIONS = 4     # Newtons Method Precision
DER_INT = 0.01          # Newtons Method Derivative Interval

######### Flight Parameters ####################################################
M_CARRY = 0             # Carry Mass (kg)
GAMMA = 0               # Flight Angle
V_MAX = 0               # Maximum Flight Velocity
V = 0                   # 3D Flight Velocity Vector (m/s)

M_TARE = 12             # Tare Mass of Drone (kg)
M = M_CARRY + M_TARE    # Total Mass of Drone (kg)
######### Drone Parameters #####################################################
A = 0.15                # Frontal Surface Area
K = 1.15                # Lifting Power Markup
C_BD = 0.075            # Blade Drag Coefficient
N_ROTOR = 8             # Number of Rotors
N_BLADES = 3            # Number of Blades
R_BLADE = 0.4           # Radius of Blade
INT_POWER = 100         # Power Internal Auxiliaries
C_BAR = 0.1             # SEE PAPER
CL_BAR = 0.4            # SEE PAPER

######### Calculated Drone Values ##############################################
ALPHA = 0               # Angle of Attack
R = 0                   # Rotor Disc Area (Calculated once)
V_T = 0                 # Blade Tip Speed
SIGMA = 0               # Rotor Solidity Ratio

T = 0                   # Thrust (Varies w/ time)
W = 0                   # Downwash Coefficient (Varies w/ time)
D_BODY = 0              # Drag Coefficity of UAV Body


######### Variable Update and Energy Function Calculations #####################

def sim_init():
    global D_BODY, R, V_T
    D_BODY = calc_d_body()
    R = calc_rotor_disc_area()


def update_sim():
    global D_BODY, T, W, V_T, M
    
    V_T = calc_blade_speed()
    D_BODY = calc_d_body()
    T = calc_thrust(power_climb())
    W = calc_downwash()
    M = M_TARE + M_CARRY


def calc_d_body():
    return 0.5 * RHO * V**2 * A * C_AIR

def calc_thrust(p_climb):
    return math.sqrt(M**2*G**2 + D_BODY**2 + 2*D_BODY*p_climb)

def calc_rotor_disc_area():
    return R_BLADE**2*math.pi*N_ROTOR

def calc_blade_speed():
    return math.sqrt((6*M*G) /
                     (N_ROTOR * N_BLADES * C_BAR * CL_BAR * RHO * R_BLADE))

def calc_solidarity_ratio():
    return N_BLADES * C_BAR / (math.pi * R_BLADE)

def calc_angle_of_attack():
    return math.atan2((-D_BODY - M*G*math.sin(GAMMA)), (M*G*math.cos(GAMMA)))

def calc_downwash(w0 = 1.0):

    # Initialize Function Constants
    c0 = T / (2 * RHO * R)
    c1 = V * math.sin(ALPHA)
    c2 = (V * math.cos(ALPHA))**2
    w0 = random.random()
    
    # Run Newtons Method
    for _ in range(MAX_ITERATIONS):
        w1 = w0 + DER_INT
        
        f_w0 = c0 - w0*math.sqrt((w0 - c1)**2 + c2)
        f_w1 = c0 - w1*math.sqrt((w1 - c1)**2 + c2)

        w0 -= f_w0 / (f_w1 - f_w0) * DER_INT

    # POTENTIAL TODO: ABS(w0), as negative roots are not permissible
    # The LHS of equation is always positive, sqrt's range is positive reals
    # This means w must always be positive. 
    
    return w0

        

def power_total():
    return power_air() + \
        K * power_lift() + \
        power_profile() + \
        power_climb() + \
        power_int()

def power_air():
    return 0.5 * RHO * V**3 * A * C_AIR

def power_lift():
    return W * T

def power_profile():
    return RHO * R * V_T**3 * (1 + 2 * (V / V_T)**2) * SIGMA * C_BD / 8

def power_climb():
    return M * G * V * math.sin(GAMMA)

def power_int():
    return INT_POWER