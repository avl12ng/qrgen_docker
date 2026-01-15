# Use an official and lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies list first to leverage Docker cache
COPY requirements.txt .

# Install required Python libraries
# --no-cache-dir is used to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script into the container
COPY app_qrgen.py .

# Expose the internal port the app runs on
EXPOSE 5050

# Command to run the application
# We use the specific filename you defined
CMD ["python", "app_qrgen.py"]
