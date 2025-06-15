FROM python:3.11-slim

WORKDIR /app

# Installeer dependencies
RUN pip install pandas numpy

# Kopieer script
COPY generate_votes.py .

# Maak data directory
RUN mkdir -p /data

CMD ["python", "generate_votes.py"]
