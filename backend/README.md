# Backend of The Memory Vault System - Us

## Folder Structure for Backend
```
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── config/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── vault.py
│   │   ├── vault_membership.py
│   │   ├── memory.py
│   │   ├── memory_media.py
│   │   ├── tag.py
│   │   ├── memory_tag.py
│   │   ├── seed.py
│   │   ├── seed_view.py
│   │   ├── journal_entry.py
│   │   ├── thinking_signal.py
│   │   └── monthly_bloom.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── vault.py
│   │   └── token.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── vaults.py
│   │   ├── health.py    # Is for checking connection statuses and others
│   │   └── deps.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── vault_service.py
│   │
│   └── utils/
│       ├── email.py
│       ├── time.py
│       └── ids.py
│
├── migrations/
├── requirements.txt
├── .env
├── alembic.ini
└── README.md

```

Running command, also do it in /backend

```
uvicorn app.main:app --reload
```
