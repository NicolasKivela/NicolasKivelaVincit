FROM python:3.11-slim

WORKDIR /app

# Kopioidaan requirements
COPY requirements.txt .

# Päivitetään pip ja asennetaan riippuvuudet
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopioidaan vasta tässä vaiheessa koodit, jotta muutos koodissa ei riko asennusvälimuistia
COPY main.py .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]