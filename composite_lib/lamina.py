"""
Lamina Module
Calculate lamina stiffness matrices and transformed properties
"""

import numpy as np


class Lamina:
    """
    Single lamina (ply) analysis
    Calculate Q matrix and transformed Q-bar matrix
    """

    def __init__(self, E1, E2, G12, nu12, t, theta=0):
        """
        Initialize lamina

        Parameters:
        -----------
        E1 : float
            Longitudinal Young's modulus (GPa)
        E2 : float
            Transverse Young's modulus (GPa)
        G12 : float
            In-plane shear modulus (GPa)
        nu12 : float
            Major Poisson's ratio
        t : float
            Lamina thickness (mm)
        theta : float
            Fiber orientation angle (degrees)
        """
        self.E1 = E1
        self.E2 = E2
        self.G12 = G12
        self.nu12 = nu12
        self.nu21 = nu12 * E2 / E1  # Minor Poisson's ratio
        self.t = t
        self.theta = theta

        # Calculate Q matrix
        self.Q = self._calculate_Q()

        # Calculate transformed Q-bar matrix
        self.Qbar = self._calculate_Qbar()

    def _calculate_Q(self):
        """
        Calculate the reduced stiffness matrix Q
        for plane stress condition

        Returns:
        --------
        Q : ndarray (3x3)
            Reduced stiffness matrix in material coordinates
        """
        nu21 = self.nu21
        denom = 1 - self.nu12 * nu21

        Q11 = self.E1 / denom
        Q22 = self.E2 / denom
        Q12 = self.nu12 * self.E2 / denom
        Q66 = self.G12

        Q = np.array([
            [Q11, Q12, 0],
            [Q12, Q22, 0],
            [0,   0,   Q66]
        ])

        return Q

    def _calculate_Qbar(self):
        """
        Calculate the transformed reduced stiffness matrix Q-bar
        for arbitrary fiber orientation

        Returns:
        --------
        Qbar : ndarray (3x3)
            Transformed reduced stiffness matrix
        """
        theta_rad = np.radians(self.theta)
        c = np.cos(theta_rad)
        s = np.sin(theta_rad)

        c2 = c**2
        s2 = s**2
        c3 = c**3
        s3 = s**3
        c4 = c**4
        s4 = s**4

        Q11, Q22, Q12, Q66 = self.Q[0,0], self.Q[1,1], self.Q[0,1], self.Q[2,2]

        # Transformation for Q-bar
        Qbar11 = Q11*c4 + 2*(Q12 + 2*Q66)*s2*c2 + Q22*s4
        Qbar22 = Q11*s4 + 2*(Q12 + 2*Q66)*s2*c2 + Q22*c4
        Qbar12 = (Q11 + Q22 - 4*Q66)*s2*c2 + Q12*(s4 + c4)
        Qbar66 = (Q11 + Q22 - 2*Q12 - 2*Q66)*s2*c2 + Q66*(s4 + c4)
        Qbar16 = (Q11 - Q12 - 2*Q66)*s*c3 + (Q12 - Q22 + 2*Q66)*s3*c
        Qbar26 = (Q11 - Q12 - 2*Q66)*s3*c + (Q12 - Q22 + 2*Q66)*s*c3

        Qbar = np.array([
            [Qbar11, Qbar12, Qbar16],
            [Qbar12, Qbar22, Qbar26],
            [Qbar16, Qbar26, Qbar66]
        ])

        return Qbar

    def get_compliance_matrix(self):
        """
        Calculate compliance matrix S in material coordinates

        Returns:
        --------
        S : ndarray (3x3)
            Compliance matrix
        """
        S = np.array([
            [1/self.E1,     -self.nu12/self.E1,  0],
            [-self.nu12/self.E1,  1/self.E2,      0],
            [0,             0,                    1/self.G12]
        ])
        return S

    def print_properties(self):
        """Print lamina properties"""
        print(f"\n=== Lamina Properties (θ = {self.theta}°) ===")
        print(f"E1  = {self.E1:.3f} GPa")
        print(f"E2  = {self.E2:.3f} GPa")
        print(f"G12 = {self.G12:.3f} GPa")
        print(f"ν12 = {self.nu12:.4f}")
        print(f"ν21 = {self.nu21:.4f}")
        print(f"t   = {self.t:.4f} mm")
        print("\nQ matrix (GPa):")
        print(self.Q)
        print("\nQ-bar matrix (GPa):")
        print(self.Qbar)
        print("=" * 40)
