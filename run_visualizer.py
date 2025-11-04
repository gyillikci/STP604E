#!/usr/bin/env python3
"""
Launch the Composite Materials 3D Visualizer
Interactive web-based visualization tool for CLPT analysis
"""

import subprocess
import sys
import os

def main():
    print("="*70)
    print("  COMPOSITE MATERIALS 3D VISUALIZER")
    print("  STP 604E - Classical Laminated Plate Theory")
    print("="*70)
    print()
    print("Starting visualization server...")
    print("The visualizer will open in your web browser.")
    print("Press Ctrl+C to stop the server.")
    print()

    # Get the path to the visualizer
    visualizer_path = os.path.join(
        os.path.dirname(__file__),
        'visualization',
        'composite_visualizer.py'
    )

    # Run streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            visualizer_path,
            '--theme.base', 'light',
            '--theme.primaryColor', '#1f77b4',
            '--server.headless', 'false'
        ])
    except KeyboardInterrupt:
        print("\n\nVisualizer stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure streamlit is installed:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
