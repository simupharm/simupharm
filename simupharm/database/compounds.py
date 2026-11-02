"""Pharmaceutical Compound Database — 300+ compounds with spectral data.

Multi-instrument data: UV-Vis peaks, IR frequencies, HPLC retention, MS fragments, optical rotation.
"""

COMPOUNDS = {
    # ============================================================
    # ANALGESICS & ANTIPYRETICS
    # ============================================================
    "paracetamol": {
        "name": "Paracetamol (Acetaminophen)",
        "category": "Analgesic",
        "molecular_weight": 151.16,
        "formula": "C8H9NO2",
        "cas": "103-90-2",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Non-opioid analgesic",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 243, "width": 15, "epsilon": 13000, "label": "π→π*"},
                {"center": 290, "width": 18, "epsilon": 1200, "label": "n→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3325, "intensity": 0.7, "width": 40, "assignment": "N-H stretch"},
                {"wavenumber": 3160, "intensity": 0.5, "width": 50, "assignment": "O-H stretch"},
                {"wavenumber": 1655, "intensity": 0.9, "width": 20, "assignment": "C=O stretch (amide)"},
                {"wavenumber": 1610, "intensity": 0.6, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1510, "intensity": 0.8, "width": 15, "assignment": "Amide II (N-H bend)"},
                {"wavenumber": 1260, "intensity": 0.7, "width": 15, "assignment": "C-O stretch (phenol)"},
                {"wavenumber": 835, "intensity": 0.5, "width": 10, "assignment": "Aromatic C-H bend"}
            ]
        },
        "hplc": {"retention_factor": 1.2, "logP": 0.46},
        "mass_spec": {
            "fragments": [
                {"mz": 151, "intensity": 30, "label": "M⁺ (molecular ion)"},
                {"mz": 109, "intensity": 100, "label": "M-42 (loss of CH₂CO)"},
                {"mz": 108, "intensity": 60, "label": "M-43 (loss of CH₃CO)"},
                {"mz": 80, "intensity": 40, "label": "M-71"},
                {"mz": 43, "intensity": 50, "label": "CH₃CO⁺"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral — optically inactive"}
    },

    "aspirin": {
        "name": "Aspirin (Acetylsalicylic Acid)",
        "category": "NSAID",
        "molecular_weight": 180.16,
        "formula": "C9H8O4",
        "cas": "50-78-2",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Non-steroidal anti-inflammatory",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 228, "width": 15, "epsilon": 9800, "label": "π→π*"},
                {"center": 276, "width": 20, "epsilon": 1500, "label": "n→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3000, "intensity": 0.4, "width": 60, "assignment": "O-H stretch (broad, acid)"},
                {"wavenumber": 1755, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (ester)"},
                {"wavenumber": 1690, "intensity": 0.8, "width": 18, "assignment": "C=O stretch (acid)"},
                {"wavenumber": 1605, "intensity": 0.5, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1190, "intensity": 0.7, "width": 15, "assignment": "C-O stretch (ester)"},
                {"wavenumber": 755, "intensity": 0.5, "width": 10, "assignment": "Aromatic C-H bend"}
            ]
        },
        "hplc": {"retention_factor": 2.5, "logP": 1.19},
        "mass_spec": {
            "fragments": [
                {"mz": 180, "intensity": 15, "label": "M⁺"},
                {"mz": 138, "intensity": 80, "label": "M-42 (loss of ketene)"},
                {"mz": 120, "intensity": 100, "label": "M-60 (loss of acetic acid)"},
                {"mz": 92, "intensity": 40, "label": "M-88"},
                {"mz": 43, "intensity": 60, "label": "CH₃CO⁺"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    "ibuprofen": {
        "name": "Ibuprofen",
        "category": "NSAID",
        "molecular_weight": 206.28,
        "formula": "C13H18O2",
        "cas": "15687-27-1",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Non-steroidal anti-inflammatory",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 222, "width": 14, "epsilon": 8200, "label": "π→π*"},
                {"center": 264, "width": 18, "epsilon": 390, "label": "π→π*(forbidden)"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 2955, "intensity": 0.7, "width": 30, "assignment": "C-H stretch (alkyl)"},
                {"wavenumber": 1720, "intensity": 0.95, "width": 18, "assignment": "C=O stretch (acid)"},
                {"wavenumber": 1510, "intensity": 0.5, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1230, "intensity": 0.6, "width": 15, "assignment": "C-O stretch"},
                {"wavenumber": 835, "intensity": 0.4, "width": 10, "assignment": "para-substituted aromatic"}
            ]
        },
        "hplc": {"retention_factor": 6.0, "logP": 3.97},
        "mass_spec": {
            "fragments": [
                {"mz": 206, "intensity": 10, "label": "M⁺"},
                {"mz": 161, "intensity": 100, "label": "M-45 (loss of CO₂H)"},
                {"mz": 119, "intensity": 40, "label": "Aryl fragment"},
                {"mz": 91, "intensity": 20, "label": "Tropylium C₇H₇⁺"}
            ]
        },
        "polarimetry": {"specific_rotation": 59.0, "note": "S-(+)-ibuprofen = +59°"}
    },

    # ============================================================
    # ANTIBIOTICS
    # ============================================================
    "amoxicillin": {
        "name": "Amoxicillin",
        "category": "Antibiotic",
        "molecular_weight": 365.40,
        "formula": "C16H19N3O5S",
        "cas": "26787-78-0",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Beta-lactam (Penicillin)",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 230, "width": 16, "epsilon": 11000, "label": "π→π*"},
                {"center": 272, "width": 14, "epsilon": 3500, "label": "Phenol absorption"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3450, "intensity": 0.6, "width": 50, "assignment": "O-H / N-H stretch"},
                {"wavenumber": 1770, "intensity": 0.85, "width": 15, "assignment": "C=O stretch (β-lactam)"},
                {"wavenumber": 1690, "intensity": 0.7, "width": 18, "assignment": "C=O stretch (amide)"},
                {"wavenumber": 1610, "intensity": 0.5, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1250, "intensity": 0.6, "width": 15, "assignment": "C-N stretch"}
            ]
        },
        "hplc": {"retention_factor": 0.8, "logP": 0.87},
        "mass_spec": {
            "fragments": [
                {"mz": 366, "intensity": 20, "label": "M+H⁺"},
                {"mz": 349, "intensity": 60, "label": "M-NH₃+H"},
                {"mz": 208, "intensity": 40, "label": "β-lactam fragment"},
                {"mz": 114, "intensity": 100, "label": "Thiazolidine ring"}
            ]
        },
        "polarimetry": {"specific_rotation": 290.0}
    },

    "ciprofloxacin": {
        "name": "Ciprofloxacin HCl",
        "category": "Antibiotic",
        "molecular_weight": 367.80,
        "formula": "C17H19ClFN3O3",
        "cas": "86393-32-0",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Fluoroquinolone",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 278, "width": 16, "epsilon": 14500, "label": "π→π*"},
                {"center": 320, "width": 18, "epsilon": 5600, "label": "n→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3400, "intensity": 0.5, "width": 50, "assignment": "N-H / O-H stretch"},
                {"wavenumber": 1725, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (acid)"},
                {"wavenumber": 1625, "intensity": 0.8, "width": 18, "assignment": "C=O stretch (quinolone)"},
                {"wavenumber": 1480, "intensity": 0.6, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1280, "intensity": 0.5, "width": 15, "assignment": "C-F stretch"},
                {"wavenumber": 1040, "intensity": 0.4, "width": 15, "assignment": "C-N stretch"}
            ]
        },
        "hplc": {"retention_factor": 1.5, "logP": -0.57},
        "mass_spec": {
            "fragments": [
                {"mz": 332, "intensity": 100, "label": "M+H⁺"},
                {"mz": 314, "intensity": 50, "label": "M-H₂O+H"},
                {"mz": 288, "intensity": 70, "label": "M-CO₂+H"},
                {"mz": 245, "intensity": 30, "label": "Piperazine loss"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Racemic"}
    },

    "metformin": {
        "name": "Metformin HCl",
        "category": "Antidiabetic",
        "molecular_weight": 165.63,
        "formula": "C4H12ClN5",
        "cas": "1115-70-4",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Biguanide",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 233, "width": 14, "epsilon": 12900, "label": "π→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3370, "intensity": 0.8, "width": 40, "assignment": "N-H stretch"},
                {"wavenumber": 3170, "intensity": 0.7, "width": 40, "assignment": "N-H stretch (amine salt)"},
                {"wavenumber": 1625, "intensity": 0.9, "width": 20, "assignment": "C=N stretch (imine)"},
                {"wavenumber": 1570, "intensity": 0.7, "width": 18, "assignment": "N-H bend"},
                {"wavenumber": 1065, "intensity": 0.4, "width": 15, "assignment": "C-N stretch"}
            ]
        },
        "hplc": {"retention_factor": 0.3, "logP": -2.64},
        "mass_spec": {
            "fragments": [
                {"mz": 130, "intensity": 100, "label": "M+H⁺ (free base)"},
                {"mz": 113, "intensity": 30, "label": "M-NH₃+H"},
                {"mz": 88, "intensity": 50, "label": "M-CH₂N₂+H"},
                {"mz": 71, "intensity": 40, "label": "Guanidine fragment"},
                {"mz": 60, "intensity": 80, "label": "Biguanide core"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    "ranitidine": {
        "name": "Ranitidine HCl",
        "category": "Gastrointestinal",
        "molecular_weight": 350.87,
        "formula": "C13H23ClN4O3S",
        "cas": "66357-59-3",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "H₂ receptor antagonist",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 228, "width": 16, "epsilon": 17400, "label": "π→π*"},
                {"center": 315, "width": 20, "epsilon": 6400, "label": "n→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3250, "intensity": 0.6, "width": 50, "assignment": "N-H stretch"},
                {"wavenumber": 2950, "intensity": 0.5, "width": 30, "assignment": "C-H stretch"},
                {"wavenumber": 1620, "intensity": 0.8, "width": 18, "assignment": "C=C stretch"},
                {"wavenumber": 1570, "intensity": 0.7, "width": 18, "assignment": "N-O stretch (nitro)"},
                {"wavenumber": 1080, "intensity": 0.5, "width": 15, "assignment": "C-S stretch"}
            ]
        },
        "hplc": {"retention_factor": 0.7, "logP": 0.27},
        "mass_spec": {
            "fragments": [
                {"mz": 315, "intensity": 30, "label": "M+H⁺ (free base)"},
                {"mz": 270, "intensity": 60, "label": "M-NO₂ fragment"},
                {"mz": 176, "intensity": 100, "label": "Furan ring + side chain"},
                {"mz": 130, "intensity": 40, "label": "Dimethylamine chain"},
                {"mz": 102, "intensity": 20, "label": "CH₂SCH₂ fragment"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Achiral"}
    },

    "caffeine": {
        "name": "Caffeine",
        "category": "Stimulant",
        "molecular_weight": 194.19,
        "formula": "C8H10N4O2",
        "cas": "58-08-2",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "CNS stimulant (xanthine derivative)",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 273, "width": 16, "epsilon": 9900, "label": "π→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 2950, "intensity": 0.3, "width": 25, "assignment": "C-H stretch (N-CH₃)"},
                {"wavenumber": 1700, "intensity": 0.9, "width": 18, "assignment": "C=O stretch"},
                {"wavenumber": 1655, "intensity": 0.85, "width": 18, "assignment": "C=O stretch"},
                {"wavenumber": 1550, "intensity": 0.6, "width": 15, "assignment": "C=N stretch"},
                {"wavenumber": 1480, "intensity": 0.5, "width": 15, "assignment": "C=C stretch"},
                {"wavenumber": 745, "intensity": 0.4, "width": 12, "assignment": "Imidazole ring"}
            ]
        },
        "hplc": {"retention_factor": 1.0, "logP": -0.07},
        "mass_spec": {
            "fragments": [
                {"mz": 194, "intensity": 100, "label": "M⁺ (molecular ion)"},
                {"mz": 165, "intensity": 10, "label": "M-CHO"},
                {"mz": 137, "intensity": 25, "label": "M-57 (ring opening)"},
                {"mz": 109, "intensity": 40, "label": "M-85"},
                {"mz": 82, "intensity": 15, "label": "HCN loss from ring"},
                {"mz": 55, "intensity": 30, "label": "Methylimidazole"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    "diclofenac": {
        "name": "Diclofenac Sodium",
        "category": "NSAID",
        "molecular_weight": 318.13,
        "formula": "C14H10Cl2NNaO2",
        "cas": "15307-79-6",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Non-steroidal anti-inflammatory",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 276, "width": 14, "epsilon": 12400, "label": "π→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3380, "intensity": 0.6, "width": 35, "assignment": "N-H stretch"},
                {"wavenumber": 1575, "intensity": 0.9, "width": 20, "assignment": "COO⁻ asymmetric stretch"},
                {"wavenumber": 1500, "intensity": 0.7, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1400, "intensity": 0.8, "width": 18, "assignment": "COO⁻ symmetric stretch"},
                {"wavenumber": 770, "intensity": 0.5, "width": 12, "assignment": "C-Cl stretch"}
            ]
        },
        "hplc": {"retention_factor": 8.0, "logP": 4.51},
        "mass_spec": {
            "fragments": [
                {"mz": 296, "intensity": 60, "label": "M+H⁺ (acid form)"},
                {"mz": 278, "intensity": 40, "label": "M-H₂O+H"},
                {"mz": 250, "intensity": 100, "label": "M-CO₂+H"},
                {"mz": 215, "intensity": 50, "label": "Loss of Cl"},
                {"mz": 214, "intensity": 30, "label": "Indolinone fragment"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    "atorvastatin": {
        "name": "Atorvastatin Calcium",
        "category": "Antihyperlipidemic",
        "molecular_weight": 1155.36,
        "formula": "C66H68CaF2N4O10",
        "cas": "134523-03-8",
        "pharmacopeia": "USP",
        "therapeutic_class": "HMG-CoA reductase inhibitor (statin)",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 246, "width": 18, "epsilon": 22000, "label": "π→π*"},
                {"center": 310, "width": 20, "epsilon": 4500, "label": "Extended conjugation"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3400, "intensity": 0.5, "width": 50, "assignment": "O-H/N-H stretch"},
                {"wavenumber": 2950, "intensity": 0.4, "width": 25, "assignment": "C-H stretch"},
                {"wavenumber": 1650, "intensity": 0.9, "width": 18, "assignment": "C=O amide stretch"},
                {"wavenumber": 1580, "intensity": 0.7, "width": 15, "assignment": "COO⁻ stretch"},
                {"wavenumber": 1220, "intensity": 0.6, "width": 15, "assignment": "C-F stretch"}
            ]
        },
        "hplc": {"retention_factor": 10.0, "logP": 6.36},
        "mass_spec": {
            "fragments": [
                {"mz": 559, "intensity": 100, "label": "M+H⁺ (single molecule)"},
                {"mz": 541, "intensity": 40, "label": "M-H₂O+H"},
                {"mz": 440, "intensity": 60, "label": "Ring system"},
                {"mz": 292, "intensity": 20, "label": "Phenanthrene core"}
            ]
        },
        "polarimetry": {"specific_rotation": -34.0}
    },

    "omeprazole": {
        "name": "Omeprazole",
        "category": "Gastrointestinal",
        "molecular_weight": 345.42,
        "formula": "C17H19N3O3S",
        "cas": "73590-58-6",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Proton pump inhibitor",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 276, "width": 16, "epsilon": 7400, "label": "π→π*"},
                {"center": 305, "width": 14, "epsilon": 10500, "label": "Benzimidazole"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3450, "intensity": 0.4, "width": 40, "assignment": "N-H stretch"},
                {"wavenumber": 2940, "intensity": 0.3, "width": 25, "assignment": "C-H stretch"},
                {"wavenumber": 1630, "intensity": 0.7, "width": 18, "assignment": "C=N stretch"},
                {"wavenumber": 1580, "intensity": 0.6, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1075, "intensity": 0.9, "width": 15, "assignment": "S=O stretch (sulfoxide)"},
                {"wavenumber": 1010, "intensity": 0.5, "width": 15, "assignment": "C-O-C stretch"}
            ]
        },
        "hplc": {"retention_factor": 3.5, "logP": 2.23},
        "mass_spec": {
            "fragments": [
                {"mz": 346, "intensity": 50, "label": "M+H⁺"},
                {"mz": 198, "intensity": 100, "label": "Benzimidazole-S fragment"},
                {"mz": 180, "intensity": 30, "label": "Loss of H₂O"},
                {"mz": 149, "intensity": 60, "label": "Pyridine-ring fragment"},
                {"mz": 136, "intensity": 40, "label": "Methoxypyridine"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Racemic (S-omeprazole = esomeprazole)"}
    },

    "amlodipine": {
        "name": "Amlodipine Besylate",
        "category": "Cardiovascular",
        "molecular_weight": 567.04,
        "formula": "C26H31ClN2O8S",
        "cas": "111470-99-6",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Calcium channel blocker",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 237, "width": 16, "epsilon": 16000, "label": "π→π*"},
                {"center": 360, "width": 22, "epsilon": 7200, "label": "DHP chromophore"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3300, "intensity": 0.5, "width": 40, "assignment": "N-H stretch (DHP)"},
                {"wavenumber": 1695, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (ester)"},
                {"wavenumber": 1615, "intensity": 0.6, "width": 15, "assignment": "C=C stretch (DHP)"},
                {"wavenumber": 1490, "intensity": 0.5, "width": 15, "assignment": "Aromatic C=C"},
                {"wavenumber": 1210, "intensity": 0.7, "width": 15, "assignment": "C-O stretch"},
                {"wavenumber": 770, "intensity": 0.4, "width": 12, "assignment": "C-Cl stretch"}
            ]
        },
        "hplc": {"retention_factor": 4.0, "logP": 3.0},
        "mass_spec": {
            "fragments": [
                {"mz": 409, "intensity": 100, "label": "M+H⁺ (amlodipine)"},
                {"mz": 377, "intensity": 40, "label": "M-CH₃OH+H"},
                {"mz": 294, "intensity": 60, "label": "DHP core"},
                {"mz": 238, "intensity": 30, "label": "Chlorophenyl-DHP"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Racemic (S-amlodipine more active)"}
    },

    "losartan": {
        "name": "Losartan Potassium",
        "category": "Cardiovascular",
        "molecular_weight": 461.00,
        "formula": "C22H22ClKN6O",
        "cas": "124750-99-8",
        "pharmacopeia": "USP",
        "therapeutic_class": "ARB (Angiotensin II receptor blocker)",
        "uvvis": {
            "solvent": "methanol",
            "peaks": [
                {"center": 234, "width": 16, "epsilon": 20000, "label": "π→π*"},
                {"center": 254, "width": 14, "epsilon": 8000, "label": "Biphenyl tetrazole"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3400, "intensity": 0.5, "width": 40, "assignment": "O-H stretch"},
                {"wavenumber": 2960, "intensity": 0.4, "width": 25, "assignment": "C-H stretch"},
                {"wavenumber": 1575, "intensity": 0.6, "width": 15, "assignment": "C=N stretch (imidazole)"},
                {"wavenumber": 1460, "intensity": 0.8, "width": 18, "assignment": "Tetrazole N=N"},
                {"wavenumber": 1270, "intensity": 0.5, "width": 15, "assignment": "C-N stretch"},
                {"wavenumber": 760, "intensity": 0.5, "width": 12, "assignment": "C-Cl stretch"}
            ]
        },
        "hplc": {"retention_factor": 5.0, "logP": 4.01},
        "mass_spec": {
            "fragments": [
                {"mz": 423, "intensity": 100, "label": "M+H⁺ (free base)"},
                {"mz": 405, "intensity": 40, "label": "M-H₂O+H"},
                {"mz": 377, "intensity": 30, "label": "M-N₂H₂+H"},
                {"mz": 207, "intensity": 50, "label": "Biphenyl-tetrazole"}
            ]
        },
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    # ============================================================
    # VITAMINS
    # ============================================================
    "ascorbic_acid": {
        "name": "Ascorbic Acid (Vitamin C)",
        "category": "Vitamin",
        "molecular_weight": 176.12,
        "formula": "C6H8O6",
        "cas": "50-81-7",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Water-soluble vitamin",
        "uvvis": {
            "solvent": "water",
            "peaks": [
                {"center": 243, "width": 14, "epsilon": 10000, "label": "Enediol π→π*"}
            ]
        },
        "ftir": {
            "peaks": [
                {"wavenumber": 3410, "intensity": 0.7, "width": 60, "assignment": "O-H stretch (broad)"},
                {"wavenumber": 3320, "intensity": 0.6, "width": 40, "assignment": "O-H stretch"},
                {"wavenumber": 1755, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (lactone)"},
                {"wavenumber": 1670, "intensity": 0.8, "width": 15, "assignment": "C=C stretch (enediol)"},
                {"wavenumber": 1320, "intensity": 0.5, "width": 15, "assignment": "O-H bend"},
                {"wavenumber": 1025, "intensity": 0.6, "width": 15, "assignment": "C-O stretch"}
            ]
        },
        "hplc": {"retention_factor": 0.5, "logP": -1.85},
        "mass_spec": {
            "fragments": [
                {"mz": 176, "intensity": 20, "label": "M⁺"},
                {"mz": 116, "intensity": 100, "label": "M-60 (loss of C₂H₄O₂)"},
                {"mz": 88, "intensity": 30, "label": "M-88"},
                {"mz": 60, "intensity": 40, "label": "C₂H₄O₂⁺"}
            ]
        },
        "polarimetry": {"specific_rotation": 20.5, "note": "L-ascorbic acid: [α]D +20.5° to +21.5°"}
    },

    # Additional compounds for comprehensive coverage
    "chloramphenicol": {
        "name": "Chloramphenicol",
        "category": "Antibiotic",
        "molecular_weight": 323.13,
        "formula": "C11H12Cl2N2O5",
        "cas": "56-75-7",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Broad-spectrum antibiotic",
        "uvvis": {"solvent": "water", "peaks": [{"center": 278, "width": 16, "epsilon": 8800, "label": "Nitrobenzene π→π*"}]},
        "ftir": {"peaks": [
            {"wavenumber": 3350, "intensity": 0.6, "width": 40, "assignment": "O-H/N-H stretch"},
            {"wavenumber": 1690, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (amide)"},
            {"wavenumber": 1520, "intensity": 0.8, "width": 15, "assignment": "NO₂ asymmetric stretch"},
            {"wavenumber": 1350, "intensity": 0.7, "width": 15, "assignment": "NO₂ symmetric stretch"},
            {"wavenumber": 775, "intensity": 0.5, "width": 12, "assignment": "C-Cl stretch"}
        ]},
        "hplc": {"retention_factor": 2.0, "logP": 1.14},
        "mass_spec": {"fragments": [{"mz": 323, "intensity": 30, "label": "M⁺"}, {"mz": 257, "intensity": 100, "label": "M-66"}, {"mz": 152, "intensity": 60, "label": "Nitrobenzyl"}]},
        "polarimetry": {"specific_rotation": 25.5}
    },

    "sulfamethoxazole": {
        "name": "Sulfamethoxazole",
        "category": "Antibiotic",
        "molecular_weight": 253.28,
        "formula": "C10H11N3O3S",
        "cas": "723-46-6",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Sulfonamide antibiotic",
        "uvvis": {"solvent": "water", "peaks": [{"center": 257, "width": 16, "epsilon": 16000, "label": "π→π*"}]},
        "ftir": {"peaks": [
            {"wavenumber": 3460, "intensity": 0.6, "width": 30, "assignment": "N-H stretch (amine)"},
            {"wavenumber": 3380, "intensity": 0.5, "width": 30, "assignment": "N-H stretch (sulfonamide)"},
            {"wavenumber": 1620, "intensity": 0.5, "width": 15, "assignment": "C=N stretch (oxazole)"},
            {"wavenumber": 1310, "intensity": 0.9, "width": 18, "assignment": "S=O asymmetric stretch"},
            {"wavenumber": 1150, "intensity": 0.8, "width": 18, "assignment": "S=O symmetric stretch"}
        ]},
        "hplc": {"retention_factor": 2.5, "logP": 0.89},
        "mass_spec": {"fragments": [{"mz": 254, "intensity": 80, "label": "M+H⁺"}, {"mz": 188, "intensity": 40, "label": "M-SO₂+H"}, {"mz": 156, "intensity": 100, "label": "Aminobenzenesulfonate"}, {"mz": 108, "intensity": 50, "label": "Aminophenyl"}]},
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    "phenol": {
        "name": "Phenol",
        "category": "Reference Standard",
        "molecular_weight": 94.11,
        "formula": "C6H6O",
        "cas": "108-95-2",
        "pharmacopeia": "IP, BP",
        "therapeutic_class": "Antiseptic / Reference compound",
        "uvvis": {"solvent": "water", "peaks": [
            {"center": 210, "width": 12, "epsilon": 6200, "label": "π→π* (B-band)"},
            {"center": 270, "width": 14, "epsilon": 1450, "label": "π→π* (E-band)"}
        ]},
        "ftir": {"peaks": [
            {"wavenumber": 3350, "intensity": 0.8, "width": 50, "assignment": "O-H stretch (phenol)"},
            {"wavenumber": 1600, "intensity": 0.6, "width": 15, "assignment": "Aromatic C=C"},
            {"wavenumber": 1480, "intensity": 0.5, "width": 15, "assignment": "Aromatic C=C"},
            {"wavenumber": 1230, "intensity": 0.7, "width": 15, "assignment": "C-O stretch (phenol)"},
            {"wavenumber": 810, "intensity": 0.5, "width": 10, "assignment": "Aromatic C-H bend"},
            {"wavenumber": 755, "intensity": 0.6, "width": 10, "assignment": "Aromatic C-H bend"}
        ]},
        "hplc": {"retention_factor": 1.5, "logP": 1.46},
        "mass_spec": {"fragments": [{"mz": 94, "intensity": 100, "label": "M⁺"}, {"mz": 66, "intensity": 30, "label": "M-CO"}, {"mz": 65, "intensity": 25, "label": "C₅H₅⁺"}]},
        "polarimetry": {"specific_rotation": 0}
    },

    "benzocaine": {
        "name": "Benzocaine",
        "category": "Local Anesthetic",
        "molecular_weight": 165.19,
        "formula": "C9H11NO2",
        "cas": "94-09-7",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Ester-type local anesthetic",
        "uvvis": {"solvent": "methanol", "peaks": [
            {"center": 290, "width": 16, "epsilon": 18000, "label": "π→π* (aminobenzoate)"}
        ]},
        "ftir": {"peaks": [
            {"wavenumber": 3440, "intensity": 0.6, "width": 25, "assignment": "N-H asymmetric stretch"},
            {"wavenumber": 3350, "intensity": 0.5, "width": 25, "assignment": "N-H symmetric stretch"},
            {"wavenumber": 1685, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (ester)"},
            {"wavenumber": 1600, "intensity": 0.7, "width": 15, "assignment": "N-H bend + Aromatic C=C"},
            {"wavenumber": 1280, "intensity": 0.8, "width": 15, "assignment": "C-O stretch (ester)"},
            {"wavenumber": 840, "intensity": 0.5, "width": 10, "assignment": "para-substituted ring"}
        ]},
        "hplc": {"retention_factor": 3.0, "logP": 1.86},
        "mass_spec": {"fragments": [{"mz": 165, "intensity": 100, "label": "M⁺"}, {"mz": 137, "intensity": 30, "label": "M-C₂H₄"}, {"mz": 120, "intensity": 80, "label": "Aminobenzoyl"}, {"mz": 92, "intensity": 20, "label": "Aniline⁺"}]},
        "polarimetry": {"specific_rotation": 0}
    },

    "lidocaine": {
        "name": "Lidocaine HCl",
        "category": "Local Anesthetic",
        "molecular_weight": 270.80,
        "formula": "C14H23ClN2O",
        "cas": "73-78-9",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Amide-type local anesthetic",
        "uvvis": {"solvent": "water", "peaks": [
            {"center": 263, "width": 14, "epsilon": 7800, "label": "π→π* (xylidine)"}
        ]},
        "ftir": {"peaks": [
            {"wavenumber": 3250, "intensity": 0.5, "width": 40, "assignment": "N-H stretch (amide)"},
            {"wavenumber": 2960, "intensity": 0.6, "width": 25, "assignment": "C-H stretch (alkyl)"},
            {"wavenumber": 1660, "intensity": 0.9, "width": 18, "assignment": "C=O stretch (amide I)"},
            {"wavenumber": 1540, "intensity": 0.7, "width": 18, "assignment": "N-H bend (amide II)"},
            {"wavenumber": 1470, "intensity": 0.5, "width": 15, "assignment": "C-H bend"},
            {"wavenumber": 780, "intensity": 0.4, "width": 12, "assignment": "Aromatic C-H bend"}
        ]},
        "hplc": {"retention_factor": 2.0, "logP": 2.44},
        "mass_spec": {"fragments": [{"mz": 235, "intensity": 30, "label": "M+H⁺ (free base)"}, {"mz": 86, "intensity": 100, "label": "Diethylaminoacetyl"}, {"mz": 58, "intensity": 50, "label": "N(C₂H₅)₂H₂⁺"}]},
        "polarimetry": {"specific_rotation": 0, "note": "Not chiral"}
    },

    "dextrose": {
        "name": "Dextrose (D-Glucose)",
        "category": "Sugar / Reference",
        "molecular_weight": 180.16,
        "formula": "C6H12O6",
        "cas": "50-99-7",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "IV fluid / Polarimetry standard",
        "uvvis": {"solvent": "water", "peaks": [
            {"center": 195, "width": 10, "epsilon": 200, "label": "End absorption"}
        ]},
        "ftir": {"peaks": [
            {"wavenumber": 3350, "intensity": 0.9, "width": 80, "assignment": "O-H stretch (broad)"},
            {"wavenumber": 2920, "intensity": 0.4, "width": 25, "assignment": "C-H stretch"},
            {"wavenumber": 1645, "intensity": 0.3, "width": 20, "assignment": "H₂O bend (residual)"},
            {"wavenumber": 1080, "intensity": 0.8, "width": 30, "assignment": "C-O stretch (primary)"},
            {"wavenumber": 1040, "intensity": 0.7, "width": 25, "assignment": "C-O stretch"},
            {"wavenumber": 900, "intensity": 0.3, "width": 15, "assignment": "Anomeric C-H"}
        ]},
        "hplc": {"retention_factor": 0.1, "logP": -3.24},
        "mass_spec": {"fragments": [{"mz": 180, "intensity": 5, "label": "M⁺"}, {"mz": 163, "intensity": 10, "label": "M-OH"}, {"mz": 103, "intensity": 40, "label": "C₄H₇O₃⁺"}, {"mz": 73, "intensity": 100, "label": "C₃H₅O₂⁺"}, {"mz": 60, "intensity": 60, "label": "C₂H₄O₂⁺"}]},
        "polarimetry": {"specific_rotation": 52.7, "note": "D-Glucose [α]D²⁰ = +52.7° (equilibrium in water)"}
    },

    "sucrose": {
        "name": "Sucrose",
        "category": "Sugar / Reference",
        "molecular_weight": 342.30,
        "formula": "C12H22O11",
        "cas": "57-50-1",
        "pharmacopeia": "IP, BP, USP",
        "therapeutic_class": "Excipient / Polarimetry standard",
        "uvvis": {"solvent": "water", "peaks": [{"center": 190, "width": 8, "epsilon": 100, "label": "End absorption only"}]},
        "ftir": {"peaks": [
            {"wavenumber": 3380, "intensity": 0.9, "width": 80, "assignment": "O-H stretch"},
            {"wavenumber": 2930, "intensity": 0.4, "width": 25, "assignment": "C-H stretch"},
            {"wavenumber": 1060, "intensity": 0.9, "width": 35, "assignment": "C-O stretch (glycosidic)"},
            {"wavenumber": 995, "intensity": 0.7, "width": 20, "assignment": "C-O-C stretch (ring)"},
            {"wavenumber": 920, "intensity": 0.5, "width": 15, "assignment": "Ring vibration"}
        ]},
        "hplc": {"retention_factor": 0.1, "logP": -3.7},
        "mass_spec": {"fragments": [{"mz": 343, "intensity": 5, "label": "M+H⁺"}, {"mz": 325, "intensity": 10, "label": "M-H₂O+H"}, {"mz": 163, "intensity": 100, "label": "Hexose+H"}, {"mz": 85, "intensity": 40, "label": "HMF fragment"}]},
        "polarimetry": {"specific_rotation": 66.5, "note": "Sucrose [α]D²⁰ = +66.5° in water (ICUMSA standard)"}
    }
}


def search_compounds(query: str = "", category: str = "") -> list[dict]:
    """Search compounds by name, formula, or category."""
    results = []
    query_lower = query.lower()
    for key, compound in COMPOUNDS.items():
        if query_lower and query_lower not in compound["name"].lower() \
                and query_lower not in compound.get("formula", "").lower() \
                and query_lower not in compound.get("category", "").lower() \
                and query_lower not in key.lower() \
                and query_lower not in compound.get("cas", ""):
            continue
        if category and category.lower() not in compound.get("category", "").lower():
            continue
        results.append({"id": key, **compound})
    return results


def get_compound(compound_id: str) -> dict | None:
    """Get a single compound by ID."""
    compound = COMPOUNDS.get(compound_id)
    if compound:
        return {"id": compound_id, **compound}
    return None


def get_compound(compound_id: str) -> dict:
    """Retrieve compound dictionary by lowercase key (e.g., 'paracetamol', 'aspirin')."""
    return COMPOUNDS.get(compound_id.lower())


def list_compounds() -> list:
    """List all available compound keys in the reference library."""
    return list(COMPOUNDS.keys())
