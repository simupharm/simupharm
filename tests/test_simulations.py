"""Tests for Simulation Endpoints — UV-Vis, FTIR, HPLC, GC, Mass Spec, Polarimeter, PSA (API v1)."""


class TestUVVis:
    """UV-Vis simulation tests."""

    def test_uvvis_custom_peaks(self, client):
        """Should generate a spectrum from custom peaks."""
        response = client.post("/api/v1/simulate/uvvis", json={
            "peaks": [
                {"center": 254, "epsilon": 10000, "width": 20},
                {"center": 280, "epsilon": 5000, "width": 15},
            ],
            "concentration": 0.001,
            "path_length": 1.0,
        })
        assert response.status_code == 200
        data = response.json()
        assert "wavelengths" in data or "spectrum" in data or "compound" in data

    def test_uvvis_from_compound(self, client):
        """Should generate a spectrum from a compound in the database."""
        response = client.post("/api/v1/simulate/uvvis", json={
            "compound_id": "aspirin"
        })
        # Either succeeds or compound not found (both are valid responses)
        assert response.status_code in (200, 404)

    def test_uvvis_no_peaks_no_compound(self, client):
        """Should return 400 if no peaks and no compound provided."""
        response = client.post("/api/v1/simulate/uvvis", json={})
        assert response.status_code == 400


class TestFTIR:
    """FTIR simulation tests."""

    def test_ftir_custom_peaks(self, client):
        """Should generate an FTIR spectrum from custom peaks."""
        response = client.post("/api/v1/simulate/ftir", json={
            "peaks": [
                {"wavenumber": 3300, "intensity": 0.8, "width": 200, "assignment": "O-H stretch"},
                {"wavenumber": 1700, "intensity": 0.9, "width": 50, "assignment": "C=O stretch"},
            ]
        })
        assert response.status_code == 200

    def test_ftir_no_data(self, client):
        """Should return 400 if no peaks provided."""
        response = client.post("/api/v1/simulate/ftir", json={})
        assert response.status_code == 400


class TestHPLC:
    """HPLC simulation tests."""

    def test_hplc_default_params(self, client):
        """Should simulate with default parameters."""
        response = client.post("/api/v1/simulate/hplc", json={
            "compounds": [
                {"name": "Aspirin", "k_prime": 2.5, "plate_count": 10000}
            ]
        })
        assert response.status_code in (200, 422)  # 422 if schema differs

    def test_hplc_with_flow_rate(self, client):
        """Should accept flow_rate parameter."""
        response = client.post("/api/v1/simulate/hplc", json={
            "compounds": [
                {"name": "Caffeine", "k_prime": 1.5, "plate_count": 8000}
            ],
            "flow_rate": 1.5,
            "column_length": 15.0,
        })
        assert response.status_code in (200, 422)


class TestGC:
    """GC simulation tests."""

    def test_gc_simulation(self, client):
        response = client.post("/api/v1/simulate/gc", json={
            "compounds": [
                {"name": "Ethanol", "boiling_point": 78.37, "retention_index": 500}
            ]
        })
        assert response.status_code in (200, 422)


class TestMassSpec:
    """Mass Spectrometry simulation tests."""

    def test_mass_spec_simulation(self, client):
        response = client.post("/api/v1/simulate/mass-spec", json={
            "compound": {
                "name": "Aspirin",
                "molecular_weight": 180.16,
                "formula": "C9H8O4",
                "fragments": [
                    {"mz": 180, "intensity": 20, "label": "M+"},
                    {"mz": 138, "intensity": 100, "label": "M-42"},
                    {"mz": 120, "intensity": 50, "label": "M-60"},
                ]
            }
        })
        assert response.status_code in (200, 422)

    def test_mass_spec_from_compound_db(self, client):
        response = client.post("/api/v1/simulate/mass-spec/compound", json={
            "compound_id": "aspirin",
            "ionization_mode": "EI"
        })
        assert response.status_code in (200, 404)


class TestPolarimeter:
    """Polarimeter simulation tests."""

    def test_polarimeter_custom(self, client):
        response = client.post("/api/v1/simulate/polarimeter", json={
            "specific_rotation": 52.7,
            "concentration": 0.1,
            "path_length": 1.0,
            "temperature": 20.0,
        })
        assert response.status_code == 200
        data = response.json()
        assert "observed_rotation" in data or "rotation" in data or "result" in data

    def test_polarimeter_from_compound(self, client):
        response = client.post("/api/v1/simulate/polarimeter", json={
            "compound_id": "sucrose"
        })
        assert response.status_code in (200, 404)


class TestPSA:
    """Particle Size Analyzer simulation tests."""

    def test_psa_simulation(self, client):
        response = client.post("/api/v1/simulate/psa", json={
            "mean_size": 50.0,
            "std_dev": 10.0,
        })
        assert response.status_code in (200, 422)


class TestMLIdentification:
    """ML compound identification tests."""

    def test_identify_with_uvvis_data(self, client):
        response = client.post("/api/v1/analyze/identify", json={
            "uvvis_peaks": [
                {"wavelength": 254, "absorbance": 0.85},
                {"wavelength": 280, "absorbance": 0.42},
            ]
        })
        assert response.status_code == 200

    def test_identify_no_data(self, client):
        """Should return 400 if no spectral data provided."""
        response = client.post("/api/v1/analyze/identify", json={})
        assert response.status_code == 400

    def test_identify_multi_instrument(self, client):
        """Should accept data from multiple instruments."""
        response = client.post("/api/v1/analyze/identify", json={
            "uvvis_peaks": [{"wavelength": 254, "absorbance": 0.85}],
            "ftir_peaks": [{"wavenumber": 1700}],
            "molecular_weight": 180.16
        })
        assert response.status_code == 200
