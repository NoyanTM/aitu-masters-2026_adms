# aitu-masters-2026_adms
Advanced database management systems

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .env
```

```sh
docker compose up -d
alembic revision --autogenerate -m "Migration name"
alembic upgrade head
```

```sh
python3 -m eduhub.scripts.insert_fake_data
python3 -m eduhub.scripts.query_examples
```

```sh
pdflatex --output-directory=build report.tex
biber ./build/report
pdflatex --output-directory=build report.tex
pdflatex --output-directory=build report.tex
```
