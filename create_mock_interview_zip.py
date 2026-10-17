"""
HireX — AI Mock Interview Simulator Packager
Packages the updated AI Mock Interview Simulator (setup, real-time voice interview room,
color-graded audit report, historical tracking, and backend services) into a drop-in ZIP archive.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ZIP_OUTPUT = os.path.join(BASE_DIR, "HireX_AI_Mock_Interview_Module.zip")
STAGING_DIR = os.path.join(BASE_DIR, "_staging_interview_module")

# Clean staging dir if exists
if os.path.exists(STAGING_DIR):
    shutil.rmtree(STAGING_DIR)
os.makedirs(STAGING_DIR, exist_ok=True)

# 1. Define files to copy
files_to_copy = [
    # Server Backend
    ("server/app/routes/interview.py", "server/app/routes/interview.py"),
    ("server/app/services/interview_service.py", "server/app/services/interview_service.py"),
    ("server/tests/test_interview_system.py", "server/tests/test_interview_system.py"),
    
    # Client View & Components
    ("client/src/views/InterviewSimulatorView.tsx", "client/src/views/InterviewSimulatorView.tsx"),
    ("client/src/components/interview/InterviewSetupCard.tsx", "client/src/components/interview/InterviewSetupCard.tsx"),
    ("client/src/components/interview/InterviewRoomView.tsx", "client/src/components/interview/InterviewRoomView.tsx"),
    ("client/src/components/interview/InterviewResultDashboard.tsx", "client/src/components/interview/InterviewResultDashboard.tsx"),
    ("client/src/components/interview/InterviewHistoryList.tsx", "client/src/components/interview/InterviewHistoryList.tsx"),
    
    # Client Types
    ("client/src/types/interview.ts", "client/src/types/interview.ts"),
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
HireX AI Mock Interview Simulator Intelligent Drop-in Installer.
Installs and integrates the AI Mock Interview Simulator into any target HireX installation:
- Automatically detects project root directory.
- Copies all backend services, routes, test suites, and frontend components.
- Integrates the router in server/app/main.py if not already present.
- Executes the test suite to verify 100% test integrity.
"""

import os
import sys
import shutil
import subprocess
import re

def log(msg):
    print(f"[HireX Interview Installer] {msg}")

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
            if f in ["apply_interview_patch.py", "README_AI_MOCK_INTERVIEW.md"]:
                continue
            src_full = os.path.join(root, f)
            rel = os.path.relpath(src_full, source_dir)
            dst_full = os.path.join(root_dir, rel)
            os.makedirs(os.path.dirname(dst_full), exist_ok=True)
            shutil.copy2(src_full, dst_full)
            log(f"Installed: {rel}")

    # 2. Patch server/app/main.py if router not included
    main_py = os.path.join(root_dir, "server", "app", "main.py")
    if os.path.exists(main_py):
        with open(main_py, "r", encoding="utf-8") as f:
            content = f.read()
        if "interview" not in content:
            if "from app.routes import" in content:
                content = re.sub(r"from app\\.routes import ([^\\n]+)", r"from app.routes import \\1, interview", content, count=1)
            if "app.include_router(interview.router)" not in content:
                content = content.replace("app.include_router(", "app.include_router(interview.router)\\napp.include_router(", 1)
            with open(main_py, "w", encoding="utf-8") as f:
                f.write(content)
            log("Patched server/app/main.py with interview.router")
        else:
            log("server/app/main.py already configured with interview router.")

    # 3. Run validation tests
    log("Running automated validation test suite...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(root_dir, "server")
    try:
        res = subprocess.run(
            [sys.executable, "-m", "unittest", "tests/test_interview_system.py"],
            cwd=os.path.join(root_dir, "server"),
            env=env,
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            log("SUCCESS! All Interview System test cases PASSED!")
        else:
            log(f"Unittest output:\\n{res.stdout}\\n{res.stderr}")
    except Exception as e:
        log(f"Note: Could not automatically invoke unittest: {e}")

    log("AI Mock Interview Simulator installation complete!")

if __name__ == "__main__":
    main()
'''

with open(os.path.join(STAGING_DIR, "apply_interview_patch.py"), "w", encoding="utf-8") as f:
    f.write(installer_script)

# 3. Comprehensive README
readme_content = '''# 🎙️ HireX: AI Mock Interview Simulator Subsystem

The **AI Mock Interview Simulator** is a full-lifecycle corporate interview simulator integrated into the institutional AICTE portal, replicating real-world technical and HR rounds with adaptive questioning, speech input/output, and audit reports.

---

## 🌟 Key Features

### 1. Multi-Dimensional Interview Setup (`InterviewSetupCard.tsx`)
- **Configurable Roles**: Software Developer, Frontend, Backend, Full Stack, Data Analyst / Scientist, DevOps, Mobile Engineer.
- **Interview Rounds**: HR & Behavioral, Technical Fundamentals, DSA & Problem Solving, System Design & Architecture, Project & Resume Discussion.
- **Difficulty & Duration**: Beginner, Intermediate, Advanced | 10, 15, or 30 minutes.
- **Target Company Alignment**: Barclays, Google, Amazon, Microsoft, TCS, Infosys, etc.
- **Context Injection**: Optional Job Description (JD) text and Resume snippets for hyper-personalized questions.

### 2. Conversational Interview Room (`InterviewRoomView.tsx`)
- **Speech Recognition (Voice Input)**: Web Speech API microphone integration with real-time speech-to-text.
- **Speech Synthesis (Voice Output)**: Natural voice text-to-speech reading interviewer questions aloud.
- **Adaptive Follow-up Questions**: Dynamically evaluates the candidate's response and generates context-aware follow-up challenges.
- **Live Interview Timer**: Auto-submits upon time expiry with countdown HUD.
- **Previous Evaluation Peek**: Instant micro-feedback with keywords detected, technical accuracy, and improvement hints.

### 3. Institutional Performance Report (`InterviewResultDashboard.tsx`)
- **Harmonized UI Color Grading**: High-contrast, theme-consistent color styling (Emerald ready, Blue proficient, Amber borderline, Rose needs work).
- **Competency Scorecard**: Technical Accuracy, Communication Clarity, Problem Solving, and Topic Relevance (0-10 scale).
- **Personalized Growth Plan**: Tailored recommended actions, documentation references, and practice areas.
- **Question-by-Question Deep Dive**: Detailed breakdown with candidate response, ideal sample answer, and evaluator feedback.

### 4. Historical Tracking (`InterviewHistoryList.tsx` & `canonical_store.json`)
- Per-student historical session archive with past scores, completion dates, and retake buttons.

---

## 📦 What Is Included

### Backend (`server/`)
- `server/app/routes/interview.py`: REST API endpoints:
  - `GET /api/interview/config`: Provider status and role/round taxonomy.
  - `POST /api/interview/start`: Session initialization with tailored first question.
  - `POST /api/interview/submit-answer`: Evaluates response and generates adaptive next question.
  - `POST /api/interview/complete`: Final report generation with dimension scores and recommendations.
  - `GET /api/interview/history/{student_id}`: Candidate session history retrieval.
- `server/app/services/interview_service.py`: Question generation engine, evaluation heuristics, Gemini/Groq LLM connector with offline knowledge-graph fallback.
- `server/tests/test_interview_system.py`: Automated tests verifying session creation, answer evaluation, score computation, and authorization boundaries.

### Frontend (`client/`)
- `client/src/views/InterviewSimulatorView.tsx`: Main view with mode switching (SETUP, ROOM, REPORT, HISTORY).
- `client/src/components/interview/InterviewSetupCard.tsx`: Configuration screen with role cards and JD upload.
- `client/src/components/interview/InterviewRoomView.tsx`: Audio-enabled interview interface with speech input and timer.
- `client/src/components/interview/InterviewResultDashboard.tsx`: Color-graded comprehensive evaluation report.
- `client/src/components/interview/InterviewHistoryList.tsx`: Historical session cards with score badges.
- `client/src/types/interview.ts`: TypeScript interfaces for configs, questions, evaluations, and reports.

---

## 🚀 Quick Installation
1. Extract `ai_mock_interview.zip` into your project root.
2. Run the automated installer:
   ```bash
   python apply_interview_patch.py
   ```
3. Run the automated test suite:
   ```bash
   python -m unittest server/tests/test_interview_system.py
   ```
'''

with open(os.path.join(STAGING_DIR, "README_AI_MOCK_INTERVIEW.md"), "w", encoding="utf-8") as f:
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

print(f"[SUCCESS] Packaged AI Mock Interview Module Zip: {ZIP_OUTPUT}")
print(f"File size: {os.path.getsize(ZIP_OUTPUT):,} bytes")

# Also copy to parent directories for convenient access
copy_destinations = [
    os.path.join(os.path.dirname(BASE_DIR), "ai_mock_interview.zip"),
    os.path.join(BASE_DIR, "ai_mock_interview.zip"),
    os.path.join(BASE_DIR, "mock_interview.zip")
]

for dst in copy_destinations:
    try:
        shutil.copy2(ZIP_OUTPUT, dst)
        print(f"[SUCCESS] Copied to: {dst}")
    except Exception as e:
        print(f"[WARN] Could not copy to {dst}: {e}")
