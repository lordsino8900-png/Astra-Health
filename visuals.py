"""
Plotly 3D Anatomical Body Map and Time-Series Visualizations
"""
import plotly.graph_objects as go
import numpy as np

def render_3d_anatomical_body(selected_zone="All Systems", alert=False):
    fig = go.Figure()
    
    # Body wireframe outline
    z_body = np.linspace(-1.5, 1.5, 35)
    x_body = np.sin(z_body * np.pi) * 0.35
    y_body = np.cos(z_body * np.pi) * 0.25
    
    fig.add_trace(go.Scatter3d(
        x=x_body, y=y_body, z=z_body,
        mode='markers',
        marker=dict(size=3, color='rgba(100, 150, 255, 0.25)', symbol='circle'),
        name='Body Frame'
    ))
    
    # NASA HRP Risk Zones
    zones = {
        "Ocular & Brain (SANS)": ([0], [0.35], [1.6], "Optic disc edema & intracranial pressure"),
        "Cardiovascular System": ([0.1], [0.1], [0.5], "Zero-G fluid shift & cardiac adaptation"),
        "Immune / Bone Marrow": ([0], [0], [0.2], "Immune biomarker shifts & hematopoiesis"),
        "Spine & Bone Density": ([0]*6, [0]*6, np.linspace(-0.8, 0.8, 6), "Calcium leaching & skeletal degradation")
    }
    
    for zone_name, (ox, oy, oz, desc) in zones.items():
        if alert:
            color = '#FF3333'
        else:
            color = '#00FF66' if selected_zone == "All Systems" or selected_zone == zone_name else '#444444'
        
        size = 11 if selected_zone == zone_name else 7
        
        fig.add_trace(go.Scatter3d(
            x=ox, y=oy, z=oz,
            mode='markers+text',
            marker=dict(size=size, color=color, symbol='diamond'),
            text=[zone_name]*len(ox),
            textposition="top center",
            name=zone_name
        ))
        
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(font=dict(color='white', size=11), orientation="h")
    )
    return fig

def render_telemetry_timeseries(df_history):
    fig = go.Figure()
    if not df_history.empty:
        fig.add_trace(go.Scatter(
            x=df_history['timestamp'], y=df_history['heart_rate'],
            mode='lines+markers', name='Heart Rate (bpm)', line=dict(color='#00FF66', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df_history['timestamp'], y=df_history['stress_level'],
            mode='lines+markers', name='Stress Index', line=dict(color='#FF9900', width=2)
        ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.15),
        xaxis=dict(gridcolor='#222630'),
        yaxis=dict(gridcolor='#222630')
    )
    return fig