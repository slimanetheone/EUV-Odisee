FROM python:3.11-slim

WORKDIR /app

# Geen Google API dependencies meer nodig!
RUN pip install pandas numpy

COPY final_ranking.py .

CMD ["python", "final_ranking.py"]
