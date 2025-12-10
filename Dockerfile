# Use a lightweight Python version
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file
COPY requirements.txt .

# Install dependencies (no cache to keep image small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports for API (8000) and UI (8501)
EXPOSE 8000
EXPOSE 8501

# Create a simplified startup script
# This allows the container to run either the API or the UI based on command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]