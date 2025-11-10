"""
Micromechanics Module
Calculate lamina properties from fiber and matrix properties
"""

import numpy as np


class Micromechanics:
    """
    Micromechanics calculations for composite materials
    Using Rule of Mixtures and Halpin-Tsai equations
    """

    def __init__(self, E_f, nu_f, E_m, nu_m, V_f):
        """
        Initialize micromechanics calculator

        Parameters:
        -----------
        E_f : float
            Fiber Young's modulus (Pa or GPa)
        nu_f : float
            Fiber Poisson's ratio
        E_m : float
            Matrix Young's modulus (Pa or GPa)
        nu_m : float
            Matrix Poisson's ratio
        V_f : float
            Fiber volume fraction
        """
        self.E_f = E_f
        self.nu_f = nu_f
        self.E_m = E_m
        self.nu_m = nu_m
        self.V_f = V_f
        self.V_m = 1 - V_f  # Matrix volume fraction

    @staticmethod
    def calculate_fiber_volume_fraction(n_fibers, d, width, t):
        """
        Calculate fiber volume fraction from fiber count and dimensions

        Parameters:
        -----------
        n_fibers : int
            Number of fibers per unit width
        d : float
            Fiber diameter
        width : float
            Reference width
        t : float
            Lamina thickness

        Returns:
        --------
        V_f : float
            Fiber volume fraction
        """
        # Area of fibers per unit width
        A_fibers = n_fibers * np.pi * (d/2)**2 / width
        # Total area per unit width
        A_total = t
        # Volume fraction
        V_f = A_fibers / A_total
        return V_f

    def longitudinal_modulus(self):
        """
        Calculate longitudinal Young's modulus E1
        Rule of Mixtures

        Returns:
        --------
        E1 : float
            Longitudinal modulus
        """
        E1 = self.E_f * self.V_f + self.E_m * self.V_m
        return E1

    def transverse_modulus_halpin_tsai(self, xi=2):
        """
        Calculate transverse Young's modulus E2
        Halpin-Tsai equation

        Parameters:
        -----------
        xi : float
            Reinforcing factor (typically 2 for circular fibers)

        Returns:
        --------
        E2 : float
            Transverse modulus
        """
        eta = (self.E_f / self.E_m - 1) / (self.E_f / self.E_m + xi)
        E2 = self.E_m * (1 + xi * eta * self.V_f) / (1 - eta * self.V_f)
        return E2

    def transverse_modulus_inverse_rom(self):
        """
        Calculate transverse Young's modulus E2
        Inverse Rule of Mixtures (lower bound)

        Returns:
        --------
        E2 : float
            Transverse modulus
        """
        E2 = 1 / (self.V_f / self.E_f + self.V_m / self.E_m)
        return E2

    def major_poisson_ratio(self):
        """
        Calculate major Poisson's ratio nu12
        Rule of Mixtures

        Returns:
        --------
        nu12 : float
            Major Poisson's ratio
        """
        nu12 = self.nu_f * self.V_f + self.nu_m * self.V_m
        return nu12

    def shear_modulus_halpin_tsai(self, xi=1):
        """
        Calculate in-plane shear modulus G12
        Halpin-Tsai equation

        Parameters:
        -----------
        xi : float
            Reinforcing factor (typically 1 for shear)

        Returns:
        --------
        G12 : float
            In-plane shear modulus
        """
        G_f = self.E_f / (2 * (1 + self.nu_f))
        G_m = self.E_m / (2 * (1 + self.nu_m))

        eta = (G_f / G_m - 1) / (G_f / G_m + xi)
        G12 = G_m * (1 + xi * eta * self.V_f) / (1 - eta * self.V_f)
        return G12

    def get_engineering_constants(self, method='halpin-tsai'):
        """
        Get all engineering constants of the lamina

        Parameters:
        -----------
        method : str
            'halpin-tsai' or 'inverse-rom' for transverse properties

        Returns:
        --------
        dict : Dictionary with E1, E2, G12, nu12
        """
        E1 = self.longitudinal_modulus()

        if method == 'halpin-tsai':
            E2 = self.transverse_modulus_halpin_tsai()
            G12 = self.shear_modulus_halpin_tsai()
        else:
            E2 = self.transverse_modulus_inverse_rom()
            G_m = self.E_m / (2 * (1 + self.nu_m))
            G12 = G_m / (1 - self.V_f)  # Simple estimate

        nu12 = self.major_poisson_ratio()

        return {
            'E1': E1,
            'E2': E2,
            'G12': G12,
            'nu12': nu12,
            'V_f': self.V_f
        }

    def print_properties(self):
        """Print calculated properties"""
        props = self.get_engineering_constants()
        print("\n=== Lamina Engineering Constants ===")
        print(f"Fiber Volume Fraction: {props['V_f']:.4f}")
        print(f"E1  = {props['E1']:.3f} GPa")
        print(f"E2  = {props['E2']:.3f} GPa")
        print(f"G12 = {props['G12']:.3f} GPa")
        print(f"ν12 = {props['nu12']:.4f}")
        print("=" * 40)
