"""
Configuration module for ASTRA HEALTH
NASA Space Apps Challenge - Deep-Space Medical Monitoring Suite
"""

PLANET_ENV = {
    "Earth (1.0G)": {
        "gravity": 1.0,
        "radiation_rate": 0.01,
        "neutron_ratio": 0.05,
        "delay_min": 0.0,
        "bone_loss_monthly": 0.0,
        "fluid_shift": "Normal terrestrial fluid distribution",
        "env_hazard": "Protected by Earth's magnetosphere and atmosphere"
    },
    "ISS / LEO (0.0G)": {
        "gravity": 0.0,
        "radiation_rate": 0.50,
        "neutron_ratio": 0.30,
        "delay_min": 0.0,
        "bone_loss_monthly": 1.5,
        "fluid_shift": "Cephalic fluid shift (Risk of SANS)",
        "env_hazard": "Closed-loop life support, microgravity, orbital debris"
    },
    "Moon / Gateway (0.16G)": {
        "gravity": 0.16,
        "radiation_rate": 0.65,
        "neutron_ratio": 0.32,
        "delay_min": 0.05,
        "bone_loss_monthly": 0.6,
        "fluid_shift": "Moderate upward fluid redistribution",
        "env_hazard": "Abrasive lunar regolith, extreme thermal fluctuations"
    },
    "Mars Transit / Surface (0.38G)": {
        "gravity": 0.38,
        "radiation_rate": 0.85,
        "neutron_ratio": 0.35,
        "delay_min": 22.0,
        "bone_loss_monthly": 0.8,
        "fluid_shift": "Partial gravitational adaptation",
        "env_hazard": "Perchlorate dust, Galactic Cosmic Rays (GCR), complete mission autonomy"
    }
}