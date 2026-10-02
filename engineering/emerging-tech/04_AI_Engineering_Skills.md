# 🤖 AI Engineering & Skills for the AI Era
> **Target Audience:** Mobile Developers transitioning to AI Engineering / Product Engineering.
> **Focus:** RAG, Agents, On-Device LLMs, and Prompt Engineering.

![AI](https://img.shields.io/badge/Tech-AI_Engineering-FFD700?style=for-the-badge&logo=openai&logoColor=black)

---

## 📖 Table of Contents
- [1. The Shift: Mobile Dev to AI Engineer](#1-the-shift-mobile-dev-to-ai-engineer)
- [2. RAG (Retrieval Augmented Generation)](#2-rag-retrieval-augmented-generation)
- [3. Agents & Function Calling](#3-agents--function-calling)
- [4. Vector Databases](#4-vector-databases)
- [5. Prompt Engineering for Developers](#5-prompt-engineering-for-developers)
- [6. Running Local LLMs (Privacy First)](#6-running-local-llms-privacy-first)

---

## 1. The Shift: Mobile Dev to AI Engineer

The "App" is becoming a thin client for Intelligence.
- **Old World**: Strings, JSON, REST APIs, Rigid Logic.
- **New World**: Embeddings, Streams, Semantic Search, Probabilistic Logic.

**Your New Stack:**
*   **Mobile**: User Interface & Context Gathering (Location, Sensors).
*   **Edge AI**: Running logic on-device (CoreML/TFLite) for <100ms latency.
*   **Vector DB**: Long-term memory.
*   **LLM Orchestration**: LangChain, LlamaIndex, or custom Python scripts.

---

## 2. RAG (Retrieval Augmented Generation)

**Problem**: LLMs hallucinate and don't know your private data.
**Solution**: RAG. Feed relevant data into the context window before asking the question.

**Mobile RAG Flow:**
1.  **User Query**: "Where did I park my car?"
2.  **Retrieval**: Search local database (Sqlite/Realm) or Vector DB for "car parking" logs.
3.  **Augmentation**: Construct prompt:
    > "Context: User parked at Lat/Long X,Y at 10:00 AM.
    > Question: Where is my car?"
4.  **Generation**: LLM answers: "You parked at X,Y."

---

## 3. Agents & Function Calling

**Definition**: An Agent is an LLM that can **use tools**.

**Example (OpenAI Function Calling):**
You define a tool in JSON:
```json
{
  "name": "get_weather",
  "parameters": { "location": "string" }
}
```

1.  **User**: "Is it raining in London?"
2.  **LLM**: *stops generating text* -> Calls function `get_weather("London")`.
3.  **App**: Executes API call `weatherapi.com/London`. Returns `{"rain": true}`.
4.  **LLM**: "Yes, it is currently raining in London."

**Mobile Context**: Your app's features (Camera, Contacts, Calendar) are the "Tools". The LLM is the "Brain" deciding which tool to use.

---

## 4. Vector Databases

**Concept**: Storing data by "Meaning" (Semantic), not "Keyword".

*   **Embeddings**: Converting text/images into a list of numbers (Vectors).
    *   "Dog" -> `[0.1, 0.9, ...]`
    *   "Puppy" -> `[0.12, 0.88, ...]` (Close distance)
    *   "Car" -> `[0.9, 0.1, ...]` (Far distance)

**Mobile Options:**
*   **SQLite-vss**: Vector search extension for SQLite.
*   **ObjectBox**: On-device vector search.
*   **Pinecone/Milvus**: Server-side vector search.

---

## 5. Prompt Engineering for Developers

It's not just "asking nicely". It's computer science with natural language.

### A. Chain of Thought (CoT)
Force the model to "think" before answering to reduce errors.
> **Bad**: "Return the fibonacci sequence in Python."
> **Good**: "First, outline the logic for a recursive fibonacci function. Then, verify edge cases like 0 and 1. Finally, write the Python code."

### B. Few-Shot Prompting
Give examples.
> "Convert this JSON to Kotlin Data Class.
> Input: `{"name": "A"}` -> Output: `data class User(val name: String)`
> Input: `{"id": 1}` -> Output: ..."

### C. System Instructions
Set the persona.
> "You are a Senior Android Engineer. You prefer Clean Architecture and strictly avoid deprecated APIs."

---

## 6. Running Local LLMs (Privacy First)

Running models like **Llama 3 (8B)** or **Mistral 7B** directly on the phone.

**Why?**
1.  **Privacy**: Data never leaves the device (Health, Finance).
2.  **Offline**: Works in airplane mode.
3.  **Cost**: No API fees.

**Android Tools:**
*   **MediaPipe LLM Inference**: Google's cross-platform solution.
*   **MLCChat (TVM)**: Open source compiler for on-device ML.
*   **Executorch**: PyTorch for Edge.

**iOS Tools:**
*   **MLX**: Apple's framework for Apple Silicon (mostly Mac, but moving to iOS).
*   **CoreML**: Optimized transformer assets.
