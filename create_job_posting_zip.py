"""
HireX — Job Posting & 6-Stage Application Tracking Packager
Packages the Recruiter Job Opportunity Creation, Student Persistent Application,
and 6-Stage Application Tracking Pipeline (Applied -> Shortlisted -> Assessment ->
Interview -> Selected -> Offer) into a drop-in ZIP archive with automated installer.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ZIP_OUTPUT = os.path.join(BASE_DIR, "HireX_Job_Posting_and_Application_Tracking_Module.zip")
STAGING_DIR = os.path.join(BASE_DIR, "_staging_job_posting_module")

# Clean staging dir if exists
if os.path.exists(STAGING_DIR):
    shutil.rmtree(STAGING_DIR)
os.makedirs(STAGING_DIR, exist_ok=True)

# 1. Define files to copy
files_to_copy = [
    # Server Backend Routes & Persistence
    ("server/app/routes/recruiter.py", "server/app/routes/recruiter.py"),
    ("server/app/routes/student.py", "server/app/routes/student.py"),
    ("server/app/data/canonical_store.json", "server/app/data/canonical_store.json"),
    
    # Client Views & Modals
    ("client/src/views/RecruiterPortalView.tsx", "client/src/views/RecruiterPortalView.tsx"),
    ("client/src/views/OpportunitiesView.tsx", "client/src/views/OpportunitiesView.tsx"),
    ("client/src/components/modals/OpportunityModal.tsx", "client/src/components/modals/OpportunityModal.tsx"),
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
HireX Job Posting & Application Tracking Intelligent Drop-in Installer.
Installs and integrates the complete Recruiter Job Opportunity Creation and
6-Stage Application Tracking Pipeline (Applied, Shortlisted, Assessment, Interview, Selected, Offer).
"""

import os
import sys
import shutil

def log(msg):
    print(f"[HireX Job Posting Installer] {msg}")

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
            if f in ["apply_job_posting_patch.py", "README_JOB_POSTING_AND_TRACKING.md"]:
                continue
            src_full = os.path.join(root, f)
            rel = os.path.relpath(src_full, source_dir)
            dst_full = os.path.join(root_dir, rel)
            os.makedirs(os.path.dirname(dst_full), exist_ok=True)
            shutil.copy2(src_full, dst_full)
            log(f"Installed: {rel}")

    log("Job Posting & 6-Stage Application Tracking installation complete!")

if __name__ == "__main__":
    main()
'''

with open(os.path.join(STAGING_DIR, "apply_job_posting_patch.py"), "w", encoding="utf-8") as f:
    f.write(installer_script)

# 3. Comprehensive README
readme_content = '''# 💼 HireX: Job Opportunity Posting & 6-Stage Application Tracking System

This subsystem establishes a closed-loop connection between corporate recruiters posting verified placement opportunities and students applying and tracking their candidacy across all hiring stages.

---

## 🌟 Key Features

### 1. Recruiter Opportunity Creation (`RecruiterPortalView.tsx` & `server/app/routes/recruiter.py`)
- Corporate recruiters post verified job opportunities (Title, Company, CTC, Location, Domain, Required Skills, Expiration Date).
- Opportunities are immediately persisted into `canonical_store.json` and broadcast to students in real-time.

### 2. Student Persistent Application State (`OpportunitiesView.tsx` & `OpportunityModal.tsx`)
- Students discover opportunities with AI match percentage algorithms.
- **Persistent Applied Lock**: When a student clicks Apply, their application is saved in the database.
  - The button turns permanently to `Applied ✓ • Current Stage: <Stage>`.
  - Re-opening the modal or refreshing the page retains the exact applied state.
  - Zero chance of accidental double-applications or reset back to "Apply".

### 3. Real-Time 6-Stage Application Tracking Pipeline
Students and recruiters can monitor candidate progression across the **6 industry standard hiring stages**:
1. **Applied**: Candidate submitted credentials and match analysis.
2. **Shortlisted**: Recruiter reviewed profile and advanced candidate.
3. **Assessment**: Candidate invited to technical/aptitude proctored test.
4. **Interview**: Candidate scheduled for AI Mock or Corporate Panel interview.
5. **Selected**: Candidate passed all technical and HR rounds.
6. **Offer**: Official offer letter released to candidate.

### 4. Recruiter Fast-Forward Actions (`RecruiterPortalView.tsx`)
- Recruiter pipeline table features:
  - Direct Stage Selector dropdown (`Applied`, `Shortlisted`, `Assessment`, `Interview`, `Selected`, `Offer`, `Rejected`).
  - One-click sequential progression buttons (`Shortlist →`, `Assessment →`, `Interview →`, `Select →`, `Release Offer →`).
  - Stage changes instantly update the student's dashboard in real-time!

---

## 📦 What Is Included

### Backend (`server/`)
- `server/app/routes/recruiter.py`:
  - `POST /api/recruiter/opportunities`: Creates live job posting.
  - `GET /api/recruiter/applications`: Retrieves candidate submissions.
  - `PATCH /api/recruiter/applications/{app_id}/status`: Advances candidate stage.
- `server/app/routes/student.py`:
  - `POST /api/student/apply`: Persists student application.
  - `GET /api/student/applications`: Returns all applications for authenticated candidate.
- `server/app/data/canonical_store.json`: JSON store maintaining relational integrity between opportunities and applications.

### Frontend (`client/`)
- `client/src/views/RecruiterPortalView.tsx`: Full recruiter command center with job posting form and 6-stage candidate tracking table.
- `client/src/views/OpportunitiesView.tsx`: Student opportunity explorer with applied badges, active stage chips, and filtering.
- `client/src/components/modals/OpportunityModal.tsx`: Opportunity details modal with 6-stage visual pipeline tracker.

---

## 🚀 Quick Installation
1. Extract `job_posting_and_application_tracking.zip` into your project root.
2. Run the automated installer:
   ```bash
   python apply_job_posting_patch.py
   ```
'''

with open(os.path.join(STAGING_DIR, "README_JOB_POSTING_AND_TRACKING.md"), "w", encoding="utf-8") as f:
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

print(f"[SUCCESS] Packaged Job Posting Module Zip: {ZIP_OUTPUT}")
print(f"File size: {os.path.getsize(ZIP_OUTPUT):,} bytes")

# Also copy to parent directories for convenient access
copy_destinations = [
    os.path.join(os.path.dirname(BASE_DIR), "job_posting_and_application_tracking.zip"),
    os.path.join(BASE_DIR, "job_posting_and_application_tracking.zip"),
    os.path.join(BASE_DIR, "job_posting.zip")
]

for dst in copy_destinations:
    try:
        shutil.copy2(ZIP_OUTPUT, dst)
        print(f"[SUCCESS] Copied to: {dst}")
    except Exception as e:
        print(f"[WARN] Could not copy to {dst}: {e}")
