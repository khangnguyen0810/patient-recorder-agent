# Virtual Medical Assistant (Patient Recorder Agent)

An automated solution designed for clinicians to streamline patient documentation. This project listens to patient-doctor consultations and automatically generates accurate, summarized medical records in a strict, structured format—saving hours of manual data entry and pushing records directly to your database without human intervention.

## Key Features

- **Flexible Multimodal Ingestion:** Accepts a wide range of audio and video formats.
- **Guaranteed Schema Enforcement:** Leverages Gemini's **Structured Outputs** feature. The Data Transfer Object (DTO) schema is defined cleanly via deterministic code, strictly preventing the AI from changing the output layout.
- **System-Agnostic & Future-Proof:** Built with decoupling in mind. You can seamlessly scale, adapt, or migrate to alternative systems simply by updating the DTO schema and system prompt.

## Demo

### Raw Structured Output (JSON)

![Structured JSON Payload](assets/demo_json.svg)
_This demonstration uses an audio sample generated via **Gemini 3.1 Flash TTS**. The image above displays the guaranteed, structured medical summary output by the AI Agent after parsing the patient interaction._

### UI Component Representation (Table)

![Tabular Dashboard Visualization](assets/demo_visual.svg)
_The parsed JSON data rendered into a clean, tabular layout, showcasing how the deterministic payload seamlessly maps to a clinician dashboard or Electronic Health Record (EHR) system._

## Installation

### 1. Clone the Repository

```bash
git clone [https://gitsdc.tma.com.vn/mcare/t-va.git](https://gitsdc.tma.com.vn/mcare/t-va.git)
cd patient-recorder-agent

```

### 2. Set Up a Virtual Environment (Recommended)

Isolating your project dependencies ensures your global environment remains clean.

- **macOS / Linux:**

```bash
  python3 -m venv .venv
  source .venv/bin/activate

```

- **Windows (Command Prompt):**

```cmd
  python -m venv .venv
  .venv\Scripts\activate

```

- **Windows (PowerShell):**

```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## Configuration & Usage

### 1. Environment Variables

Create a `.env` file in the root directory of your project and add your Gemini API Key:

```env
GEMINI_API_KEY=your_api_key_here

```

_(Note: This agent is optimized to utilize the high-speed **Gemini 2.5 Flash** model)._

### 2. Testing Custom Audio

The repository includes a default test audio file. To test your own files, open `main.py` and modify the input file path line:

```python
audio_input = "your_custom_audio.wav"

```

### 3. Execution

Run the application layout pipeline:

```bash
python main.py

```

> 💡 **Performance Note:** The application runs OpenAI Whisper locally in inference mode to transcribe the initial audio. Depending on your local machine's hardware capabilities, execution might take a moment while Whisper finishes processing. Once the transcription transfers to Gemini, processing and structuring happen almost instantly.

---

## Future Integrations

Because the output layout is strictly formatted as a predictable data payload, you can easily plug the results of this script into an active API endpoint to auto-populate EHR (Electronic Health Record) databases or pipe it directly into front-end visualization dashboards.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
