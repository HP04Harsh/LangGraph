# LangGraph Learning Projects

Small Python examples for learning LangGraph workflows with Groq-hosted language
models. The examples cover basic graphs, interactive chat, image input, MongoDB
checkpointing, and conditional routing.

## Project metrics

These are counts of the examples and graph structures in this repository, not
performance benchmarks:

| Metric | Value |
| --- | ---: |
| Runnable Python examples | 5 |
| LangGraph node examples | 2, 1, 1, and 3 nodes |
| Models referenced in the examples | 2 |
| Interactive chat history | In-memory, retained for the current process |
| Checkpoint storage example | MongoDB, keyed by a LangGraph thread ID |
| Image-input example | 1 image URL per request |

The graph node counts correspond to `langgraph_chat.py`,
`langgraph_chat_ai.py`, `checkpointing.py`, and `conditional_edge.py`,
respectively. These metrics describe the current examples; latency, token usage,
and response quality have not been benchmarked.

## Examples

| File | What it demonstrates | Run |
| --- | --- | --- |
| `langgraph_chat.py` | A two-node sequential graph with fixed responses | `python .\langgraph_chat.py` |
| `langgraph_chat_ai.py` | An interactive Groq chat with conversation history | `python .\langgraph_chat_ai.py` |
| `chat-multimodal.py` | A Groq request containing text and an image URL | `python .\chat-multimodal.py` |
| `checkpointing.py` | Saving and resuming graph message state with MongoDB | `python .\checkpointing.py` |
| `conditional_edge.py` | Routing from a Qwen node to another model or the end node | `python .\conditional_edge.py` |

In `conditional_edge.py`, the route is selected using the supplied `is_good`
state value. It is currently set to `False`, so the example calls the second
model; the code does not automatically evaluate response quality.

## Requirements

- Python 3.10 or later
- A Groq API key for the model examples
- Docker Desktop (optional, for the MongoDB checkpoint example)

## Setup (Windows PowerShell)

From the project directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

Set the `GROQ_API` environment variable in a local `.env` file:

```text
GROQ_API=your_groq_api_key
```

Keep the real `.env` file private; it is excluded from Git. Do not commit API
keys.

## Run the MongoDB example

Start the local MongoDB service from the project directory:

```powershell
docker compose up -d
python .\checkpointing.py
```

The compose file exposes MongoDB on `localhost:27017` and stores its data in a
Docker volume. Stop the service when finished with `docker compose down`.

The checkpoint example uses the thread ID `harsh`. Calls using that same ID
share checkpointed conversation state. The interactive chat example keeps
history only in memory and starts a fresh conversation when the process exits.

## Notes

- The examples use the model identifiers shown in their source files:
  `qwen/qwen3.8-27b` and `openai/gpt-oss-120b`.
- `chat-multimodal.py` uses a sample public image URL. Replace it with an image
  URL suitable for your own experiment.
- API availability, model identifiers, and provider support can change; consult
  Groq's current documentation if a model request is rejected.
