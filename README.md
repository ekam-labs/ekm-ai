# EKM AI

EKM AI is a lightweight AI chat platform that allows users to interact with multiple language models through a single interface.

It uses a FastAPI backend to route requests to different AI providers and a Streamlit interface for chatting with the models. The project is designed to stay simple, developer-friendly, and easy to extend.

>**Project Status:** Dev Preview (v0.1)

The project is currently in an early development stage. Expect updates and improvements as development continues.

---

## Resources

Live Application  
just wait a min

Project Walkthrough  
https://youtu.be/9mhf7VWo_8o

---

## Core Features

**Multi-Model Chat**  
Interact with multiple AI models through a single interface.

**No Account Required**  
Start using the platform instantly without registration.

**No Stored Conversations**  
Chats are not persisted, keeping interactions simple and private.

**Minimal Interface**  
Lightweight Streamlit UI focused on clarity and usability.

---

## Project Structure

```
EKM-AI
│
├── backend
│   └── app
│       ├── prompts
│       │   └── identity.py
│       │
│       ├── services
│       │   ├── gemini_service.py
│       │   ├── groq_service.py
│       │   └── router.py
│       │
│       ├── config.py
│       ├── main.py
│       └── schemas.py
│
├── web
│   └── ui.py
│
├── requirements.txt
└── .env
```

---

## Architecture

```
User
  │
  ▼
Streamlit UI
  │
  ▼
FastAPI Backend
  │
  ▼
Router
  │
  ├── Gemini Service
  └── Groq Service
```

The router selects the appropriate provider based on the chosen model.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/ekm-ai.git
cd ekm-ai
```

### Setup backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`

```
GROQ_API=your_key
GOOGLE_API=your_key
MODEL=your_model
```

Run backend

```bash
uvicorn app.main:app --reload
```

---

### Run the web interface

```bash
cd web
pip install -r requirements.txt
streamlit run ui.py
```

---

## API Usage

Endpoint

```
POST /chat
```

Example request

```json
{
  "model": "openai/gpt-oss-120b",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```

---

## Adding New Models

1. Add the model identifier in `config.py`
2. Implement provider logic inside `services`
3. Update the routing logic in `router.py`

---

## Contributing

Contributions are welcome.

If you find the project interesting, explore the codebase and open a pull request.

---

## Community

YouTube  
https://youtube.com/@ekamlabs

Telegram  
https://t.me/ekam_ai

---

## Roadmap

Planned improvements include:

- Android application for mobile access
- UI and usability improvements
- Support for additional model providers
- Improved deployment infrastructure

Running public AI services requires infrastructure resources.  
Community support for hosting or deployment can help the project grow.

---

## Support the Project

If you find this project useful, consider giving the repository a star ⭐.  
It helps the project reach more developers and grow the community.

---

## License

MIT License