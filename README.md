
# Prometheus-and-Grfana
The project uses Docker to manage and run a multi-service application that includes a Flask API, MySQL database, MySQL exporter, Prometheus for metrics collection, and Grafana for visualization. Each component is defined and configured in separate files to ensure seamless integration and monitoring.

# Flask API with MySQL, Prometheus, and Grafana

This project sets up a Flask API with a MySQL database, MySQL exporter, Prometheus for metrics collection, and Grafana for visualization, all running in Docker containers.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Step 1: Clone the Repository

```sh
git clone <repository_url>
cd <repository_directory>

```


### Step 2: Build and Run the Containers
Use Docker Compose to build and run the containers.

```sh
docker-compose up --build
```

This command will:

Build the Flask API Docker image
Start all the defined services: MySQL, mysqld-exporter, phpMyAdmin, Prometheus, Grafana, and the Flask API.


### Step 3: Access the Services


#### Once the containers are up and running, you can access the services at the following URLs:

Flask API: http://localhost:5000

phpMyAdmin: http://localhost:8080

Login: Use the credentials defined in docker-compose.yml (root / rootpassword)

Prometheus: http://localhost:9090

Grafana: http://localhost:3000

Login: admin / admin (or the password defined in docker-compose.yml)


### Step 4: Add Prometheus as a Data Source in Grafana

Log in to Grafana.

Go to Configuration (gear icon) > Data Sources.

Click Add data source.

Select Prometheus.

Set the URL to http://prometheus:9090.

Click Save & Test to verify the connection.


### Step 5: Create Dashboards in Grafana


You can create custom dashboards to visualize your metrics. Here are some example queries:


**Flask API Request Duration**
Prometheus Query:

```promql
rate(request_processing_seconds_sum[5m]) / rate(request_processing_seconds_count[5m])
```

**MySQL Database Item Count**
Prometheus Query:

```promql
item_count
```

# Project Structure

**docker-compose.yml**: Defines the Docker services.

**Dockerfile**: Instructions to build the Flask API Docker image.

**my.cnf**: MySQL configuration file.

**prometheus.yml**: Prometheus configuration file for scraping metrics.

**requirements.txt**: Python dependencies for the Flask API.

## Configuration Details

**docker-compose.yml**
Defines all the services (MySQL, mysqld-exporter, phpMyAdmin, Prometheus, Grafana, Flask API) and their configurations.

**Dockerfile**
#Builds the Docker image for the Flask API using Python 3.9, installs dependencies, and sets the entry point to run the Flask application.

**my.cnf**
MySQL configuration file setting basic parameters and SQL modes.

**prometheus.yml**
Prometheus configuration file defining scrape intervals and targets (mysqld-exporter, Flask API).

**requirements.txt**
Lists the Python packages required for the Flask API.


