# oulad-data-pipeline
This repository contains the code and configuration files for a data pipeline built using Apache Airflow, Hadoop (HDFS), PySpark, and MySQL. The pipeline processes educational data from the Open University Learning Analytics Dataset (OULAD) and stores aggregated data in a MySQL database for real-time use.
=======
# OULAD Data Pipeline Project

This repository contains the code and configuration files for a data pipeline built using Apache Airflow, Hadoop (HDFS), PySpark, and MySQL. The pipeline processes educational data from the Open University Learning Analytics Dataset (OULAD) and stores aggregated data in a MySQL database for real-time use.

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- **Apache Hadoop (HDFS)**
- **Apache Airflow**
- **Apache Spark (with PySpark)**
- **MySQL Server**
- **Python 3.10.12** (installed within a virtual environment)
- **Pandas, SQLAlchemy, and PyMySQL libraries** (installed within the virtual environment)

## Setup

### 1. Set Up Your Environment

#### Virtual Environment

Create and activate a Python virtual environment to isolate your project dependencies:

```bash
python3 -m venv airflow_env
source airflow_env/bin/activate
```
Install Required Python Libraries inside the virtual environment, 
install the necessary Python libraries:

```
pip install apache-airflow
pip install pandas==1.5.3 SQLAlchemy<1.5 pymysql pyspark
```

### Issues Encountered:
**Python Library Compatibility:** Encountered issues with pandas and SQLAlchemy versions. 
Resolved by reinstalling specific versions (pandas==1.5.3, SQLAlchemy<1.5) to ensure compatibility.

### 2. Hadoop Configuration
Hadoop Installation and Configuration
Install and configure Hadoop (outside the virtual environment). Below are the key configuration files:

- **core-site.xml is included:** Configures fundamental Hadoop settings, including the default filesystem path and I/O operations
- **hdfs-site.xml is included:** Manages settings specific to the Hadoop Distributed File System (HDFS), such as replication factors and Namenode configurations.
- **mapred-site.xml is included:** Configures MapReduce-specific properties, defining how data processing jobs are executed in the Hadoop ecosystem.
- **yarn-site.xml is included:** Controls YARN (Yet Another Resource Negotiator) settings, managing resources across the cluster, including ResourceManager and NodeManager configurations.

#### - SSH Configuration for Hadoop:
During the Hadoop setup, SSH is required for communication between the NameNode and DataNodes. 
This requires passwordless SSH setup.

Generate SSH keys:

```bash
ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
```
Add the SSH key to authorized keys:

```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
Verify SSH setup by running:
```bash
ssh localhost
```
**Issues Encountered:**
SSH Configuration Issue: Initially, Hadoop setup failed due to SSH not being configured properly. This was resolved by setting up passwordless SSH, which is critical for Hadoop’s distributed operations.

Start the Hadoop NameNode and DataNode:
```bash:
start-dfs.sh
```
### Issues Encountered:
**Hadoop Configuration Errors:** Incorrect settings in core-site.xml and hdfs-site.xml caused initial failures. Correcting the configurations resolved these issues.

### 3. MySQL Configuration
Install MySQL server (outside the virtual environment):
```bash:
sudo apt-get install mysql-server
```

Start the MySQL server:
```bash:
sudo systemctl start mysql
```

Create a database and user (inside MySQL):
```sql

CREATE DATABASE oulad_db;
CREATE USER 'tom1989'@'localhost' IDENTIFIED BY 's5426304';
GRANT ALL PRIVILEGES ON oulad_db.* TO 'tom1989'@'localhost';
FLUSH PRIVILEGES;
```
### Issues Encountered:
**MySQL Authentication:** Had to configure MySQL to use password authentication for the root user to create a new user with the necessary privileges.

### 4. Airflow Configuration
Initialize Airflow
Inside the virtual environment, set up Airflow:

```bash
export AIRFLOW_HOME=~/airflow
airflow db init
```

Create an Airflow user:
```bash
airflow users create --username admin --firstname Tom --lastname 1989 --role Admin --email tom@example.com
```

Start the Airflow web server and scheduler:
```bash
airflow webserver --port 8080
airflow scheduler
```

### Issues Encountered:
**Airflow DAG Issues:** Encountered several issues related to DAG dependencies and task retries. These were resolved by adjusting the retry parameters and monitoring the Airflow UI logs.

### 5. DAG Script
The final DAG script (oulad_pipeline_dag.py) used to automate the pipeline tasks is included in this repo

### Issues Encountered:
**Task Failures:** Encountered failures in the load_to_sql task due to issues with SQLAlchemy and pandas compatibility. Solved by downgrading pandas and SQLAlchemy to compatible versions within the virtual environment.

### 6. Execution
Trigger the DAG
After configuring the DAG, trigger it manually:

```bash
airflow dags trigger oulad_pipeline
```

Check the status of each task:
```bash
airflow tasks states-for-dag-run oulad_pipeline <dag_run_id>
```
### Conclusion

This project demonstrates a complete ETL (Extract, Transform, Load) data pipeline using Apache Airflow, Hadoop (HDFS), PySpark, and MySQL. The pipeline automates data extraction, transformation, and loading, ensuring efficient processing and storage of educational data.

#### High-Level Overview of the Pipeline

1. **Data Extraction:**
   - The pipeline begins with the extraction of data from a ZIP file containing the Open University Learning Analytics Dataset (OULAD). 
   - **Component:** Apache Airflow's `BashOperator` triggers a shell command that unzips the data and loads it into **Hadoop HDFS**.

2. **Data Loading to HDFS:**
   - The extracted files are moved into a specific directory within the Hadoop Distributed File System (HDFS).
   - **Component:** HDFS handles the storage of the dataset across distributed nodes, ensuring fault tolerance and scalability. **Subcomponent:** DataNodes are used to store the data, while the NameNode manages metadata and the namespace.

3. **Data Transformation:**
   - **Component:** Apache Spark, specifically PySpark, is used for the transformation of the data. 
   - **Subcomponents:**
     - **Spark Session:** Initializes the Spark environment.
     - **PySpark DataFrame:** Reads the CSV files from HDFS and performs group-based aggregation of student scores.
   - The transformed data is converted to a Pandas DataFrame and saved as a CSV file for subsequent loading into MySQL.

4. **Data Loading to MySQL:**
   - The aggregated data is loaded into a MySQL database, where it can be accessed for real-time analysis and use.
   - **Component:** MySQL serves as the relational database where the final aggregated data is stored.
   - **Subcomponent:** SQLAlchemy manages the connection and insertion of data into MySQL using the `to_sql` method provided by Pandas.

#### Summary of Components Involved

- **Apache Airflow:** Orchestrates the entire workflow by scheduling and triggering the tasks.
- **Hadoop (HDFS):** Handles distributed storage of raw and transformed data, ensuring data resilience.
- **Apache Spark (PySpark):** Performs data transformations on large datasets using distributed processing.
- **MySQL:** Acts as the final storage for the processed data, making it available for real-time querying and analysis.
>>>>>>> e2e3019 (Initial commit: Add OULAD data pipeline project with all scripts and configurations)
