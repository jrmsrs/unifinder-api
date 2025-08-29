# unifinder-api

## 1. Create a Virtual Enviroment

**On Linux/macOs**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windowns**

```bash
python3 -m venv venv
.\venv\Scripts\activate
```

## 2.Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run - Dev mode

```bash
fastapi dev app/main.py
```

## 4. Access API
Once the server is running, open your browser:

API Root: http://127.0.0.1:8000

Interactive Docs (Swagger UI): http://127.0.0.1:8000/docs

Alternative Docs (ReDoc): http://127.0.0.1:8000/redoc