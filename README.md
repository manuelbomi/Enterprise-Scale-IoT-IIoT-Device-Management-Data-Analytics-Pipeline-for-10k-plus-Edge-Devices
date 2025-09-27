# Enterprise-Scale IoT-IIoT Device Management & Data Analytics Pipeline for 10k+ Sensors, RFIDs, and Edge Devices using AWS IoT Core, AWS Glue, SageMaker,  AWS IoT Devices Management and QuickSight

#### Overview
* This repository contains a fully automated, scalable, and secure solution for managing and analyzing data from thousands of  IoT / Industrial IoT devices including:
  
    • Industrial sensors  (temperature, humidity, vibration)
  
    • RFID tags & readers
  
    • Raspberry Pi  edge nodes
  
    • Smart meters, environmental sensors, and more
  
* It leverages core AWS IoT and analytics services such as AWS Glue, AWS SageMaker, AWS IoT Devices Management, AWS IoT Core, and AWS QuickSight

 
 ### Architecture Flowchart
```ruby

flowchart TD;
    A[IoT Devices (200+)] -->|MQTT| B[AWS IoT Core]
    B -->|IoT Rule| C[S3: /group/device/date/]
    C --> D[AWS Glue Crawler]
    D --> E[Glue Data Catalog]
    E --> F1[Athena]
    E --> F2[SageMaker ML Pipelines]
    E --> F3[QuickSight Dashboards]

```
---


### Repository Structure 
```ruby
iot-enterprise-platform/
├── provisioning/
│   └── provision_device.py           # Auto-onboarding script
├── publishers/
│   └── mqtt_publisher.py             # Simulated data publisher
├── glue_jobs/
│   └── clean_and_transform.py        # Glue ETL script
├── sagemaker_pipeline/
│   ├── pipeline.py                   # SageMaker pipeline
│   ├── train_model.py                # Model training script
│   ├── data/
│   │   └── cleansed/                 # Cleansed training data from S3
│   └── models/                       # Trained models go here
├── quicksight/
│   └── dashboard_guide.md            # Steps to build dashboard
├── templates/
│   └── fleet_template_group1.json    # Fleet provisioning template
├── certs/
│   ├── claim_cert.pem                # Shared claim cert
│   ├── claim_private.key             # Shared private key
│   └── AmazonRootCA1.pem             # Root CA

```
---

### Project Features

| Feature                         | Descsription                                      |
|---------------------------------|--------------------------------------------------|
|  Auto-Onboarding (Fleet Provisioning) | Auto-register devices using claim certificates   |
|  Secure MQTT Messaging         | MQTT over TLS with X.509 certs                   |
|  S3 Data Lake Partitioning      | `/group/device/year/month/day/` layout          |
|  ETL with AWS Glue              | Cleans JSON → Parquet with metadata             |
|  Athena / QuickSight Integration | Query and visualize sensor data                 |
|  SageMaker Pipelines           | Train ML models on IoT data                      |
|  Live Dashboards               | Real-time metrics & alerts                       |

---

## Enterprise IoT/IIoT Sensors' Data Analytics, ML Pipeline Designs and Dashboarding

### To be able to onboard thousands of different enetrprise IoT/IIoT devices 
* Start the project from here: https://github.com/manuelbomi/Enterprise-Scale-IoT-Device-Management-Data-Ingestion-Using-AWS-Services-for-thousands-IoT-Devices

*After finishing the inital phase of the project, and once data from IoT/IIoT devices is being ingested into Amazon S3, organizing it smartly is the key to enabling:

      * querying
      
      * dashboarding and 
      
      * ML pipelines designs:

  In the AWS ecosystem, the above 3 components can be achieved by the following AWS services: 
  
     *  1. Easy ETL & analysis (via Glue, Athena, Redshift, etc.)
     
     *  2. Machine learning pipelines (via SageMaker or custom ML workflows)
     
     *  3. Dashboarding (via QuickSight, Tableau, Grafana, etc.)


 ### Goal: Smart Organization of S3 Bucket Data from IoT Devices

 ### To structure S3 data like a data lake with:
 
    • Logical partitioning (e.g., by device group, ID, and date)
    
    • Queryability (via Glue Catalog / Athena)
    
    • Scalability to 200+ devices
    
    • Compatibility with ETL, ML, and dashboards

### ....follow the steps below:

#### STEP 1: Organize Your S3 Structure by Group, Device, Date

* Use this folder/key format in your AWS IoT Rule. Check a good rule in step 6 of the preceding project here:   https://github.com/manuelbomi/Enterprise-Scale-IoT-Device-Management-Data-Ingestion-Using-AWS-Services-for-thousands-IoT-Devices
  
* Accomplish a partitioned storage in your S3. Arrange your data as shown in the partitioned storage format below:

```ruby

s3://your-bucket-name/
├── group1/
│   ├── temp-001/
│   │   ├── year=2025/month=09/day=23/
│   │   │   └── data-1634567890000.json
│   │   │   └── data-1634567891000.json
│   └── temp-002/
│       └── ...
├── group2/
│   └── rfid-001/
│       └── year=2025/month=09/day=23/
│           └── ...

```

Partitioned storage, makes querying and ETL jobs 10x easier. 

##### Modify AWS IoT Rule to Match

* In your IoT Rule, change the S3 action to:
  
```ruby
{
  "s3": {
    "roleArn": "arn:aws:iam::<acct>:role/IoTRole",
    "bucketName": "your-bucket-name",
    "key": "iot_data/${group()}/${thingName()}/year=${timestamp(\"yyyy\")}/month=${timestamp(\"MM\")}/day=${timestamp(\"dd\")}/${timestamp()}.json"
  }
}

```
The Enterprise Data Architect will need to set the thingName and use the device group name as a tag or topic prefix.

####  STEP 2: Use AWS Glue to Catalog Your IoT Data

Once data is in S3:

<ins>2.1</ins> Create Glue Crawlers

    • Create a crawler per device group or a single one for the bucket
    
    • Point it to the base S3 path

s3://your-bucket-name/group1/

    • Crawler auto-detects schema and registers tables in the AWS Glue Data Catalog

<ins>2.2</ins> Resulting Table Structure (in Athena/Redshift Spectrum)

* Run SQL queries like:

```ruby

SELECT temperature, humidity, timestamp
FROM "iot_database"."group1_temp001"
WHERE year = '2025' AND month = '09' AND day = '23'

```

####  STEP 3: ETL Pipelines for Cleansing, Transforming, and Enriching

#### See how to set up and use AWS Glue here: 

* Use AWS Glue (Spark) or AWS Lambda to:
  
    • Clean missing/null values
  
    • Transform timestamp formats
  
    • Add metadata (e.g., location, thresholds)
  
    • Convert JSON → Parquet (columnar, compressed)
  
    • Load to Redshift/S3/Databases

#### Example Glue Job:

```ruby

df = glueContext.create_dynamic_frame.from_catalog(
    database = "iot_database",
    table_name = "group1_temp001"
)
df_clean = df.drop_null_fields().filter(lambda x: x["temperature"] < 80)

```

#### STEP 4: Build Machine Learning Pipelines

#####  Use Amazon SageMaker Pipelines or your own tools to:
  
    • Pull training data from S3 or Athena
  
    • Run feature engineering (e.g., rolling averages, anomalies)
  
    • Train models (e.g., temperature prediction, vibration anomaly detection)
  
    • Deploy endpoints (inference)


<ins>Example</ins>:

* Train a model to predict HVAC failures based on vibration and temperature patterns.

SageMaker supports:

    • CSV/Parquet input from S3
    
    • Athena queries as data source
    
    • SageMaker Feature Store



#### STEP 5: Dashboarding with QuickSight, Grafana, etc.

##### You can now build dashboards from:

    • Amazon QuickSight via Athena or Redshift
    
    • Grafana + Amazon Managed Grafana
    
    • Tableau, Power BI via S3/Glue/Redshift
    
    
  #### Example Use Cases:

    • Live dashboards of temperature trends by group
    
    • Daily usage summary per device
    
    • Alerts for out-of-range sensor readings


### Summary of the Workflow (step 1 - step 5)

```ruby

graph TD;
A[IoT Devices (200+)] -->|MQTT| B[AWS IoT Core]
B -->|Rule Action| C[S3 (grouped + partitioned)]
C --> D[AWS Glue Crawler]
D --> E[Glue Catalog / Athena Tables]
E --> F1[QuickSight Dashboard]
E --> F2[ETL via Glue Jobs]
E --> F3[ML Pipelines in SageMaker]

```


### Best Practices
| Area          | Practice                                                       |
|---------------|----------------------------------------------------------------|
| Data layout   | Use partitioned S3 paths (`group/device/date`)                 |
| File format   | Convert JSON → Parquet for analytics                           |
| Cataloging    | Use Glue Crawlers to auto-update schema                        |
| Permissions   | IAM roles must allow IoT → S3 and S3 → Glue/SageMaker          |
| Cost control  | Enable S3 lifecycle policies for cold storage                  |


---


## Examples of the Workflow  (AWS Glue, AWS SageMaker, AWS QuickSight)

## 1. AWS Glue Job Script (ETL): Clean & Convert IoT Data

#### We desire to create a Glue Job script that:

    • Reads raw IoT JSON data from S3
    
    • Filters and cleans the data
    
    • Adds metadata (e.g., group/device)
    
    • Converts to Parquet for optimized querying
    
    • Stores cleaned data into another S3 location

#### Directory Structure in the Repository

```ruby
glue_jobs/
├── raw/              # Raw incoming data (JSON)
│   └── group1/temp-001/year=2025/...
├── cleaned/          # Cleaned, transformed Parquet files
└── scripts/
    └── clean_and_transform.py
```

* Please check the repo  under  scripts/clean_and_transform.py  for the AWS Glue Script

#### Setup via AWS Console

   #### 1. Upload clean_and_transform.py to S3
    
   #### 2. In AWS Glue:
    
        ◦ Create a new Glue Job
        
        ◦ Choose "A new script authored by you"
        
        ◦ Use Spark (Python) and attach the uploaded script
        
        ◦ Assign a role with access to both raw and cleaned buckets
        
    3. Schedule it or trigger it from a Lambda  (i.e. AWS Lambda Fucntion)

---

## 2.  SageMaker ML Pipeline (Model Training)

#### We desire to use SageMaker Pipelines to:

    • Pull cleaned data from S3
    
    • Train a simple temperature prediction model
    
    • Evaluate it
    
    • Register it for deployment

#####Folder Structure (AWS SageMaker Studio) 

```ruby
sagemaker-pipeline/
├── pipeline.py             # Pipeline definition
├── train_model.py          # Training script
├── data/
│   └── cleaned/            # Cleaned training data from S3
└── models/
```

* Please check the repo  under sagemaker_pipeline for the script pipeline.py

* Run the script via SageMaker Studio or SDK to start training.

---

## 3. QuickSight Dashboard

#### QuickSight integrates with:

    • Athena (for S3 data)
    
    • Glue Catalog
    
    • Redshift
    
#### Steps to Build Dashboard from IoT Data

#### Step 1: Enable Athena and QuickSight Integration

    • Go to AWS QuickSight
    
    • Connect to Athena
    
    • Choose the Glue database (iot_database)
    
    • Choose the cleaned table (e.g., group1_temp001)

#### Step 2: Build Visuals for teh QuicSight Dashboard

Suggested visuals:

```ruby

| Metric                  | Chart Type               |
|-------------------------|--------------------------|
| Temperature over time   | Line chart               |
| Avg temp per device     | Bar chart                |
| Device anomalies        | Scatter / Alert indicators |
| Humidity vs Temp        | Correlation scatterplot  |

```

#### Step 3: Filter & Drilldowns for the QuickSight Dashboard

    • Add filters by group, device_id, timestamp
    
    • Use date range slicers
    
    • Create custom aggregations for weekly/monthly summaries

### Summary of Deliverables for the Workflow Example

| Output                  | Purpose                                |
|-------------------------|----------------------------------------|
| clean_and_transform.py | ETL raw JSON → clean Parquet           |
| pipeline.py            | ML pipeline for model training         |
| QuickSight Setup       | For dashboarding and live insights     |

---


## How to Deploy this Repository for Your Enterprise-Scale Project

#### Clone the Repository

* git clone 

* cd iot-enterprise-platform

#### Prerequisites

    • AWS CLI configured (aws configure)
    
    • IAM roles for:
    
        ◦ AWS IoT access
        
        ◦ Glue job execution
        
        ◦ SageMaker execution
        
    • S3 buckets created:
    
        ◦ iot-raw-data-bucket

        ◦ iot-cleaned-data-bucket
        
    • Device claim certificate and private key provisioned


### Provision Devices (On Boot) 

#### Flash each device (or Raspberry Pi gateway) with:

    • provisioning/provision_device.py
    
    • certs/claim_cert.pem
    
    • Device-specific serial ID
    
#### Provisioning script auto-registers the device on AWS IoT Core and retrieves unique certs.

#### Example usage: python provisioning/provision_device.py --serial rpi-0042

#### This will:

    1. Connect to AWS IoT Core using the claim certificate
    
    2. Publish a provisioning request to the template
    
    3. Receive a new cert/key for the device
    
    4. Save them under certs/<thing-name>-certificate.pem.crt etc.

*python publishers/mqtt_publisher.py*


#### Publishes mock sensor data to MQTT topics: 

#### iot/group1/temp-001/data


#### ETL with AWS Glue

    • Upload glue_jobs/clean_and_transform.py to S3
    
    • Create Glue Job via AWS Console or CDK
    
    • Input = iot-raw-data-bucket/group1/
    
    • Output = iot-cleaned-data-bucket/cleaned/

#### Train Machine Learning Model with SageMaker 

* cd sagemaker_pipeline
  
*python pipeline.py*


#### Pulls Parquet data from S3

    • Trains temperature predictor or anomaly detector
    
    • Stores model in s3://iot-cleaned-data-bucket/models/
    
#### Create QuickSight Dashboard

    • Connect QuickSight to Athena
    
    • Use iot_database.group1_temp001
    
    • Build visuals: temperature trend, device health, alert zones
    

#### Example Use Cases:

    • Predict cold-chain failure from temperature drift
    
    • Detect motor failure from vibration spikes
    
    • Track asset movement with RFID
    
    •  Monitor smart grid energy load
    
    • Aggregate CO₂ levels for environmental compliance
    
#### Security

    • X.509 certificates per device
    
    • MQTT over TLS
    
    • IAM Roles for service access
    
    • S3 bucket policies for secure access
    
#### Scaling Notes

    • Handles 1000+ devices via fleet provisioning and thing groups
    
    • Use IoT Device Defender for monitoring large fleets
    
    • Use IoT Greengrass for local edge processing (optional)



---

Thank you for reading

---

### **AUTHOR'S BACKGROUND**
### Author's Name:  Emmanuel Oyekanlu
```
Skillset:   I have experience spanning several years in data engineering, developing scalable enterprise data pipelines,
enterprise solution architecture, architecting enterprise systems data and AI applications,
software and AI solution design and deployments, data science, high performance computing (GPU, CUDA), machine learning,
NLP, Agentic-AI and LLM applications as well as deploying scalable solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com

Websites (professional):  http://emmanueloyekanlu.com/
Websites (application):  https://app.emmanueloyekanluprojects.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```
[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)
















