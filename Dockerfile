FROM python:3.9-slim

# Instalar dependencias del sistema para Selenium
RUN apt-get update && apt-get install -y \
    chromium-driver \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    && apt-get clean

# Copiar el proyecto
WORKDIR /app
COPY . .

# Instalar requerimientos
RUN pip install -r requirements.txt

# Ejecutar el bot
CMD ["bash", "start.sh"]
