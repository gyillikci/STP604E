"""
Composite Materials Analysis Library
Classical Laminated Plate Theory (CLPT) Implementation
"""

from .micromechanics import Micromechanics
from .lamina import Lamina
from .laminate import Laminate

__version__ = "1.0.0"
__all__ = ['Micromechanics', 'Lamina', 'Laminate']
