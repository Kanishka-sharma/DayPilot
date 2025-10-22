# DayPilot — Smart Planner & Personal Memory Assistant
### Intelligent multi-agent assistant for daily planning, reflection, and personalization using LLM orchestration and contextual memory.

---

## Overview

**DayPilot** is an AI-driven personal productivity assistant that integrates **multi-agent systems**, **Retrieval-Augmented Generation (RAG)**, and **long-term memory** to deliver personalized insights and recommendations.

The app combines several intelligent agents — for weather, news, scheduling, recommendations, and reflection — coordinated by a central **orchestrator**. Each interaction adapts to the user’s preferences using vector-based memory and contextual embeddings.

Built with **Python**, **Streamlit**, and **LangChain**, DayPilot demonstrates applied **Agentic AI**, **contextual reasoning**, and **memory-augmented personalization**.

---

## Key Features

- **Multi-Agent Architecture:** Dedicated agents for weather, news, reflection, and planning.  
- **RAG-Enhanced Reasoning:** Retrieves and grounds responses using stored user context (ChromaDB).  
- **Contextual Memory:** Persistent personalization across sessions via vector embeddings.  
- **Streamlit Interface:** Clean, conversational UI for seamless interaction.  
- **Modular Design:** Extensible architecture for adding new agents or tools.

---

## Tech Stack

| Category | Technology |
|-----------|-------------|
| **Language Models** | Gemini / GPT-4 |
| **Frameworks** | LangChain, Streamlit |
| **Vector DB** | ChromaDB |
| **Memory & Orchestration** | Custom Python MemoryManager + Agent Orchestrator |
| **Environment** | Python-dotenv, Pandas, JSON APIs |

---

## Project Structure
DayPilot/
├── ui/app.py # Streamlit UI
├── orchestrator.py # Manages all AI agents
├── agents/ # Independent AI modules
├── memory/memory_manager.py
├── utils/ # API wrappers & prompt templates
├── user_profile.json
└── .env / requirements.txt

## Autonomous Agents
| Agent | Role |
|-------|------|
| **Weather Agent** | Provides contextual weather forecasts & activity recommendations. |
| **News Agent** | Summarizes daily news relevant to user interests. |
| **Calendar Agent** | Plans and structures daily schedules or tasks. |
| **Recommender Agent** | Suggests activities, habits, or content based on user profile. |
| **Reflection Agent** | Analyzes daily progress and provides constructive insights. |

## AI Concepts Demonstrated

| Concept | Demonstration |
|----------|----------------|
| **Agentic AI** | Independent agents collaborate under a reasoning orchestrator. |
| **RAG (Retrieval-Augmented Generation)** | Queries enriched using vector-based memory context. |
| **LLM Reasoning** | Chain-of-thought planning and task decomposition. |
| **Contextual Memory** | Persistent personalization using Chroma vector embeddings. |
| **Tool Use & Orchestration** | Dynamic agent calls for external APIs (weather, news). |
