# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# update pip
RUN pip install --upgrade pip setuptools wheel

# Install Pytorch from the official source
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install any remaining packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available in the cluster
EXPOSE 8000

# Run main.py when the container launches
CMD ["python", "main.py"]