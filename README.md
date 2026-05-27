# 🧪 A/B Testing Recommendation Platform

[![Canary Deployment](https://github.com/kallurayaankit/model-ab-testing/actions/workflows/canary.yml/badge.svg)](https://github.com/kallurayaankit/model-ab-testing/actions/workflows/canary.yml)

A production‑ready recommendation API that demonstrates **advanced deployment patterns**, **traffic splitting**, a **feature store**, **feedback loop**, and **canary deployment** automation.

---

## 🧠 Architecture Overview

| Component | Technology | Purpose |
|-----------|------------|---------|
| **API Gateway** | FastAPI | Receives user requests, routes traffic between models |
| **A/B Router** | Custom logic (80/20 split) | Sends 80% of traffic to champion, 20% to challenger |
| **Feature Store** | Redis | Serves real‑time user features consistently |
| **Feedback Loop** | SQLite + Prometheus | Logs predictions & clicks, computes CTR per model |
| **Monitoring** | Prometheus + Grafana | Tracks request count, latency, and CTR |
| **Model Registry** | MLflow (local) | Stores and versions champion/challenger models |
| **CI/CD** | GitHub Actions | Builds Docker image, simulates canary rollout |

![Architecture](https://via.placeholder.com/800x400?text=A/B+Testing+Architecture+Diagram)

---

## 🚀 Quick Start (Local)

### Prerequisites
- Docker Desktop
- Python 3.12 (to train the models)

### 1. Clone the repository
```bash
git clone https://github.com/kallurayaankit/model-ab-testing.git
cd model-ab-testing
