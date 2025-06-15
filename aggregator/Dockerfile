FROM bitnami/spark:latest

USER root

WORKDIR /app

# Geen Google API dependencies meer nodig!
COPY aggregate_votes.py .

CMD ["python", "aggregate_votes.py"]

