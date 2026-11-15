"""
Physiological Simulation Engine, CANS Radiation Model & Autonomous AI Triage
"""
import random
from datetime import datetime

# Встроенные константы сред миссии (без внешних зависимостей)
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

def generate_telemetry(crew_id, planet, solar_flare=False):
    env = PLANET_ENV.get(planet, PLANET_ENV["Mars Transit / Surface (0.38G)"])
    rad_multiplier = 45.0 if solar_flare else 1.0

    if solar_flare:
        heart_rate = random.randint(115, 148)
        spo2 = random.randint(86, 92)
        stress_level = random.randint(80, 99)
        systolic = random.randint(145, 168)
        diastolic = random.randint(92, 108)
        body_temp = round(random.uniform(37.4, 38.2), 1)
    else:
        base_shift = 4 if env["gravity"] == 0.0 else 0
        heart_rate = random.randint(62 + base_shift, 82 + base_shift)
        spo2 = random.randint(96, 99)
        stress_level = random.randint(12, 36)
        systolic = random.randint(110, 128)
        diastolic = random.randint(70, 84)
        body_temp = round(random.uniform(36.4, 36.9), 1)

    total_rad = round(env["radiation_rate"] * rad_multiplier * random.uniform(0.92, 1.08), 2)
    neutron_dose = round(total_rad * env["neutron_ratio"], 2)
    gamma_dose = round(total_rad - neutron_dose, 2)

    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "crew_id": crew_id,
        "heart_rate": heart_rate,
        "spo2": spo2,
        "stress_level": stress_level,
        "systolic": systolic,
        "diastolic": diastolic,
        "body_temp": body_temp,
        "total_radiation": total_rad,
        "neutron_dose": neutron_dose,
        "gamma_dose": gamma_dose,
        "radiation_msev": total_rad,
        "delay": env["delay_min"]
    }

def get_nasa_hrp_risks(planet, solar_flare=False):
    env = PLANET_ENV.get(planet, PLANET_ENV["Mars Transit / Surface (0.38G)"])
    risks = []

    sans_status = "Warning" if env["gravity"] < 0.5 else "Nominal"
    risks.append({
        "system": "Ocular & Central Nervous System (SANS Risk)",
        "status": sans_status,
        "desc": f"{env['fluid_shift']}. Potential optic disc edema and intracranial pressure elevation."
    })

    bone_status = "Critical" if env["bone_loss_monthly"] >= 1.0 else ("Warning" if env["bone_loss_monthly"] > 0 else "Nominal")
    risks.append({
        "system": "Musculoskeletal System (Bone Density Loss)",
        "status": bone_status,
        "desc": f"Projected bone mineral degradation: {env['bone_loss_monthly']}% per month. Mandatory ARED resistance exercise protocols required."
    })

    if solar_flare:
        risks.append({
            "system": "Radiation Safety (CANS Active Neutron Alert)",
            "status": "CRITICAL EMERGENCY",
            "desc": "Solar Particle Event (SPE) detected! High-energy neutron and proton flux exceeds safe habitat limits."
        })
    else:
        risks.append({
            "system": "Radiation Safety (CANS Spectrometer)",
            "status": "Nominal",
            "desc": f"Neutron radiation component (~{int(env['neutron_ratio']*100)}% of background) monitored continuously by CANS."
        })

    risks.append({
        "system": "Immunology & Microbiome (Closed Ecosystem)",
        "status": "Monitoring",
        "desc": f"Environmental factors: {env['env_hazard']}. Risk of latent virus reactivation and biomarker shifts."
    })

    auto_status = "Warning" if env["delay_min"] > 5.0 else "Nominal"
    risks.append({
        "system": "Behavioral Health & Autonomy (Deep Space Distance)",
        "status": auto_status,
        "desc": f"Communication delay with Mission Control: {env['delay_min']} minutes. Autonomous medical triage active."
    })

    return risks

def run_autonomous_ai_triage(telemetry, planet, solar_flare=False):
    hr = telemetry.get("heart_rate", 72)
    spo2 = telemetry.get("spo2", 98)
    stress = telemetry.get("stress_level", 20)
    rad = telemetry.get("total_radiation", 0.1)
    neutrons = telemetry.get("neutron_dose", 0.03)

    diagnoses = []
    recommendations = []

    if solar_flare or rad > 10.0:
        diagnoses.append(f"CRITICAL HAZARD: Acute Radiation Exposure ({rad} mSv, CANS Neutron component: {neutrons} mSv).")
        recommendations.append("Immediately transfer crew to the central water-shielded radiation shelter.")
        recommendations.append("Suspend all Extravehicular Activities (EVA) and administer prophylactic countermeasures.")

    if hr > 105:
        diagnoses.append(f"Tachycardia Detected ({hr} bpm): Elevated cardiovascular strain.")
        recommendations.append("Cease strenuous physical activity, ensure hydration, and verify electrolyte balance.")

    if spo2 < 93:
        diagnoses.append(f"Hypoxia Warning (SpO2: {spo2}%): Reduced tissue oxygen saturation.")
        recommendations.append("Inspect cabin O2 partial pressure and CO2 scrubbers; prepare auxiliary oxygen masks.")

    if stress > 75:
        diagnoses.append(f"Behavioral Drift (Stress Index: {stress}/100): High psychological and cognitive burden.")
        recommendations.append("Initiate 4-hour operational stand-down, private comms buffer with family, and circadian adjustment.")

    if not diagnoses:
        diagnoses.append("All vital signs and biomarker profiles operating within acceptable deep-space adaptation limits.")
        recommendations.append(f"Continue scheduled mission tasks in {planet} environment. Perform daily ARED workout and visual acuity check.")

    return diagnoses, recommendations