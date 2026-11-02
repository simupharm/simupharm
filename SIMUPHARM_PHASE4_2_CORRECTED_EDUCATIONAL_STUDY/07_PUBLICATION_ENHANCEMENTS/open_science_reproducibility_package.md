# Open Science & Reproducibility Package
**Document ID:** P4.2.1-REPRO-PKG-2026-REV2.1 (FINAL PROTOCOL FREEZE)  
**Target:** Open Science Framework (OSF) & Zenodo Deposition Standards  

---

## 1. Independent Repository Partitioning
To guarantee data privacy, code integrity, and transparency, all project materials are partitioned into five isolated compartments:

1. **Frozen Simulator Source Code:** Immutable client-side source code verified by SHA-256 cryptographic hashes.
2. **Educational Study Materials:** Protocol documents, student worksheets, neutral scripts, and rubrics.
3. **Analysis Code Pipeline:** Python statistical scripts licensed under open MIT License.
4. **Participant Data (Post-Collection):** Completely de-identified raw participant CSV data deposited only after study completion.
5. **Demo / Unit-Test Data:** Synthetic test records labeled `DEMO_TEST_ONLY.csv` strictly isolated in `test_data/`.

---

## 2. Cryptographic Hashes of Frozen Scientific Engine Files
The exact SHA-256 cryptographic checksums of the client-side SimuPharm engine are recorded below to prove zero post-hoc modifications:

| Engine Component | Relative File Path | File Size | SHA-256 Cryptographic Checksum |
| :--- | :--- | :---: | :--- |
| **HPLC Simulator Engine** | `hplc_simulator_script.js` | 184,262 B | `2fad9547f9fc7c671176346e78732be30246a515853631dede21ae8f7d3b7167` |
| **Core Interactive Script** | `script.js` | 67,625 B | `9812fea221fee06391a35d2680c28ce375ca62bc26bc265ed07f36d4d96f0600` |
| **Master Index** | `index.html` | 85,537 B | `dfb896b41790efcc365a3721b8ccc7aa8f49861485a74b02538eb38cadbdee36` |
| **Simulator Page** | `hplc_simulator.html` | 93,721 B | `02b2b226bf291c2466c23832382e296523cecc68811afe26ba65822197afd6bb` |

*Verification Determination:* **PASS — ENGINE FROZEN.**
