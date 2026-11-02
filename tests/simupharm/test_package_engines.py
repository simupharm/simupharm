"""
SimuPharm Automated Package Test Suite

Tests all 7 analytical simulation engines, the 21-API compound database,
and the multimodal identification chemometrics matcher.
"""
import pytest
import numpy as np
import time

from simupharm import (
    simulate_hplc, HPLCParams, ColumnParams, HPLCCompound, van_deemter,
    simulate_uvvis, UVVisParams, UVVisCompound, UVVisPeak, generate_calibration_curve,
    simulate_ftir, FTIRParams, IRPeak, identify_functional_groups,
    simulate_gc, GCParams, GCCompound, TempRamp,
    simulate_mass_spec, MassSpecParams, MassSpecCompound, MSFragment,
    simulate_polarimeter, PolarimetryParams, PolarimetryCompound,
    simulate_psa, PSAParams,
    COMPOUNDS, get_compound, list_compounds,
    identify_compound, cosine_similarity, peak_position_score
)


class TestHPLC:
    """HPLC kinetics and plate theory verification."""

    def test_van_deemter_calculation(self):
        H = van_deemter(particle_size_um=5.0, flow_rate=1.0)
        assert H > 0.0
        assert isinstance(H, float)

    def test_hplc_binary_separation(self):
        comp1 = HPLCCompound(name="Paracetamol", retention_factor=1.8)
        comp2 = HPLCCompound(name="Caffeine", retention_factor=3.2)
        params = HPLCParams(
            compounds=[comp1, comp2],
            column=ColumnParams(length_cm=15.0, particle_size_um=3.5),
            flow_rate_ml_min=1.0,
            mobile_phase_organic_pct=50.0
        )
        res = simulate_hplc(params)
        assert len(res.peaks) == 2
        assert res.peaks[0].retention_time < res.peaks[1].retention_time
        assert res.peaks[1].resolution > 1.0
        assert "pass" in res.system_suitability

    def test_hplc_execution_speed(self):
        comp1 = HPLCCompound(name="Comp1", retention_factor=2.0)
        params = HPLCParams(compounds=[comp1])
        t0 = time.perf_counter()
        for _ in range(50):
            simulate_hplc(params)
        t_elapsed = (time.perf_counter() - t0) / 50.0
        assert t_elapsed < 0.02  # Less than 20 ms per run


class TestUVVis:
    """UV-Vis electronic absorption and calibration curve verification."""

    def test_uvvis_spectrum_simulation(self):
        peak = UVVisPeak(center=277.0, width=18.0, epsilon=42000.0, label="pi->pi*")
        compound = UVVisCompound(name="Ciprofloxacin", peaks=[peak])
        params = UVVisParams(compound=compound, concentration_molar=1e-5, path_length_cm=1.0)
        res = simulate_uvvis(params)

        assert abs(res.lambda_max - 277.0) <= 2.0
        assert res.max_absorbance > 0.1
        assert len(res.wavelengths) == len(res.absorbance)
        assert len(res.transmittance) == len(res.absorbance)

    def test_beer_lambert_calibration_curve(self):
        concentrations = [1e-5, 2e-5, 4e-5, 6e-5, 8e-5, 1e-4]
        calib = generate_calibration_curve(concentrations, peak_epsilon=25000.0, noise=0.001)

        assert calib.r_squared > 0.99
        assert calib.slope > 0.0
        assert calib.lod > 0.0
        assert calib.loq > calib.lod


class TestFTIR:
    """FTIR interferogram FFT and functional group verification."""

    def test_ftir_fft_and_transmittance(self):
        p1 = IRPeak(wavenumber=1715.0, intensity=0.9, width=25.0, assignment="C=O")
        p2 = IRPeak(wavenumber=2950.0, intensity=0.7, width=40.0, assignment="C-H")
        params = FTIRParams(peaks=[p1, p2])
        res = simulate_ftir(params)

        assert len(res.wavenumbers) > 100
        assert len(res.transmittance) == len(res.wavenumbers)
        # Absorption peaks should have low transmittance
        assert min(res.transmittance) < 50.0

    def test_functional_group_tagging(self):
        groups = identify_functional_groups([1710.0, 3350.0])
        names = [g["functional_group"] for g in groups]
        assert any("carbonyl" in n.lower() for n in names)
        assert any("alcohol" in n.lower() or "amine" in n.lower() for n in names)


class TestGC:
    """Capillary gas chromatography temperature ramp verification."""

    def test_gc_temperature_programming(self):
        c1 = GCCompound(name="Ethanol", boiling_point_c=78.4, retention_index=600.0)
        c2 = GCCompound(name="Toluene", boiling_point_c=110.6, retention_index=800.0)
        params = GCParams(
            compounds=[c1, c2],
            initial_temp_c=40.0,
            ramps=[TempRamp(rate_c_min=15.0, target_temp_c=200.0, hold_time_min=2.0)]
        )
        res = simulate_gc(params)

        assert len(res.peaks) == 2
        assert res.peaks[0].retention_time < res.peaks[1].retention_time
        assert res.peaks[1].resolution > 1.5


class TestMassSpec:
    """Mass spectrometry ionization, fragmentation, and isotope modeling."""

    def test_mass_spec_isotope_and_fragments(self):
        comp = MassSpecCompound(
            name="Paracetamol",
            molecular_weight=151.16,
            formula="C8H9NO2",
            fragments=[
                MSFragment(mz=109.0, intensity=85.0, label="[M-COCH3]+"),
                MSFragment(mz=80.0, intensity=30.0, label="[C5H6N]+")
            ]
        )
        params = MassSpecParams(compound=comp, ionization_mode="EI")
        res = simulate_mass_spec(params)

        assert res.molecular_ion == 151.16
        assert len(res.peaks) >= 4  # Parent isotopes + fragments
        mzs = [p.mz for p in res.peaks]
        assert 151.0 in mzs or 151.2 in mzs or any(abs(m - 151.16) < 0.5 for m in mzs)
        assert any(abs(m - 109.0) < 0.5 for m in mzs)


class TestPolarimeterAndPSA:
    """Polarimetry and particle size analysis verification."""

    def test_polarimetry_rotation(self):
        comp = PolarimetryCompound(name="Dextrose", specific_rotation=+52.7, concentration_g_ml=0.05)
        params = PolarimetryParams(compound=comp, path_length_dm=1.0)
        res = simulate_polarimeter(params)

        assert res.observed_rotation > 0.0
        assert "dextrorotatory" in res.interpretation.lower()

    def test_psa_distribution(self):
        params = PSAParams(d50_um=45.0, geometric_std=1.4)
        res = simulate_psa(params)

        assert res.d10 < res.d50 < res.d90
        assert res.span > 0.0
        assert res.surface_area_m2_g > 0.0


class TestCompoundDatabase:
    """Reference pharmaceutical compound database verification."""

    def test_database_integrity(self):
        assert len(COMPOUNDS) >= 21
        names = list_compounds()
        assert "paracetamol" in names
        assert "aspirin" in names
        assert "ibuprofen" in names
        assert "ciprofloxacin" in names

        para = get_compound("paracetamol")
        assert para["molecular_weight"] == 151.16
        assert "uvvis" in para
        assert "ftir" in para
        assert "hplc" in para


class TestMultimodalMatcher:
    """Chemometrics and multi-instrument unknown identification verification."""

    def test_cosine_similarity(self):
        v1 = np.array([1.0, 2.0, 3.0])
        v2 = np.array([1.0, 2.0, 3.0])
        assert abs(cosine_similarity(v1, v2) - 1.0) < 1e-6

    def test_peak_position_scoring(self):
        query = [254.0, 280.0]
        ref = [253.5, 280.2]
        score = peak_position_score(query, ref, tolerance=1.0)
        assert score == 1.0

    def test_multimodal_compound_identification(self):
        # Multi-instrument query matching Paracetamol (UV + FTIR + MS)
        res = identify_compound(
            uvvis_peaks=[{"wavelength": 243.0, "absorbance": 0.8}, {"wavelength": 290.0, "absorbance": 0.1}],
            ftir_peaks=[{"wavenumber": 1655.0}, {"wavenumber": 3325.0}],
            ms_fragments=[151.0, 109.0, 80.0],
            molecular_weight=151.16
        )
        assert len(res.top_matches) > 0
        top_name = res.top_matches[0].compound_name.lower()
        assert "paracetamol" in top_name or "acetaminophen" in top_name
        assert res.top_matches[0].confidence > 85.0
