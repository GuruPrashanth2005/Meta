FROM python:3.10-slim

# Create a non-root user specifically for Debian-based Hugging Face container constraints
RUN useradd -m -u 1000 astrafluxuser

WORKDIR /app

# Upgrade pip securely without maintaining cache blocks
RUN pip install --no-cache-dir --upgrade pip

COPY . .

# Run the editable install inside strict build dependencies layer avoiding tmp cache
RUN pip install --no-cache-dir -e .

# Clean unneeded apt caches or system files maintaining lean footprint
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Shift permission boundary to the non-root execution shell
RUN chown -R astrafluxuser:astrafluxuser /app
USER astrafluxuser

EXPOSE 7860

CMD ["server"]
