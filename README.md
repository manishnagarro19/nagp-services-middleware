# Microservices Project with RabbitMQ and gRPC

## Overview

This project demonstrates the implementation of a microservices architecture using RabbitMQ as the message broker and gRPC for communication between services. Microservices architecture promotes the development of small, loosely coupled services that can be developed, deployed, and scaled independently.

## Technologies Used

- [RabbitMQ](https://www.rabbitmq.com/): A message broker that facilitates communication between microservices.
- [gRPC](https://grpc.io/): A high-performance, open-source framework for building remote procedure call (RPC) APIs.

## Pre-commit Hook, Flake8, and Black

To maintain a consistent codebase, please install the pre-commit hook on your local system. This hook integrates Flake8 for style checking and Black for code formatting.

```bash
pre-commit install
```

### Service Communication
Services communicate through RabbitMQ for asynchronous message passing and use gRPC for synchronous communication. Each service is responsible for specific functionalities and communicates with others via defined message queues or gRPC endpoints.

## Running the Project Locally

### To run this project on your local system, follow the steps below:


#### 1. Set Up a Virtual Environment
Create and activate a virtual environment on your local system.


#### 2.  Install Requirements
Ensure you have the required dependencies installed within your virtual environment by executing the following command:
```bash
make install
```

#### 3 Run FastAPI Server
Launch a new terminal and activate the virtual environment and Start the FastAPI server by running the following command:
```bash
python3 product/main.py
```

#### 4. Run gRPC Server
Launch a new terminal and activate the virtual environment and Launch the gRPC server with the following command:
```bash
python3 order/grpc_server.py
```

#### 5. Run Notification1 Service
Launch a new terminal and activate the virtual environment and Run the Notification1 service using the command:
```bash
python3 notification1/consumer.py
```

#### 6. Run Notification2 Service
Launch a new terminal and activate the virtual environment and execute the Notification2 service with the command:
```bash
python3 notification2/consumer.py
```

## Run Rabbit MQ on local system
We've crafted a Dockerfile to facilitate RabbitMQ setup. Execute the following command to run RabbitMQ on your local system.
```bash
make setup-rabbit-mq
```
