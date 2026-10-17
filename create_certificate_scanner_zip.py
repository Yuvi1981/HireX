"""
HireX — Certificate Scanner & Skill Verification Packager
Packages the Forensic Certificate Scanner, ML Skill Verifier, Verified Skill Passport,
and Proctoring Engine into a self-contained, drop-in ZIP archive with automated installer.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ZIP_OUTPUT = os.path.join(BASE_DIR, "HireX_Certificate_Scanner_Module.zip")
STAGING_DIR = os.path.join(BASE_DIR, "_staging_certificate_scanner_module")

# Clean staging dir if exists
if os.path.exists(STAGING_DIR):
    shutil.rmtree(STAGING_DIR)
os.makedirs(STAGING_DIR, exist_ok=True)

# 1. Define files and directories to copy
files_to_copy = [
    # Server Backend Services & ML
    ("server/app/services/certificate_scanner.py", "server/app/services/certificate_scanner.py"),
    ("server/app/services/skill_ontology.py", "server/app/services/skill_ontology.py"),
    ("server/app/services/jd_skill_analysis.py", "server/app/services/jd_skill_analysis.py"),
    ("server/app/ml/skill_verifier.py", "server/app/ml/skill_verifier.py"),
    ("server/app/ml/skill_extractor.py", "server/app/ml/skill_extractor.py"),
    ("server/app/ml/skill_intelligence.py", "server/app/ml/skill_intelligence.py"),
    ("server/tests/test_certificate_scanner.py", "server/tests/test_certificate_scanner.py"),
    ("server/tests/test_jd_skill_analysis.py", "server/tests/test_jd_skill_analysis.py"),
    
    # Client Views & Components
    ("client/src/views/SkillVerificationView.tsx", "client/src/views/SkillVerificationView.tsx"),
    ("client/src/components/certificates/CertificateScannerWorkspace.tsx", "client/src/components/certificates/CertificateScannerWorkspace.tsx"),
    ("client/src/components/passport/VerifiedSkillPassport.tsx", "client/src/components/passport/VerifiedSkillPassport.tsx"),
    ("client/src/components/modals/CertificateScannerModal.tsx", "client/src/components/modals/CertificateScannerModal.tsx"),
    ("client/src/components/modals/CandidatePassportModal.tsx", "client/src/components/modals/CandidatePassportModal.tsx"),
    ("client/src/components/RoleSpecificSkillAnalysis.tsx", "client/src/components/RoleSpecificSkillAnalysis.tsx"),
    
    # Client Data & Services
    ("client/src/data/skillQuestions.ts", "client/src/data/skillQuestions.ts"),
    ("client/src/services/jdSkillAnalysis.ts", "client/src/services/jdSkillAnalysis.ts"),
    ("client/src/services/faceDetection.ts", "client/src/services/faceDetection.ts"),
]

for src_rel, dst_rel in files_to_copy:
    src_path = os.path.join(BASE_DIR, src_rel)
    dst_path = os.path.join(STAGING_DIR, dst_rel)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
    else:
        print(f"[WARN] File not found: {src_path}")

# 2. Automated Installer Script inside Staging
installer_script = '''#!/usr/bin/env python3
"""
HireX Certificate Scanner & Skill Verification Intelligent Drop-in Installer.
Installs and integrates the Certificate Scanner & Skill Verification module into any target HireX installation:
- Automatically detects project root directory.
- Copies all backend services, ML verifiers, unit test suites, and frontend components.
- Validates the test suite to verify 100% test integrity.
"""

import os
import sys
import shutil
import subprocess

def log(msg):
    print(f"[HireX Certificate Scanner Installer] {msg}")

def find_project_root():
    cwd = os.path.abspath(os.getcwd())
    if os.path.exists(os.path.join(cwd, "server")) and os.path.exists(os.path.join(cwd, "client")):
        return cwd
    script_dir = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(os.path.join(script_dir, "server")) and os.path.exists(os.path.join(script_dir, "client")):
        return script_dir
    parent = os.path.dirname(script_dir)
    if os.path.exists(os.path.join(parent, "server")) and os.path.exists(os.path.join(parent, "client")):
        return parent
    return None

def main():
    root_dir = find_project_root()
    if not root_dir:
        print("[ERROR] Could not locate HireX project root directory (containing 'server' and 'client').")
        sys.exit(1)

    log(f"Target HireX root: {root_dir}")
    source_dir = os.path.abspath(os.path.dirname(__file__))

    # 1. Copy Files
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if f in ["apply_certificate_patch.py", "README_CERTIFICATE_SCANNER.md"]:
                continue
            src_full = os.path.join(root, f)
            rel = os.path.relpath(src_full, source_dir)
            dst_full = os.path.join(root_dir, rel)
            os.makedirs(os.path.dirname(dst_full), exist_ok=True)
            shutil.copy2(src_full, dst_full)
            log(f"Installed: {rel}")

    # 2. Run validation tests
    log("Running automated validation test suite...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(root_dir, "server")
    try:
        res = subprocess.run(
            [sys.executable, "-m", "unittest", "server/tests/test_certificate_scanner.py"],
            cwd=root_dir,
            env=env,
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            log("SUCCESS! Certificate Scanner test cases PASSED!")
        else:
            log(f"Unittest output:\\n{res.stdout}\\n{res.stderr}")
    except Exception as e:
        log(f"Note: Could not automatically invoke unittest: {e}")

    log("Certificate Scanner & Skill Verification installation complete!")

if __name__ == "__main__":
    main()
'''

with open(os.path.join(STAGING_DIR, "apply_certificate_patch.py"), "w", encoding="utf-8") as f:
    f.write(installer_script)

# 3. Comprehensive README
readme_content = '''# 🛡️ HireX: Certificate Scanner & Skill Verification Subsystem

The **Certificate Scanner & Skill Verification Subsystem** is an institutional-grade, AI-powered forensic document auditing and multi-signal competency verification engine.

---

## 🌟 Key Features

### 1. Forensic Certificate Scanner (`CertificateScannerWorkspace.tsx` & `certificate_scanner.py`)
- **Multi-Provider OCR Parsing**:
  - Microsoft Certifications (Azure AI-102, AZ-900, DP-100, SC-900, PL-300).
  - AWS Certifications (Solutions Architect, Developer, Cloud Practitioner).
  - NPTEL / SWAYAM National Certifications with Elite / Gold / Silver badges.
  - Coursera & Stanford/DeepLearning.AI credentials.
- **Cryptographic Fraud Prevention**:
  - **SHA-256 Collision Check**: Detects duplicate certificates uploaded by multiple candidates.
  - **Levenshtein Distance KYC Name Audit**: Catches certificate theft or mismatched names (e.g. certificate belonging to another student).
  - **Expiration & Tamper Auditing**: Flags expired or backdated credentials with security warnings.
- **Academic Credit Mapping (NCrF / AICTE)**:
  - Assigns National Credit Framework (NCrF) academic credits (1 to 4 credits).
  - Computes institutional verified score boosts (+2 to +5 points).
  - Automatically updates student profile skills with "Verified" badge status upon commit.

### 2. Multi-Signal Skill Verification Engine (`skill_verifier.py` & `SkillVerificationView.tsx`)
- **Ridge-Regression Calibration Model**:
  - Combines 4 signals: (1) Proctored Assessment Score, (2) Code Complexity AST, (3) GitHub Proof-of-Work, (4) Academic Benchmarks.
  - Outputs a calibrated 0-100 verified score and badge tier (`Gold - Industry Ready`, `Silver - Proficient`, `Bronze - Competent`).
- **AI Webcam Proctoring**:
  - Built-in TinyFaceDetector deep-learning face-tracking with fallback calibrated CV.
  - Multi-face and no-face detection, audio anomaly monitor, and fullscreen lock.

### 3. Tamper-Evident Verified Skill Passport (`VerifiedSkillPassport.tsx`)
- Digital skill credential passport displaying verified competency badges.
- Career pathway alignment and skill level progression history.
- Shareable institutional verification link with cryptographic signature.

---

## 📦 What Is Included

### Backend (`server/`)
- `server/app/services/certificate_scanner.py`: Forensic parser, OCR anchor extraction, SHA-256 duplicate cache, Levenshtein KYC auditor, NCrF credit assigner.
- `server/app/ml/skill_verifier.py`: Ridge regression calibration model (multi-signal proof-of-work -> verified badge).
- `server/app/ml/skill_extractor.py`: Semantic skill extractor from resumes and documents.
- `server/app/ml/skill_intelligence.py`: Skill embeddings and semantic distance mapping.
- `server/app/services/skill_ontology.py`: Standardized skill taxonomy.
- `server/app/services/jd_skill_analysis.py`: Job description skill parser and alignment.
- `server/tests/test_certificate_scanner.py`: Unit tests for certificate parsing, KYC name mismatch, duplicate SHA-256 detection, and skill assignment.
- `server/tests/test_jd_skill_analysis.py`: Unit tests for JD skill matching.

### Frontend (`client/`)
- `client/src/components/certificates/CertificateScannerWorkspace.tsx`: Complete OCR scanner UI with preset samples, upload drag-and-drop, forensic audit cards, skill badges, and profile commit button.
- `client/src/views/SkillVerificationView.tsx`: Comprehensive proctored assessment and skill verification view.
- `client/src/components/passport/VerifiedSkillPassport.tsx`: Verified Skill Passport UI card with career pathways.
- `client/src/components/modals/CertificateScannerModal.tsx`: Slide-over modal for quick certificate upload.
- `client/src/components/modals/CandidatePassportModal.tsx`: Institutional passport view for recruiters and TPOs.
- `client/src/components/RoleSpecificSkillAnalysis.tsx`: Dynamic competency gap radar.
- `client/src/data/skillQuestions.ts`: Multi-category technical assessment questions.
- `client/src/services/jdSkillAnalysis.ts`: Frontend JD semantic matching bridge.
- `client/src/services/faceDetection.ts`: Dynamic face-api AI detection and proctoring service.

---

## 🚀 Quick Installation
1. Extract `certificate_scanner_and_skill_verification.zip` into your project root.
2. Run the automated installer:
   ```bash
   python apply_certificate_patch.py
   ```
3. Run the automated test suite:
   ```bash
   python -m unittest server/tests/test_certificate_scanner.py
   ```
'''

with open(os.path.join(STAGING_DIR, "README_CERTIFICATE_SCANNER.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

# 4. Create the Zip file
with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(STAGING_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, STAGING_DIR)
            zipf.write(full_path, arcname)

# Clean staging dir
shutil.rmtree(STAGING_DIR)

print(f"[SUCCESS] Packaged Certificate Scanner Module Zip: {ZIP_OUTPUT}")
print(f"File size: {os.path.getsize(ZIP_OUTPUT):,} bytes")

# Also copy to parent directories for convenient access
copy_destinations = [
    os.path.join(os.path.dirname(BASE_DIR), "certificate_scanner_and_skill_verification.zip"),
    os.path.join(BASE_DIR, "certificate_scanner_and_skill_verification.zip"),
    os.path.join(BASE_DIR, "certificate_scanner.zip")
]

for dst in copy_destinations:
    try:
        shutil.copy2(ZIP_OUTPUT, dst)
        print(f"[SUCCESS] Copied to: {dst}")
    except Exception as e:
        print(f"[WARN] Could not copy to {dst}: {e}")
