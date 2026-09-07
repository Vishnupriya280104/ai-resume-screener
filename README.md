# Multi-Format AI Resume Screening & Ranking Engine

A reliable, production-ready backend engine built to parse, filter, enrich, and rank bulk candidate resume pools. This application processes mixed document sets (.pdf, .docx, and .txt) concurrently, filters out out-of-scope applicant records deterministically, scores passing candidates based on strict analytical rubrics using Gemini 3.6-Flash, and merges open-source telemetry profiles utilizing the public GitHub REST API.

---

##  System Architecture & Innovations

### 1. Hybrid Token-Saving Filtration Design
The system uses a fast, deterministic pre-filtering keyword parsing layer before initiating AI processing cycles. If a resume completely lacks mandatory baseline technical traits (e.g., Python and AI framework footprints), it is rejected instantly. This completely eliminates unnecessary LLM API token overhead and pricing billing loops for mismatched candidates.

### 2. Guardrails Over Optimization & "The Trap Case" Stability
The strict rule-based screening engine is built specifically to address nuanced developer profiles. A candidate is **never** rejected simply because alternative ecosystems (*Java, React, Next.js, or Spring Boot*) are on the resume. As long as the primary *Python + AI* baseline exposure threshold criteria are checked off, full-stack hybrid profiles pass safely to scoring, avoiding common algorithmic keyword bias mistakes.

### 3. Structural Contracts and Data Consistency
The pipeline uses **Pydantic Data Schemas** to enforce structured layout constraints at the LLM interface tier. By locking down Google Gemini's response formatting via a strict JSON output configuration schema, the application prevents common parsing failures or string formatting inconsistencies, ensuring clean downstream array sorting.

### 4. Bounded Failure Resilience (Defensive Design)
The batch processing framework is designed defensively. If a file is corrupted, malformed, or unreadable, or if the public GitHub connection encounters an external API rate limit network error (`retry_delay` cycles), **the system never crashes or halts**. The application catches the exception gracefully, registers a warning to the logs, falls back to structural template data maps, and pushes forward to parse the remaining files in the queue.

---

##  Workspace Quick Start

### 1. Initialize and Activate Environment
Ensure your local Python runtime is isolated and installation tracking variables are loaded:
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variable Keys
Create a `.env` configuration file directly in the main root directory and paste your API key parameters:
```env
GEMINI_API_KEY=your_actual_free_google_ai_studio_api_key_here
```
*(A safe, generic reference layout is available for review in `.env.example`)*

---

##  Running the Interfaces

### Interface A: The System Command Line (CLI App)
To execute the complete processing pipeline across your batch document folders directly via your terminal prompt workspace, run:
```cmd
set PYTHONPATH=.&& python main.py --input ./resumes --output ./output/results.json
```

### Interface B: The Asynchronous Web Controller (FastAPI Server)
To fire up the live development backend web server routing panel node, run:
```cmd
set PYTHONPATH=.&& uvicorn src.api.app:app --reload
```
Open **`http://127.0.0`** inside any browser window to access the automated interactive Swagger UI controls.
- `POST /screen`: Initiates batch file extraction as non-blocking background workers (`BackgroundTasks`).
- `GET /results`: Queries the disk storage array cache to pull structural shortlist ranking analytics.

### Generating the Compact Read-Only Summary Report
To parse the processed JSON logs dataset into a minimalist, read-only static HTML overview data table as a bonus reporting artifact, run:
```cmd
python src/pipeline/reporter.py
```
*Outputs a clean evaluation dashboard table matrix at `./output/report.html`*

---

##  Operational Testing
Validate your primary eligibility constraint filter logic paths across passing, failing, and full-stack hybrid edge-cases by firing up your testing framework:
```cmd
pytest
```

---

##  Future System Roadmap (If I Had More Time...)
1. **Asynchronous I/O Network Parallelism:** Transition the parsing loops into concurrent `asyncio.TaskGroup` architectures bounded by a strict `asyncio.Semaphore(limit=5)` throttle to maximize file throughput while preventing rate-limiting blocks.
2. **Persistent Enterprise Storage layers:** Replace local file caching parameters (`results.json`) with an integrated relational database framework like PostgreSQL or a key-value memory cache like Redis.
3. **Advanced Text Sanitization Trimming:** Inject structural token stripping logic to remove generic boilerplate sentences from the raw extracted resume strings prior to running the AI model to save further on input costs.
