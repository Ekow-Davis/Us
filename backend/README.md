# Backend of The Memory Vault System - Us

## Folder Structure for Backend
```
backend/
│
├── app/
│   ├── main.py                 # FastAPI entry point
│   │
│   ├── config/                   # Core system config
│   │   ├── config.py           # Env variables, settings
│   │   ├── security.py         # JWT, password hashing
│   │   └── database.py         # DB engine & session
│   │
│   ├── models/                 # SQLAlchemy models
|   |   ├── user.py
|   |   ├── vault.py              
|   |   ├── vault_membership.py   
|   |   ├── memory.py
|   |   ├── memory_media.py       
|   |   ├── tag.py
|   |   ├── memory_tag.py         
|   |   ├── seed.py               
|   |   ├── seed_view.py          
|   |   ├── journal_entry.py      
|   |   ├── thinking_signal.py
|   |   ├── monthly_bloom.py      
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── memory.py
│   │   ├── note.py
│   │   └── auth.py
│   │
│   ├── api/                    # Route definitions
│   │   ├── deps.py             # Shared dependencies
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── memories.py
│   │   ├── notes.py
│   │   ├── signals.py
│   │   └── health.py
│   │
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── memory_service.py
│   │   ├── notification_service.py
│   │   └── media_service.py
│   │
│   ├── utils/                  # Helpers
│   │   ├── email.py
│   │   ├── time.py
│   │   └── ids.py
│   │
│   └── tests/                  # Tests (optional initially)
│       └── test_memories.py
│
├── migrations/                 # Alembic migrations
│
├── requirements.txt
├── main.py
├── .env
├── alembic.ini
└── README.md

```