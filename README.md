# EpGuides Renamer Service

A FastAPI-powered backend microservice built to interact with the unofficial EpGuides API (`https://epguides.frecar.no/`). This service forms the foundation of an automated media renamer application, allowing users to query, track, and retrieve structured television show and episode data.

Built for maximum performance and minimal footprint utilizing modern tools like **uv** and **FastAPI**.

---

## 🛠️ Tech Stack & Architecture

- **Runtime & Package Manager:** [uv](https://github.com/astral-sh/uv) (Blazing fast Python package resolver and environment manager)
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **HTTP Client:** [HTTPX](https://www.python-httpx.org/) (Synchronous connection pooling with redirection support)
- **Configuration & Validation:** [Pydantic Settings v2](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

### Project Architecture

The project strictly enforces **Separation of Concerns (SoC)** using Object-Oriented Programming (OOP) design patterns:

1. **Configuration Layer (`config.py`):** Universal, type-safe settings validation parsing `.env` sheets globally.
2. **Client Layer (`client.py`):** Domain-specific API wrapper isolating network protocols and data serialization.
3. **Application Layer (`main.py`):** Core framework routing orchestrating endpoints and server-wide lifecycle events.

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have `uv` installed. If you don't have it yet:

```bash
# macOS/Linux
curl -LsSf https://astral-sh/uv/install.sh | sh
```

### 2. Installation & Setup

Clone the repository, shift into the project directory, and initialize your environment:

```bash
# Create an isolated virtual environment using Python 3.12
uv venv --python 3.12

# Activate the virtual environment
source .venv/bin/activate
```

Install the required dependencies directly into the local environment:

```bash
uv pip install fastapi uvicorn httpx pydantic-settings
```

### 3. Environment Configuration

Create a `.env` file at the root of your directory:

```bash
HOST=127.0.0.1
PORT=8000
BASE_API_URL=https://epguides.frecar.no
ALL_SHOWS_ENDPOINT=/shows/
```

_Note: The system resolves absolute root directory mapping, meaning you can boot scripts seamlessly regardless of nested subdirectories._

### 4. Running the Application

Spin up the local development Uvicorn instance through uv:

```bash
uv run python main.py
```

The application will launch on your configured port (e.g., `http://127.0.0.1:8000`). You can explore the interactive OpenAPI system docs at `http://127.0.0.1:8000/docs`.

## 📖 Module API Documentation

All modules strictly conform to Google-style docstring specifications, ensuring seamless integration with type-checkers (`mypy/Pyright`) and automated documentation generators.
