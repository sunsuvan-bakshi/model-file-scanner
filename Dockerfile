# Use a minimal, secure Python base image
FROM python:3.10-slim

# Create a non-root user for security best practices
RUN useradd -m scanneruser
USER scanneruser
WORKDIR /home/scanneruser/app

# Copy requirements and install dependencies locally
COPY --chown=scanneruser:scanneruser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code into the container
COPY --chown=scanneruser:scanneruser src/ src/

# Set default entrypoint to run the scanner
ENTRYPOINT ["python", "src/scanner.py"]