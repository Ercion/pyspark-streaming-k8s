FROM bitnami/spark:latest

# Copy the PySpark streaming app script
COPY streaming_app.py /opt/bitnami/spark/streaming_app.py

# Set the working directory
WORKDIR /opt/bitnami/spark

# Command to run the app
CMD ["python", "streaming_app.py"]
