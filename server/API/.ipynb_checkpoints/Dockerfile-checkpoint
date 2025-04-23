# Use base Python image
FROM python:3.10

# Set working directory to /app inside the container
WORKDIR ./

# Copy only the server/API folder into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Render listens on port 10000
EXPOSE 10000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
