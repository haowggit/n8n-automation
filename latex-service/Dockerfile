# We start from a standard Python image to run our Flask server
FROM python:3.9-slim

# Install necessary system libraries for font management
RUN apt-get update && \
    apt-get install -y --no-install-recommends fontconfig && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install a more robust, but still curated, set of TeX packages
# This includes advanced font utilities via texlive-luatex
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-xetex \
    texlive-luatex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-font-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Rebuild the system's font cache to recognize all available fonts
RUN fc-cache -f -v

# Install Flask for our web service
RUN pip install Flask

# Set up the application directory
WORKDIR /app
COPY server.py .

# Expose the port the server will run on
EXPOSE 5000

# The command to start the server
CMD ["python", "server.py"]