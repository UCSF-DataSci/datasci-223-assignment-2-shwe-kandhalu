#!/usr/bin/env python3
"""
Emergency Room Medication Calculator

This script calculates medication dosages for emergency room patients based on 
standard emergency protocols. It follows weight-based dosing guidelines for common 
emergency medications.

Dosing Formula:
    Base Dosage (mg) = Patient Weight (kg) × Medication Factor (mg/kg)
    Loading Dose (mg) = Base Dosage × 2 (for first dose only)

When to use Loading Doses:
    - Only for first doses of certain medications (e.g., antibiotics, anti-seizure meds)
    - Determined by 'is_first_dose' flag in the input
    - Some medications always use loading doses for first administration

Example:
    Patient: 70kg, Medication: epinephrine, Is First Dose: No
    Base Dosage = 70 kg × 0.01 mg/kg = 0.7 mg
    Final Dosage = 0.7 mg

    Patient: 70kg, Medication: amiodarone, Is First Dose: Yes
    Base Dosage = 70 kg × 5 mg/kg = 350 mg
    Loading Dose = 350 mg × 2 = 700 mg
    Final Dosage = 700 mg

Input Format:
    {
        "name": "John Smith",
        "weight": 70.0,
        "medication": "epinephrine",
        "condition": "anaphylaxis",
        "is_first_dose": false,
        "allergies": ["penicillin"]
    }

Output:
    {
        "name": "John Smith",
        "weight": 70.0,
        "medication": "epinephrine",
        "base_dosage": 0.7,
        "is_first_dose": false,
        "loading_dose_applied": false,
        "final_dosage": 0.7,
        "warnings": ["Monitor for arrhythmias"]
    }

Medication Factors (mg/kg):
    epinephrine:  0.01  (Anaphylaxis)
    amiodarone:   5.00  (Cardiac arrest)
    lorazepam:    0.05  (Seizures)
    fentanyl:     0.001 (Pain)
    ...
"""

import json
import os
import sys

# Dosage factors for different medications (mg per kg of body weight)
# These are standard dosing factors based on medical guidelines
DOSAGE_FACTORS = {
    "epinephrine": 0.01,  # Anaphylaxis
    "amiodarone": 5.00,   # Cardiac arrest
    "lorazepam": 0.05,    # Seizures
    "fentanyl": 0.001,    # Pain
    "lisinopril": 0.5,    # ACE inhibitor for blood pressure
    "metformin": 10.0,    # Diabetes medication
    "oseltamivir": 2.5,   # Antiviral for influenza
    "sumatriptan": 1.0,   # Migraine medication
    "albuterol": 0.1,     # Asthma medication
    "ibuprofen": 5.0,     # Pain/inflammation
    "sertraline": 1.5,    # Antidepressant
    "levothyroxine": 0.02 # Thyroid medication
}

# Medications that use loading doses for first administration
# BUG: Missing commas and typo in "fentynal"
# FIX: Added commas and corrected spelling to "fentanyl"
LOADING_DOSE_MEDICATIONS = [
    "amiodarone",
    "lorazepam",
    "fentanyl"
]

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """

    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # BUG: No error handling for file not found
        # FIX: Adding error checking for file not found
        print("File not found!")
        sys.exit(1)

def calculate_dosage(patient):
    patient_with_dosage = patient.copy()

    # BUG: No checks for keys
    # FIX: Defensive checks for required fields
    weight = patient.get("weight")
    medication = patient.get("medication")
    is_first_dose = patient.get("is_first_dose", False)

    if weight is None or medication is None:
        print("Missing required patient data: weight or medication.")
        return patient_with_dosage

    factor = DOSAGE_FACTORS.get(medication, 0)
    base_dosage = weight * factor  # FIX: Was using addition

    loading_dose_applied = False
    final_dosage = base_dosage

    # BUG: Missed loading dose application logic
    # FIX: Apply if first dose AND medication requires it
    if is_first_dose and medication in LOADING_DOSE_MEDICATIONS:
        loading_dose_applied = True
        final_dosage = base_dosage * 2  # FIX: Was using addition

    # Add dosage info
    patient_with_dosage["base_dosage"] = base_dosage
    patient_with_dosage["loading_dose_applied"] = loading_dose_applied
    patient_with_dosage["final_dosage"] = final_dosage

    # Warnings based on medication
    warnings = []
    if medication == "epinephrine":
        warnings.append("Monitor for arrhythmias")
    elif medication == "amiodarone":
        warnings.append("Monitor for hypotension")
    elif medication == "fentanyl":
        warnings.append("Monitor for respiratory depression")

    patient_with_dosage["warnings"] = warnings

    return patient_with_dosage

def calculate_all_dosages(patients):
    total_medication = 0
    patients_with_dosages = []

    for patient in patients:
        patient_with_dosage = calculate_dosage(patient)
        patients_with_dosages.append(patient_with_dosage)

        final_dosage = patient_with_dosage.get("final_dosage")
        if final_dosage is not None:
            total_medication += final_dosage
        else:
            # BUG: Tried adding None
            # FIX: Skip if final_dosage not found
            print("Warning: Missing final dosage, skipping in total.")

    return patients_with_dosages, total_medication

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', 'raw', 'meds.json')

    patients = load_patient_data(data_path)
    patients_with_dosages, total_medication = calculate_all_dosages(patients)

    print("Medication Dosages:")
    for patient in patients_with_dosages:
        required_keys = ['name', 'medication', 'base_dosage', 'final_dosage']
        if not all(key in patient for key in required_keys):
            # BUG: Crashes if keys missing
            # FIX: Skip if essential info missing
            print("Error: Missing required keys. Skipping.")
            continue

        print(f"Name: {patient['name']}, Medication: {patient['medication']}, "
              f"Base Dosage: {patient['base_dosage']:.2f} mg, "
              f"Final Dosage: {patient['final_dosage']:.2f} mg")

        if patient["loading_dose_applied"]:
            print("  * Loading dose applied")
        if patient["warnings"]:
            print("  * Warnings:", ", ".join(patient["warnings"]))

    print(f"\nTotal medication needed: {total_medication:.2f} mg")
    return patients_with_dosages, total_medication

if __name__ == "__main__":
    main()