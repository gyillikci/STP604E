"""
Interactive 3D Composite Materials Visualizer
Real-time visualization of laminate properties and parameter effects
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from composite_lib import Laminate, Lamina


def main():
    st.set_page_config(
        page_title="Composite Materials Visualizer",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🔬 Composite Materials 3D Visualizer")
    st.markdown("**STP 604E - Classical Laminated Plate Theory (CLPT)**")
    st.markdown("---")

    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Configuration")

        viz_mode = st.selectbox(
            "Visualization Mode",
            ["Laminate Structure", "Stiffness Analysis", "Quasi-Isotropic Study",
             "Parametric Analysis", "Stress/Strain Distribution"]
        )

        st.markdown("---")
        st.header("📊 Material Properties")

        # Material selection
        material_preset = st.selectbox(
            "Material Preset",
            ["Custom", "AS4/3501-6 Carbon/Epoxy", "AS/3501 Graphite/Epoxy",
             "Kevlar/Epoxy", "E-Glass/Epoxy"]
        )

        # Get material properties
        material = get_material_properties(material_preset)

        # Allow custom editing
        if material_preset == "Custom":
            E1 = st.number_input("E₁ (GPa)", value=150.0, min_value=1.0, max_value=500.0)
            E2 = st.number_input("E₂ (GPa)", value=10.0, min_value=1.0, max_value=100.0)
            G12 = st.number_input("G₁₂ (GPa)", value=7.0, min_value=1.0, max_value=50.0)
            nu12 = st.number_input("ν₁₂", value=0.28, min_value=0.1, max_value=0.5)
            material = {'E1': E1, 'E2': E2, 'G12': G12, 'nu12': nu12}
        else:
            st.info(f"E₁ = {material['E1']} GPa")
            st.info(f"E₂ = {material['E2']} GPa")
            st.info(f"G₁₂ = {material['G12']} GPa")
            st.info(f"ν₁₂ = {material['nu12']}")

        st.markdown("---")
        st.header("📐 Laminate Configuration")

        # Stacking sequence input
        stacking_input = st.text_input(
            "Stacking Sequence",
            value="0/45/-45/90",
            help="Enter angles separated by /, use _s for symmetric"
        )

        ply_thickness = st.number_input(
            "Ply Thickness (mm)",
            value=0.125,
            min_value=0.01,
            max_value=2.0,
            step=0.01
        )

    # Main content area
    if viz_mode == "Laminate Structure":
        visualize_laminate_structure(material, stacking_input, ply_thickness)

    elif viz_mode == "Stiffness Analysis":
        visualize_stiffness_analysis(material, stacking_input, ply_thickness)

    elif viz_mode == "Quasi-Isotropic Study":
        visualize_quasi_isotropic(material, ply_thickness)

    elif viz_mode == "Parametric Analysis":
        visualize_parametric_analysis(material, stacking_input, ply_thickness)

    elif viz_mode == "Stress/Strain Distribution":
        visualize_stress_strain(material, stacking_input, ply_thickness)


def get_material_properties(preset):
    """Get material properties from preset"""
    materials = {
        "AS4/3501-6 Carbon/Epoxy": {
            'E1': 142.0, 'E2': 10.3, 'G12': 7.2, 'nu12': 0.27
        },
        "AS/3501 Graphite/Epoxy": {
            'E1': 181.0, 'E2': 10.3, 'G12': 7.17, 'nu12': 0.28
        },
        "Kevlar/Epoxy": {
            'E1': 76.0, 'E2': 5.5, 'G12': 2.3, 'nu12': 0.34
        },
        "E-Glass/Epoxy": {
            'E1': 38.6, 'E2': 8.27, 'G12': 4.14, 'nu12': 0.26
        },
        "Custom": {
            'E1': 150.0, 'E2': 10.0, 'G12': 7.0, 'nu12': 0.28
        }
    }
    return materials.get(preset, materials["Custom"])


def visualize_laminate_structure(material, stacking_input, ply_thickness):
    """Visualize 3D laminate structure"""
    st.header("🏗️ Laminate Structure Visualization")

    try:
        lam = Laminate(material, stacking_input, ply_thickness)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Laminate Information")
            st.write(f"**Stacking Sequence:** {lam.stacking_sequence}")
            st.write(f"**Number of Plies:** {lam.n_plies}")
            st.write(f"**Total Thickness:** {lam.total_thickness:.4f} mm")
            st.write(f"**Symmetric:** {'✓ Yes' if lam.is_symmetric() else '✗ No'}")
            st.write(f"**Balanced:** {'✓ Yes' if lam.is_balanced() else '✗ No'}")

            # Z-coordinates table
            st.subheader("Z-Coordinates")
            z_data = []
            for i, (z, theta) in enumerate(zip(lam.z_coords[:-1], lam.stacking_sequence)):
                z_data.append({
                    'Ply': i+1,
                    'Angle (°)': theta,
                    'z_bottom (mm)': f"{lam.z_coords[i]:.4f}",
                    'z_top (mm)': f"{lam.z_coords[i+1]:.4f}"
                })
            st.dataframe(z_data)

        with col2:
            # 3D visualization of laminate
            fig = create_3d_laminate_plot(lam)
            st.plotly_chart(fig, use_container_width=True)

        # Stiffness matrices
        st.subheader("Stiffness Matrices")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**[A] Matrix (N/mm)**")
            st.dataframe(lam.A, use_container_width=True)

        with col2:
            st.write("**[B] Matrix (N)**")
            st.dataframe(lam.B, use_container_width=True)

        with col3:
            st.write("**[D] Matrix (N·mm)**")
            st.dataframe(lam.D, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


def create_3d_laminate_plot(lam):
    """Create 3D visualization of laminate layers"""
    fig = go.Figure()

    # Color map for angles
    colors = px.colors.qualitative.Set3

    # Create each ply as a 3D surface
    width = 50  # mm
    length = 50  # mm

    for i, theta in enumerate(lam.stacking_sequence):
        z_bottom = lam.z_coords[i]
        z_top = lam.z_coords[i+1]

        # Create ply surfaces
        x = np.array([[0, length], [0, length]])
        y = np.array([[0, 0], [width, width]])
        z = np.array([[z_bottom, z_bottom], [z_bottom, z_bottom]])

        # Color based on angle
        color_idx = int((theta + 90) / 30) % len(colors)

        # Bottom surface
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, colors[color_idx]], [1, colors[color_idx]]],
            showscale=False,
            name=f"Ply {i+1} ({theta}°)",
            hovertemplate=f"Ply {i+1}<br>Angle: {theta}°<br>z: %{{z:.4f}} mm<extra></extra>"
        ))

        # Top surface
        z = np.array([[z_top, z_top], [z_top, z_top]])
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, colors[color_idx]], [1, colors[color_idx]]],
            showscale=False,
            showlegend=False,
            hovertemplate=f"Ply {i+1}<br>Angle: {theta}°<br>z: %{{z:.4f}} mm<extra></extra>"
        ))

        # Draw fiber direction arrows
        mid_z = (z_bottom + z_top) / 2
        arrow_length = 15
        cx, cy = length/2, width/2
        dx = arrow_length * np.cos(np.radians(theta))
        dy = arrow_length * np.sin(np.radians(theta))

        # Draw line for fiber direction
        fig.add_trace(go.Scatter3d(
            x=[cx - dx/2, cx + dx/2],
            y=[cy - dy/2, cy + dy/2],
            z=[mid_z, mid_z],
            mode='lines+markers',
            line=dict(color='black', width=4),
            marker=dict(size=[6, 10], color=['black', 'red'], symbol='diamond'),
            name=f"Fiber direction {theta}°",
            showlegend=False,
            hovertemplate=f"Fiber direction: {theta}°<extra></extra>"
        ))

    fig.update_layout(
        title="Laminate 3D Structure (Fiber Orientations)",
        scene=dict(
            xaxis_title='Length (mm)',
            yaxis_title='Width (mm)',
            zaxis_title='Thickness (mm)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=600
    )

    return fig


def visualize_stiffness_analysis(material, stacking_input, ply_thickness):
    """Visualize stiffness matrix components"""
    st.header("📊 Stiffness Matrix Analysis")

    try:
        lam = Laminate(material, stacking_input, ply_thickness)

        # Create heatmaps
        col1, col2, col3 = st.columns(3)

        with col1:
            fig = create_matrix_heatmap(lam.A, "[A] Extensional Stiffness", "N/mm")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = create_matrix_heatmap(lam.B, "[B] Coupling Stiffness", "N")
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            fig = create_matrix_heatmap(lam.D, "[D] Bending Stiffness", "N·mm")
            st.plotly_chart(fig, use_container_width=True)

        # Rotation study
        st.markdown("---")
        st.subheader("🔄 Rotation Study: Effect of Laminate Rotation")
        st.write("Rotate the entire laminate and observe how the stiffness matrices change")

        rotation_angle = st.slider("Global Rotation Angle (°)", -90, 90, 0, 5)

        rotated_sequence = [(angle + rotation_angle) for angle in lam.stacking_sequence]
        lam_rotated = Laminate(material, rotated_sequence, ply_thickness)

        # Display sequences
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Original:** {lam.stacking_sequence}")
        with col2:
            st.success(f"**Rotated by {rotation_angle}°:** {rotated_sequence}")

        # Show A matrix comparison with heatmaps
        st.write("### [A] Matrix Comparison")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Original [A] Matrix**")
            fig = create_matrix_heatmap(lam.A, "Original [A]", "N/mm")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write(f"**Rotated [A] Matrix ({rotation_angle}°)**")
            fig = create_matrix_heatmap(lam_rotated.A, f"Rotated [A] (θ={rotation_angle}°)", "N/mm")
            st.plotly_chart(fig, use_container_width=True)

        # Show numerical comparison
        with st.expander("📊 Detailed Numerical Comparison"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Original [A]**")
                st.dataframe(lam.A, use_container_width=True)

            with col2:
                st.write("**Rotated [A]**")
                st.dataframe(lam_rotated.A, use_container_width=True)

            with col3:
                st.write("**Absolute Difference**")
                diff = np.abs(lam_rotated.A - lam.A)
                st.dataframe(diff, use_container_width=True)

                # Calculate and show max change
                max_change = np.max(diff)
                avg_change = np.mean(diff[diff > 1e-10])  # Ignore near-zero values
                st.metric("Max Change", f"{max_change:.3f} N/mm")
                if avg_change > 0:
                    st.metric("Avg Change", f"{avg_change:.3f} N/mm")

        # B and D matrix comparisons
        st.write("### [B] and [D] Matrix Comparison")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**[B] Coupling Matrix**")
            fig = create_matrix_heatmap(lam_rotated.B, f"[B] at θ={rotation_angle}°", "N")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("**[D] Bending Matrix**")
            fig = create_matrix_heatmap(lam_rotated.D, f"[D] at θ={rotation_angle}°", "N·mm")
            st.plotly_chart(fig, use_container_width=True)

        # Add continuous rotation plot
        st.markdown("---")
        st.write("### 📈 Stiffness vs. Rotation Angle")

        with st.expander("Show continuous rotation analysis", expanded=False):
            st.write("This plot shows how stiffness matrix elements vary with rotation angle")

            # Calculate for a range of angles
            angles = np.linspace(-90, 90, 37)  # Every 5 degrees
            A11_vals, A22_vals, A12_vals, A66_vals = [], [], [], []
            A16_vals, A26_vals = [], []

            for angle in angles:
                temp_seq = [(a + angle) for a in lam.stacking_sequence]
                temp_lam = Laminate(material, temp_seq, ply_thickness)
                A11_vals.append(temp_lam.A[0, 0])
                A22_vals.append(temp_lam.A[1, 1])
                A12_vals.append(temp_lam.A[0, 1])
                A66_vals.append(temp_lam.A[2, 2])
                A16_vals.append(temp_lam.A[0, 2])
                A26_vals.append(temp_lam.A[1, 2])

            # Create plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=angles, y=A11_vals, name='A₁₁',
                                    mode='lines', line=dict(width=2)))
            fig.add_trace(go.Scatter(x=angles, y=A22_vals, name='A₂₂',
                                    mode='lines', line=dict(width=2, dash='dash')))
            fig.add_trace(go.Scatter(x=angles, y=A12_vals, name='A₁₂',
                                    mode='lines', line=dict(width=2)))
            fig.add_trace(go.Scatter(x=angles, y=A66_vals, name='A₆₆',
                                    mode='lines', line=dict(width=2)))

            # Add vertical line at current rotation
            fig.add_vline(x=rotation_angle, line_dash="dot", line_color="red",
                         annotation_text=f"Current: {rotation_angle}°",
                         annotation_position="top")

            fig.update_layout(
                title="[A] Matrix Elements vs. Global Rotation",
                xaxis_title="Rotation Angle (°)",
                yaxis_title="Stiffness (N/mm)",
                height=400,
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Coupling terms
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=angles, y=A16_vals, name='A₁₆',
                                     mode='lines', line=dict(width=2)))
            fig2.add_trace(go.Scatter(x=angles, y=A26_vals, name='A₂₆',
                                     mode='lines', line=dict(width=2)))

            fig2.add_vline(x=rotation_angle, line_dash="dot", line_color="red",
                          annotation_text=f"Current: {rotation_angle}°")
            fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

            fig2.update_layout(
                title="Shear Coupling Terms vs. Global Rotation",
                xaxis_title="Rotation Angle (°)",
                yaxis_title="Stiffness (N/mm)",
                height=400,
                hovermode='x unified'
            )

            st.plotly_chart(fig2, use_container_width=True)

            # Check for quasi-isotropy
            A11_range = max(A11_vals) - min(A11_vals)
            A16_max = max(np.abs(A16_vals))
            if A11_range < 0.01 * np.mean(A11_vals) and A16_max < 0.01:
                st.success("✓ This laminate appears to be QUASI-ISOTROPIC! The stiffness remains nearly constant with rotation.")
            else:
                st.info(f"ℹ️ This laminate is NOT quasi-isotropic. A₁₁ varies by {A11_range:.2f} N/mm ({A11_range/np.mean(A11_vals)*100:.1f}%)")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def create_matrix_heatmap(matrix, title, units):
    """Create heatmap visualization of matrix"""
    labels = ['11', '22', '12', '16', '26', '66']

    # Use only 3x3 for display
    display_matrix = np.zeros((3, 3))
    display_matrix[0, 0] = matrix[0, 0]
    display_matrix[1, 1] = matrix[1, 1]
    display_matrix[0, 1] = display_matrix[1, 0] = matrix[0, 1]
    display_matrix[2, 2] = matrix[2, 2]
    display_matrix[0, 2] = display_matrix[2, 0] = matrix[0, 2]
    display_matrix[1, 2] = display_matrix[2, 1] = matrix[1, 2]

    fig = go.Figure(data=go.Heatmap(
        z=display_matrix,
        x=['1', '2', '6'],
        y=['1', '2', '6'],
        colorscale='Viridis',
        text=display_matrix,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        hovertemplate='%{y}%{x}: %{z:.3f} ' + units + '<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='j',
        yaxis_title='i',
        height=400
    )

    return fig


def visualize_quasi_isotropic(material, ply_thickness):
    """Visualize quasi-isotropic laminate behavior"""
    st.header("🔄 Quasi-Isotropic Laminate Study")

    st.write("""
    A quasi-isotropic laminate has extensional stiffness that remains unchanged
    when the entire laminate is rotated. This requires specific ply orientations.
    """)

    # Test different laminates
    test_laminates = {
        "[-45/0/45/90]": [-45, 0, 45, 90],
        "[0/30/60/90]": [0, 30, 60, 90],
        "[0/45/-45/90]": [0, 45, -45, 90],
        "[0/60/-60]": [0, 60, -60]
    }

    selected_laminate = st.selectbox("Select Laminate", list(test_laminates.keys()))

    base_sequence = test_laminates[selected_laminate]

    # Calculate for different rotations
    rotations = np.linspace(0, 360, 73)
    results = {'A11': [], 'A22': [], 'A12': [], 'A66': [], 'A16': [], 'A26': []}

    for rot in rotations:
        rotated = [(angle + rot) % 360 for angle in base_sequence]
        rotated = [a if a <= 180 else a - 360 for a in rotated]
        lam = Laminate(material, rotated, ply_thickness)

        results['A11'].append(lam.A[0, 0])
        results['A22'].append(lam.A[1, 1])
        results['A12'].append(lam.A[0, 1])
        results['A66'].append(lam.A[2, 2])
        results['A16'].append(lam.A[0, 2])
        results['A26'].append(lam.A[1, 2])

    # Check quasi-isotropy
    A11_range = max(results['A11']) - min(results['A11'])
    A16_max = max(np.abs(results['A16']))
    is_quasi_iso = (A11_range < 0.01 * np.mean(results['A11']) and A16_max < 0.01)

    if is_quasi_iso:
        st.success(f"✓ {selected_laminate} is QUASI-ISOTROPIC")
    else:
        st.warning(f"✗ {selected_laminate} is NOT quasi-isotropic")

    # Plot results
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=rotations, y=results['A11'],
                            mode='lines', name='A₁₁', line=dict(width=2)))
    fig.add_trace(go.Scatter(x=rotations, y=results['A22'],
                            mode='lines', name='A₂₂', line=dict(width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=rotations, y=results['A66'],
                            mode='lines', name='A₆₆', line=dict(width=2)))

    fig.update_layout(
        title=f"Extensional Stiffness vs. Rotation - {selected_laminate}",
        xaxis_title="Rotation Angle (°)",
        yaxis_title="Stiffness (N/mm)",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Coupling terms
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=rotations, y=results['A16'],
                             mode='lines', name='A₁₆'))
    fig2.add_trace(go.Scatter(x=rotations, y=results['A26'],
                             mode='lines', name='A₂₆'))

    fig2.update_layout(
        title="Shear Coupling Terms",
        xaxis_title="Rotation Angle (°)",
        yaxis_title="Stiffness (N/mm)",
        height=400
    )

    st.plotly_chart(fig2, use_container_width=True)


def visualize_parametric_analysis(material, stacking_input, ply_thickness):
    """Interactive parametric analysis"""
    st.header("🎛️ Parametric Analysis")

    st.write("Explore how material properties and ply angles affect laminate behavior")

    analysis_type = st.selectbox(
        "Analysis Type",
        ["Ply Angle Variation", "Material Property Variation", "Thickness Variation"]
    )

    if analysis_type == "Ply Angle Variation":
        st.subheader("Vary Ply Angles")

        try:
            base_lam = Laminate(material, stacking_input, ply_thickness)
            n_plies = len(base_lam.stacking_sequence)

            ply_to_vary = st.slider("Select Ply to Vary", 1, n_plies, 1) - 1
            angle_range = st.slider("Angle Range (°)", -90, 90, (-90, 90))

            angles = np.linspace(angle_range[0], angle_range[1], 100)
            A11_vals, A22_vals, A12_vals, A66_vals = [], [], [], []

            for angle in angles:
                seq = base_lam.stacking_sequence.copy()
                seq[ply_to_vary] = angle
                lam = Laminate(material, seq, ply_thickness)
                A11_vals.append(lam.A[0, 0])
                A22_vals.append(lam.A[1, 1])
                A12_vals.append(lam.A[0, 1])
                A66_vals.append(lam.A[2, 2])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=angles, y=A11_vals, name='A₁₁', mode='lines'))
            fig.add_trace(go.Scatter(x=angles, y=A22_vals, name='A₂₂', mode='lines'))
            fig.add_trace(go.Scatter(x=angles, y=A12_vals, name='A₁₂', mode='lines'))
            fig.add_trace(go.Scatter(x=angles, y=A66_vals, name='A₆₆', mode='lines'))

            fig.update_layout(
                title=f"Effect of Ply {ply_to_vary + 1} Angle on [A] Matrix",
                xaxis_title=f"Ply {ply_to_vary + 1} Angle (°)",
                yaxis_title="Stiffness (N/mm)",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    elif analysis_type == "Material Property Variation":
        st.subheader("Vary Material Properties")

        property_to_vary = st.selectbox("Property to Vary", ["E1", "E2", "G12", "nu12"])

        if property_to_vary == "E1":
            values = np.linspace(50, 300, 50)
            ylabel = "E₁ (GPa)"
        elif property_to_vary == "E2":
            values = np.linspace(5, 50, 50)
            ylabel = "E₂ (GPa)"
        elif property_to_vary == "G12":
            values = np.linspace(2, 20, 50)
            ylabel = "G₁₂ (GPa)"
        else:
            values = np.linspace(0.15, 0.45, 50)
            ylabel = "ν₁₂"

        A11_vals, A22_vals, D11_vals = [], [], []

        for val in values:
            mat = material.copy()
            mat[property_to_vary] = val
            try:
                lam = Laminate(mat, stacking_input, ply_thickness)
                A11_vals.append(lam.A[0, 0])
                A22_vals.append(lam.A[1, 1])
                D11_vals.append(lam.D[0, 0])
            except:
                A11_vals.append(np.nan)
                A22_vals.append(np.nan)
                D11_vals.append(np.nan)

        col1, col2 = st.columns(2)

        with col1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=values, y=A11_vals, name='A₁₁', mode='lines'))
            fig1.add_trace(go.Scatter(x=values, y=A22_vals, name='A₂₂', mode='lines'))
            fig1.update_layout(
                title="Effect on [A] Matrix",
                xaxis_title=ylabel,
                yaxis_title="Stiffness (N/mm)",
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=values, y=D11_vals, name='D₁₁', mode='lines'))
            fig2.update_layout(
                title="Effect on [D] Matrix",
                xaxis_title=ylabel,
                yaxis_title="Bending Stiffness (N·mm)",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)


def visualize_stress_strain(material, stacking_input, ply_thickness):
    """Visualize stress and strain distributions"""
    st.header("📈 Stress/Strain Distribution")

    try:
        lam = Laminate(material, stacking_input, ply_thickness)

        st.subheader("Applied Loads")

        col1, col2, col3 = st.columns(3)

        with col1:
            Nx = st.number_input("Nx (N/m)", value=1000.0)
            Ny = st.number_input("Ny (N/m)", value=1000.0)
            Nxy = st.number_input("Nxy (N/m)", value=0.0)

        with col2:
            Mx = st.number_input("Mx (N)", value=0.0)
            My = st.number_input("My (N)", value=0.0)
            Mxy = st.number_input("Mxy (N)", value=0.0)

        loads = {'Nx': Nx, 'Ny': Ny, 'Nxy': Nxy, 'Mx': Mx, 'My': My, 'Mxy': Mxy}

        # Calculate strains and curvatures
        strains, curvatures = lam.calculate_strains_curvatures(loads)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Mid-Plane Strains**")
            st.write(f"εₓ⁰ = {strains[0]*1e6:.3f} με")
            st.write(f"εᵧ⁰ = {strains[1]*1e6:.3f} με")
            st.write(f"γₓᵧ⁰ = {strains[2]*1e6:.3f} με")

        with col2:
            st.write("**Curvatures**")
            st.write(f"κₓ = {curvatures[0]:.6f} mm⁻¹")
            st.write(f"κᵧ = {curvatures[1]:.6f} mm⁻¹")
            st.write(f"κₓᵧ = {curvatures[2]:.6f} mm⁻¹")

        # Calculate stresses through thickness
        st.subheader("Through-Thickness Distribution")

        z_plot = []
        sigma_x_plot = []
        sigma_y_plot = []
        tau_xy_plot = []
        sigma_1_plot = []
        sigma_2_plot = []

        for i in range(lam.n_plies):
            z_bottom = lam.z_coords[i]
            z_top = lam.z_coords[i+1]

            # Bottom
            stress_global_bot, stress_local_bot = lam.calculate_ply_stresses(
                strains, curvatures, i, 'bottom'
            )
            z_plot.append(z_bottom)
            sigma_x_plot.append(stress_global_bot[0])
            sigma_y_plot.append(stress_global_bot[1])
            tau_xy_plot.append(stress_global_bot[2])
            sigma_1_plot.append(stress_local_bot[0])
            sigma_2_plot.append(stress_local_bot[1])

            # Top
            stress_global_top, stress_local_top = lam.calculate_ply_stresses(
                strains, curvatures, i, 'top'
            )
            z_plot.append(z_top)
            sigma_x_plot.append(stress_global_top[0])
            sigma_y_plot.append(stress_global_top[1])
            tau_xy_plot.append(stress_global_top[2])
            sigma_1_plot.append(stress_local_top[0])
            sigma_2_plot.append(stress_local_top[1])

        col1, col2 = st.columns(2)

        with col1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=sigma_x_plot, y=z_plot, name='σₓ', mode='lines+markers'))
            fig1.add_trace(go.Scatter(x=sigma_y_plot, y=z_plot, name='σᵧ', mode='lines+markers'))
            fig1.add_trace(go.Scatter(x=tau_xy_plot, y=z_plot, name='τₓᵧ', mode='lines+markers'))

            # Add ply boundaries
            for z in lam.z_coords:
                fig1.add_hline(y=z, line_dash="dash", line_color="gray", opacity=0.3)

            fig1.update_layout(
                title="Global Stresses",
                xaxis_title="Stress (MPa)",
                yaxis_title="z (mm)",
                height=500
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=sigma_1_plot, y=z_plot, name='σ₁', mode='lines+markers'))
            fig2.add_trace(go.Scatter(x=sigma_2_plot, y=z_plot, name='σ₂', mode='lines+markers'))

            # Add ply boundaries
            for z in lam.z_coords:
                fig2.add_hline(y=z, line_dash="dash", line_color="gray", opacity=0.3)

            fig2.update_layout(
                title="Material Stresses",
                xaxis_title="Stress (MPa)",
                yaxis_title="z (mm)",
                height=500
            )
            st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
