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

## 🌐 Web3 Compliant Agent

d3b4 is a **Web3 compliant AI agent** that supports decentralized token-based inference — compatible with the venice.ai ecosystem.

### 💎 Supported Tokens

| Token | Description |
|-------|-------------|
| **A0T**  | venice.ai ecosystem utility token for inference and compute credits |
| **Diem** | Stablecoin-backed token for inference payments and agent service transactions |

- Pay for LLM inference using **A0T** or **Diem** tokens
- Compatible with venice.ai decentralized inference marketplace
- Token-gated agent capabilities and compute tiers
- Wallet integration for seamless on-chain inference billing
- Works alongside traditional API key providers (OpenAI, Anthropic, etc.)

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
Agent Zero (frdel/agent-zero)
    └── deby-lite (piknar/deby-lite)  ← full featured
            └── d3b4 (piknar/d3b4)   ← lean & mean
```

## License

Based on [Agent Zero](https://github.com/frdel/agent-zero) by frdel, via [deby-lite](https://github.com/piknar/deby-lite).

---

## 🙏 Credits & Attribution

d3b4 is a fork of **[deby-lite](https://github.com/piknar/deby-lite)**, which is itself a fork and customization of the **[Agent Zero](https://github.com/frdel/agent-zero)** project.

> **All core framework code, architecture, tooling, Web UI, memory systems, and agent infrastructure are the original work of [frdel](https://github.com/frdel) and the Agent Zero contributors.**

| | |
|---|---|
| **Original Project** | [Agent Zero](https://github.com/frdel/agent-zero) |
| **Original Author** | [frdel](https://github.com/frdel) |
| **Original License** | [MIT License](https://github.com/frdel/agent-zero/blob/main/LICENSE) |
| **Original Docs** | [agent-zero.ai](https://agent-zero.ai) |
| **Intermediate Fork** | [deby-lite](https://github.com/piknar/deby-lite) by piknar |

d3b4 builds upon deby-lite and Agent Zero by providing:
- A minimal footprint (~300MB) optimized for **512MB RAM** environments
- Stripped of browser automation, Torch, TTS/STT for lean operation
- Purpose-built for **Render.com free tier** and similar constrained environments
- Web3 token inference compatibility (A0T + Diem) inherited from deby-lite

If you find Agent Zero useful, please ⭐ **star the original repo**: https://github.com/frdel/agent-zero

---

## 👥 Contributors

| Name | GitHub | Email | Role |
|------|--------|-------|------|
| piknar | [@piknar](https://github.com/piknar) | piknar@gmail.com | Creator & Maintainer |

*Want to contribute? Open a pull request or reach out at [piknar@gmail.com](mailto:piknar@gmail.com)*
