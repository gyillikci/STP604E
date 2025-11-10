import numpy as np
d = 10e-6 # meters
n = 1900 
t = 0.25e-3 # meters
A_fibers = n * np.pi * (d/2)**2
V_ply = 1e-3 * t # m^2 * m = m^3 (for 1 mm width)
V_f = A_fibers / (1e-3) # fiber area per 1 mm width (projected)
V_f_fraction = V_f * t / V_ply
print(f"Fiber Volume V_f: {V_f_fraction:.4f} ({V_f_fraction*100:.2f}%)")

E_f, v_f = 220e9, 0.25
E_m, v_m = 3.6e9, 0.40
V_m = 1 - V_f_fraction
E1 = V_f_fraction * E_f + V_m * E_m
E2 = 1 / (V_f_fraction / E_f + V_m / E_m)
v12 = V_f_fraction * v_f + V_m * v_m
G_f, G_m = E_f/(2*(1+v_f)), E_m/(2*(1+v_m))
G12 = 1 / (V_f_fraction / G_f + V_m / G_m)
