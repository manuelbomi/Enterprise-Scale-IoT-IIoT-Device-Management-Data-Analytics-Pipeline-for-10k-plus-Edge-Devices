# Enterprise-Scale IoT-IIoT Device Management & Data Analytics Pipeline for 10k+ Sensors, RFIDs, and Edge Devices using AWS IoT Core, AWS Glue, SageMaker,  AWS IoT Devices Management and QuickSight

#### Overview
* This repository contains a fully automated, scalable, and secure solution for managing and analyzing data from thousands of  IoT / Industrial IoT devices including:
  
    • Industrial sensors  (temperature, humidity, vibration)
  
    • RFID tags & readers
  
    • Raspberry Pi  edge nodes
  
    • Smart meters, environmental sensors, and more
  
* It leverages core AWS IoT and analytics services such as AWS Glue, AWS SageMaker, AWS IoT Devices Management, AWS IoT Core, and AWS QuickSight

  ### Architecture Diagram 


mermaid

flowchart TD;
    A[IoT Devices (200+)] -->|MQTT| B[AWS IoT Core]
    B -->|IoT Rule| C[S3: /group/device/date/]
    C --> D[AWS Glue Crawler]
    D --> E[Glue Data Catalog]
    E --> F1[Athena]
    E --> F2[SageMaker ML Pipelines]
    E --> F3[QuickSight Dashboards]



---
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

    ```mermaid
    graph TD;
        A-->B;
        A-->C;
        B-->D;
        C-->D;

