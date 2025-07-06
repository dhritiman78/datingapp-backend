# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY ./app ./app

# Expose the port your app runs on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["python", "-m", "app.main"]