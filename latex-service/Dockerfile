# Wir starten von einem Python-Image, um Flask zu haben
FROM python:3.9-slim

# Installieren von XeTeX (eine relativ schlanke LaTeX-Version)
RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-xetex && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installieren von Flask
RUN pip install Flask

# Setzen des Arbeitsverzeichnisses
WORKDIR /app

# Kopieren unseres Server-Skripts in den Container
COPY server.py .

# Dieser Port wird vom Webserver im Container verwendet
EXPOSE 5000

# Der Befehl, der beim Start des Containers ausgeführt wird
CMD ["python", "/app/server.py"]