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




