# 1. Use official Python image
FROM python:3.9-slim

# 2. Set working directory in the container
WORKDIR /app

# 3. Copy everything from current dir to /app in the container
COPY . .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose port 10000 (Render default)
EXPOSE 10000

# 6. Run FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
