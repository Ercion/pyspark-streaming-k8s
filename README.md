# PySpark Streaming on Kubernetes

This project demonstrates how to run a PySpark streaming application on a Kubernetes cluster using Minikube. The application reads a dataset (in Parquet format) from a mounted directory, processes the data using PySpark, and outputs the results to the console in a streaming fashion.

# Project Structure
```bash
pyspark-streaming-k8s/
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── spark-ui-service.yaml
├── Dockerfile
├── streaming_app.py
└── data/
    └── yellow_tripdata_2025-01.parquet
```


Dockerfile: The Dockerfile for building the PySpark streaming application image.

streaming_app.py: The PySpark streaming application code.

data/: Contains the dataset (in Parquet format) that will be processed by the PySpark application.

k8s/: Kubernetes configuration files for namespace, deployment, and Spark UI service.

## Prerequisites

Minikube: A local Kubernetes cluster.

kubectl: Command line tool to interact with Kubernetes.

Docker: To build and manage Docker images.

# Setup Instructions
## Step 1: Clean Up Existing Resources (Optional but Recommended)

If you're encountering issues or just want to start fresh, you can clean up the existing resources:

Delete all Kubernetes resources:
```bash
kubectl delete -f k8s/
```

Delete the Spark Streaming Namespace (if it wasn't automatically deleted):
```bash
kubectl delete namespace spark-streaming
```

Delete the Minikube Cluster (optional):
```bash
minikube stop
minikube delete
```

Note: If it's your first time setting up, start from Step 2 after cleaning up resources.

## Step 2: Start Minikube

Start your Minikube cluster using the following command:

minikube start

## Step 3: Set Docker Environment to Minikube

Set up Docker to use Minikube's Docker daemon:

eval $(minikube docker-env)

## Step 4: Build Docker Image for PySpark Application

Make sure you're in the root directory of the project. Then, build the Docker image using the following command:

docker build --no-cache -t pyspark-streaming-app:latest .

## Step 5: Deploy the Application on Kubernetes

Apply the necessary Kubernetes configurations:

Create Namespace:

kubectl apply -f k8s/namespace.yaml


Create Deployment:
open a new terminal, run:
minikube mount ./data:/data

after then come back to old terminal and run:
kubectl apply -f k8s/deployment.yaml


Create Spark UI Service (Optional):

kubectl apply -f k8s/spark-ui-service.yaml


Note: Step 5 (Image loading into Minikube) has been removed. It is no longer necessary as the Docker image should be available once you build it and use minikube image load or similar commands if needed.

## Step 6: Check the Status of Pods

Check the status of the deployed pods to ensure everything is running correctly:

kubectl get pods -n spark-streaming


You should see the pod with a status like Running.

## Step 7: Access the Spark UI (Optional)

If you've created the Spark UI service, you can port-forward to view the Spark UI:

kubectl port-forward service/spark-ui-service 4040:4040 -n spark-streaming


Note: If this step doesn’t work, the Spark UI might not be available due to the way the service is configured or other issues with Minikube’s networking setup.

Now, you can access the Spark UI at:

http://localhost:4040

## Step 8: Verify the Streaming Output

To view the output of your streaming application, use:

kubectl logs <pod_name> -n spark-streaming


You should see the results of your PySpark streaming job, such as the counts of PULocationID in the dataset.



Troubleshooting

Permission Issues: If you encounter permission errors (e.g., "Operation not permitted"), you may need to adjust the permissions on the mounted directory inside the Minikube VM:

minikube ssh
sudo chmod -R 777 /data
exit
minikube mount ./data:/data


Image Pull Issues: If the image is not found or not pulled, ensure you've built the image properly and used minikube image load to load it into Minikube's Docker registry:

minikube image load pyspark-streaming-app:latest

Notes

The application reads Parquet files in a stream from the /data directory inside the pod.

The data is grouped by PULocationID and the count is printed to the console.

The deployment is set up with a volume mount (host path) pointing to the /data directory, allowing the application to access the dataset stored on the host machine.

The code does not use checkpoints in this example for simplicity, but this can be added if fault tolerance is needed for long-running jobs.

Clean Up

Once you're done, you can clean up the resources using:

kubectl delete -f k8s/
minikube stop
minikube delete

Useful Kubectl and Minikube Commands

View Pods:

kubectl get pods -n spark-streaming


View Logs:

kubectl logs <pod_name> -n spark-streaming

kubectl logs -l app=pyspark -n spark-streaming 

kubectl logs -l app=pyspark -n spark-streaming --tail=-1


Access Spark UI (if enabled):

kubectl port-forward service/spark-ui-service 4040:4040 -n spark-streaming


Step 4: Start Over After Clean-Up

Now that we've cleaned up, you can follow the setup instructions from scratch as outlined above.

Next Steps:

Delete existing resources using the commands mentioned.

Build and load the image into Minikube's Docker daemon.

Reapply all configurations for the deployment and Spark UI.

Monitor the logs and access the Spark UI to verify the application runs correctly.
