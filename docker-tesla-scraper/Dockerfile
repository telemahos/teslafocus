# Verwenden des AlmaLinux-Images als Basis
FROM almalinux:8

# System-Updates und Abhängigkeiten installieren, inklusive Xvfb und weiterer benötigter Pakete für Playwright
RUN dnf -y install epel-release && \
    dnf -y update && \
    dnf -y install \
    xorg-x11-server-Xvfb \
    python39 \
    python39-pip \
    nss \
    nspr \
    atk \
    at-spi2-atk \
    cups-libs \
    libXcomposite \
    libXdamage \
    libXrandr \
    libgbm \
    pango \
    cairo \
    alsa-lib \
    at-spi2-core

# Setzen Sie das Arbeitsverzeichnis im Container
# WORKDIR /app

# Kopieren Sie die requirements.txt Datei in das Verzeichnis im Container
COPY requirements.txt .

# Installieren Sie die Python-Abhängigkeiten
RUN pip3 install --no-cache-dir -r requirements.txt

# Kopieren Sie das Python-Skript in das Containerverzeichnis
COPY de_tesla_invetory.py .

# Installieren Sie Playwright und die erforderlichen Browser
RUN pip3 install playwright && playwright install

# Setzen Sie den Standardbefehl zum Starten der Anwendung mit xvfb-run
CMD ["xvfb-run", "python3.9", "de_tesla_invetory.py"]

