"""
Laminate Module
Classical Laminated Plate Theory (CLPT) implementation
Calculate A, B, D matrices and perform laminate analysis
"""

import numpy as np
from .lamina import Lamina


class Laminate:
    """
    Laminate analysis using Classical Laminated Plate Theory (CLPT)
    """

    def __init__(self, material_props, stacking_sequence, ply_thickness):
        """
        Initialize laminate

        Parameters:
        -----------
        material_props : dict
            Dictionary with E1, E2, G12, nu12
        stacking_sequence : list
            List of ply angles (degrees), e.g., [0, 90, 0] or [-45, 45]
            Can use 's' suffix for symmetric, e.g., "0/90/0_s"
        ply_thickness : float or list
            Thickness of each ply (mm), or single value if all equal
        """
        self.material_props = material_props

        # Parse stacking sequence
        if isinstance(stacking_sequence, str):
            self.stacking_sequence = self._parse_stacking_sequence(stacking_sequence)
        else:
            self.stacking_sequence = stacking_sequence

        # Handle ply thickness
        if isinstance(ply_thickness, (int, float)):
            self.ply_thicknesses = [ply_thickness] * len(self.stacking_sequence)
        else:
            self.ply_thicknesses = ply_thickness

        self.n_plies = len(self.stacking_sequence)

        # Create lamina objects
        self.laminae = self._create_laminae()

        # Calculate laminate properties
        self.total_thickness = sum(self.ply_thicknesses)
        self.z_coords = self._calculate_z_coordinates()

        # Calculate ABD matrices
        self.A, self.B, self.D = self._calculate_ABD()

        # Calculate compliance matrices
        self.ABD = self._assemble_ABD()
        self.abd = np.linalg.inv(self.ABD)

    def _parse_stacking_sequence(self, seq_str):
        """
        Parse stacking sequence string
        Examples: "0/90/0_s", "[0/90]_s", "45/-45/0"
        """
        # Remove brackets and spaces
        seq_str = seq_str.replace('[', '').replace(']', '').replace(' ', '')

        # Check for symmetric notation
        if '_s' in seq_str.lower() or 's' == seq_str[-1].lower():
            seq_str = seq_str.replace('_s', '').replace('_S', '').replace('S', '').replace('s', '')
            angles = [float(x) for x in seq_str.split('/')]
            # Create symmetric layup
            angles = angles + angles[::-1]
        else:
            angles = [float(x) for x in seq_str.split('/')]

        return angles

    def _create_laminae(self):
        """Create Lamina objects for each ply"""
        laminae = []
        for i, theta in enumerate(self.stacking_sequence):
            lamina = Lamina(
                E1=self.material_props['E1'],
                E2=self.material_props['E2'],
                G12=self.material_props['G12'],
                nu12=self.material_props['nu12'],
                t=self.ply_thicknesses[i],
                theta=theta
            )
            laminae.append(lamina)
        return laminae

    def _calculate_z_coordinates(self):
        """
        Calculate z-coordinates of ply interfaces
        Reference at mid-plane (z=0)

        Returns:
        --------
        z : ndarray
            z-coordinates [z0, z1, ..., zn]
        """
        z = np.zeros(self.n_plies + 1)
        z[0] = -self.total_thickness / 2

        for i in range(self.n_plies):
            z[i+1] = z[i] + self.ply_thicknesses[i]

        return z

    def _calculate_ABD(self):
        """
        Calculate A, B, D stiffness matrices

        Returns:
        --------
        A : ndarray (3x3)
            Extensional stiffness matrix
        B : ndarray (3x3)
            Coupling stiffness matrix
        D : ndarray (3x3)
            Bending stiffness matrix
        """
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        D = np.zeros((3, 3))

        for i, lamina in enumerate(self.laminae):
            z_k = self.z_coords[i]
            z_k1 = self.z_coords[i+1]

            Qbar = lamina.Qbar

            # A matrix
            A += Qbar * (z_k1 - z_k)

            # B matrix
            B += 0.5 * Qbar * (z_k1**2 - z_k**2)

            # D matrix
            D += (1/3) * Qbar * (z_k1**3 - z_k**3)

        return A, B, D

    def _assemble_ABD(self):
        """
        Assemble 6x6 ABD matrix

        Returns:
        --------
        ABD : ndarray (6x6)
            Combined stiffness matrix
        """
        ABD = np.block([
            [self.A, self.B],
            [self.B, self.D]
        ])
        return ABD

    def calculate_strains_curvatures(self, loads):
        """
        Calculate mid-plane strains and curvatures from applied loads

        Parameters:
        -----------
        loads : dict or ndarray
            Applied loads: {'Nx', 'Ny', 'Nxy', 'Mx', 'My', 'Mxy'}
            or array [Nx, Ny, Nxy, Mx, My, Mxy]

        Returns:
        --------
        strains : ndarray (3,)
            Mid-plane strains [εx0, εy0, γxy0]
        curvatures : ndarray (3,)
            Curvatures [κx, κy, κxy]
        """
        if isinstance(loads, dict):
            N = np.array([loads.get('Nx', 0), loads.get('Ny', 0), loads.get('Nxy', 0)])
            M = np.array([loads.get('Mx', 0), loads.get('My', 0), loads.get('Mxy', 0)])
            load_vector = np.concatenate([N, M])
        else:
            load_vector = np.array(loads)

        # Solve for strains and curvatures
        strain_curvature = self.abd @ load_vector

        strains = strain_curvature[0:3]
        curvatures = strain_curvature[3:6]

        return strains, curvatures

    def calculate_ply_stresses(self, strains, curvatures, ply_index, surface='mid'):
        """
        Calculate stresses in a specific ply

        Parameters:
        -----------
        strains : ndarray (3,)
            Mid-plane strains
        curvatures : ndarray (3,)
            Curvatures
        ply_index : int
            Index of ply (0-based)
        surface : str
            'top', 'mid', or 'bottom' of the ply

        Returns:
        --------
        stress_global : ndarray (3,)
            Stresses in global coordinates [σx, σy, τxy]
        stress_local : ndarray (3,)
            Stresses in material coordinates [σ1, σ2, τ12]
        """
        # Get z-coordinate
        z_k = self.z_coords[ply_index]
        z_k1 = self.z_coords[ply_index + 1]

        if surface == 'top':
            z = z_k1
        elif surface == 'bottom':
            z = z_k
        else:  # mid
            z = (z_k + z_k1) / 2

        # Calculate strains at z
        strain_z = strains + z * curvatures

        # Get Qbar for this ply
        Qbar = self.laminae[ply_index].Qbar

        # Calculate stress in global coordinates
        stress_global = Qbar @ strain_z

        # Transform to material coordinates
        theta = self.laminae[ply_index].theta
        stress_local = self._transform_stress_to_material(stress_global, theta)

        return stress_global, stress_local

    def _transform_stress_to_material(self, stress_global, theta):
        """
        Transform stress from global to material coordinates

        Parameters:
        -----------
        stress_global : ndarray (3,)
            Stress in global coordinates [σx, σy, τxy]
        theta : float
            Ply angle (degrees)

        Returns:
        --------
        stress_local : ndarray (3,)
            Stress in material coordinates [σ1, σ2, τ12]
        """
        theta_rad = np.radians(theta)
        c = np.cos(theta_rad)
        s = np.sin(theta_rad)

        T = np.array([
            [c**2,    s**2,    2*s*c],
            [s**2,    c**2,   -2*s*c],
            [-s*c,    s*c,     c**2 - s**2]
        ])

        stress_local = T @ stress_global

        return stress_local

    def is_symmetric(self):
        """Check if laminate is symmetric"""
        n = len(self.stacking_sequence)
        for i in range(n // 2):
            if self.stacking_sequence[i] != self.stacking_sequence[-(i+1)]:
                return False
        return True

    def is_balanced(self):
        """Check if laminate is balanced"""
        angles = np.array(self.stacking_sequence)
        for angle in np.unique(angles):
            if angle != 0 and angle != 90:
                count_pos = np.sum(angles == angle)
                count_neg = np.sum(angles == -angle)
                if count_pos != count_neg:
                    return False
        return True

    def print_properties(self):
        """Print laminate properties"""
        print("\n" + "="*60)
        print(f"LAMINATE ANALYSIS: {self.stacking_sequence}")
        print("="*60)
        print(f"\nMaterial Properties:")
        print(f"  E1  = {self.material_props['E1']:.3f} GPa")
        print(f"  E2  = {self.material_props['E2']:.3f} GPa")
        print(f"  G12 = {self.material_props['G12']:.3f} GPa")
        print(f"  ν12 = {self.material_props['nu12']:.4f}")

        print(f"\nStacking Sequence: {self.stacking_sequence}")
        print(f"Number of Plies: {self.n_plies}")
        print(f"Total Thickness: {self.total_thickness:.4f} mm")
        print(f"Symmetric: {self.is_symmetric()}")
        print(f"Balanced: {self.is_balanced()}")

        print(f"\nZ-coordinates (mm): {self.z_coords}")

        print("\n--- A Matrix (Extensional Stiffness) [N/mm] ---")
        print(self.A)

        print("\n--- B Matrix (Coupling Stiffness) [N] ---")
        print(self.B)

        print("\n--- D Matrix (Bending Stiffness) [N·mm] ---")
        print(self.D)

        print("\n" + "="*60)
