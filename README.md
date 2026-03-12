# d3b4

> *Born of deby-lite. Stripped to the bone. Built to run in 512MB.*

**d3b4** is a lean AI agent forked from [deby-lite](https://github.com/piknar/deby-lite), purpose-built for constrained environments like Render.com free tier (512MB RAM).

## What is d3b4?

d3b4 is **Agent Zero** at its core - intelligent, agentic, and API-connected - without the heavy extras.

| Feature | deby-lite | d3b4 |
|---|---|---|
| Chat & Web UI | ✅ | ✅ |
| Venice.ai API | ✅ | ✅ |
| Agent Zero API (Web3) | ✅ | ✅ |
| MCP / A2A Protocol | ✅ | ✅ |
| LiteLLM (all providers) | ✅ | ✅ |
| Memory & Skills | ✅ | ✅ |
| Search & Utilities | ✅ | ✅ |
| Browser (Playwright) | ✅ | ❌ removed |
| Torch / Embeddings | ✅ | ❌ removed |
| TTS / STT | ✅ | ❌ removed |
| **Docker image size** | ~950MB | ~300MB target |
| **Min RAM** | ~512MB+ | ~256MB |

## Quick Start

```bash
docker run -d \
  -p 8080:8080 \
  -e PORT=8080 \
  -v d3b4-data:/d3b4/usr \
  piknar/d3b4:latest
```

Then open: http://localhost:8080

## Deploy on Render.com

1. Create a new **Web Service** on [render.com](https://render.com)
2. Select **Deploy an existing image from a registry**
3. Image: `docker.io/piknar/d3b4:latest`
4. Add env var: `PORT=8080`
5. Select **Free** plan (512MB) ✅

## Configuration

Mount `/d3b4/usr` volume and place your `.env` file there with API keys:

```env
API_KEY_VENICE=your_venice_api_key
API_KEY_OPENAI=your_openai_key
# ... other LiteLLM provider keys
```

## Lineage

```
Agent Zero (frdkpnt/agent-zero)
    └── deby-lite (piknar/deby-lite)  ← full featured
            └── d3b4 (piknar/d3b4)   ← lean & mean
```

## License

MIT - See [LICENSE](LICENSE)
