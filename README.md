# FastApi-Jwt-Auth

### run this app

- fill env Postgresql config to alembic/env.py and src/core/config.py
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

- Run, It will do migrate migrations then run app

```bash
alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 80
```
