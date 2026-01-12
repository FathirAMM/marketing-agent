# Marketing Agent

A multi-agent system designed to streamline marketing activities for Dilmah Tea. This project utilizes specialized AI agents to research brand information, generate social media content, and create marketing visuals, all while staying aligned with the brand's core values and persona.

## 🚀 Overview

The **Marketing Agent** system is built to automate the creation of brand-aligned marketing materials. It leverages a Retrieval-Augmented Generation (RAG) pipeline to ground its output in factual data from Dilmah's annual reports, website, and YouTube content.

### Key Components

- **Multi-Agent Orchestration:** Uses a central coordinator to manage specialized agents.
- **RAG Pipeline:** Extracts and indexes data from various sources (PDFs, Web, Video) into a vector database for factual grounding.
- **Brand Alignment:** Ensures all generated content adheres to a predefined brand persona.
- **Guardrails:** Implements safety and quality checks on agent outputs.

---

## 🤖 Specialized Agents

The system consists of several specialized agents, each with a unique role:

### 1. Marketing Coordinator (`marketing_agent`)
The "brain" of the operation. It receives high-level marketing tasks and orchestrates the other agents to fulfill them. It uses the `content_researcher_agent`, `social_lead_agent`, and `visualist_agent` as tools.

### 2. Content Researcher (`content_researcher_agent`)
Acts as the factual grounding for campaigns. It retrieves specific anecdotes, strategic insights, and factual information from:
- **Internal Knowledge Base:** (Annual Reports, YouTube Transcriptions, Website Content) stored in Qdrant.
- **Web Search:** Uses SerpApi for up-to-date external information.

### 3. Social Lead (`social_lead_agent`)
Generates brand-aligned social media content across various platforms, ensuring consistent messaging by utilizing the retrieved brand persona.

### 4. Visualist (`visualist_agent`)
Responsible for creating and editing brand-aligned marketing visuals. It can generate new images or edit existing ones to fit the campaign's needs.

---

## 🏗️ Project Structure

- `marketing_agent/`: Contains the central coordinator agent and its specific tools.
- `content_researcher_agent/`: Handles data retrieval from the knowledge base and the web.
- `social_lead_agent/`: Focuses on social media content generation.
- `visualist_agent/`: Manages visual content creation and editing.
- `Data-Extraction/`: Scripts and notebooks for extracting data from annual reports (PDF), websites, and YouTube videos.
- `rag-pipeline/`: Implementation of the RAG system, including chunking, embedding, and indexing data into the vector store.
- `guard_rails/`: Implements callbacks and runners to ensure agent outputs meet quality and safety standards.
- `logo/`: Stores brand-related assets like the Dilmah logo.

---

## 🛠️ Technical Stack

- **Framework:** [Google ADK](https://github.com/google/-adk) (Agent Development Kit)
- **Models:** Gemini 3 Flash Preview (via Google GenAI)
- **Vector Database:** [Qdrant](https://qdrant.tech/)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Data Processing:** LangChain, Pandas, yt-dlp, Firecrawl
- **Search API:** SerpApi

---

## ⚙️ Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FathirAMM/marketing-agent.git
   cd marketing-agent
   ```

2. **Install dependencies:**
   This project uses `uv` for dependency management.
   ```bash
   uv sync
   ```
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Copy `.env.sample` to `.env` and fill in the required API keys:
   - `GOOGLE_API_KEY`: For Gemini models.
   - `OPENAI_API_KEY`: For OpenAI embeddings.
   - `QDRANT_URL` & `QDRANT_API_KEY`: For the vector database.
   - `SERP_API_KEY`: For web search capabilities.
   - `FIRECRAWL_API_KEY`: For web crawling (if applicable).

---

## 📈 Usage

The system is designed to be triggered through the `marketing_coordinator`. You can interact with it by providing a marketing goal or task.

Example task:
> "Create a social media campaign for the new Dilmah Green Tea launch, including three Twitter posts and a matching visual, focusing on our sustainability efforts mentioned in the latest annual report."
---

## 🚢 Deployment (Cloud Run)

This project can be deployed to **Google Cloud Run** using the **Google ADK** CLI.
Reference docs: https://google.github.io/adk-docs/deploy/

### Prerequisites

- A Google Cloud project with billing enabled.
- `gcloud` installed and authenticated:
  ```bash
  gcloud auth login
  gcloud config set project $GOOGLE_CLOUD_PROJECT
  ```
- Set the required deployment environment variables:
  - `GOOGLE_CLOUD_PROJECT`
  - `GOOGLE_CLOUD_LOCATION`

### Deploy

Run:

```bash
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=marketing-agent \
  --app_name=marketing-agent \
  --with_ui \
  marketing_agent
```
