# miad-dsa-project
Proyecto Final para Despliegue de Soluciones Analíticas en MIAD

---
title: "U.S. Crime Statistics Dataset"
author: "Dataset Maintainer"
date: "2024-10-17"
output: html_document
---

# U.S. Crime Statistics Dataset

This comprehensive dataset provides an in-depth overview of crime statistics across the United States. It includes various types of crimes, ranging from violent offenses like homicide and assault to property crimes such as theft and burglary. The dataset is meticulously organized to offer insights into crime trends, geographical variations, and temporal patterns, providing a valuable resource for researchers, policymakers, and analysts.

## About this Dataset

The dataset is structured to facilitate exploration of core crime details, classifications, victim information, and geographical context. Below is a detailed overview of the data fields included.

### Core Crime Information

- **DR_NO**: Unique identifier for each reported crime.
- **Date Rptd**: Date the crime was reported to law enforcement.
- **DATE OCC**: Date the crime occurred.
- **TIME OCC**: Time the crime occurred.
- **AREA**: Geographic area or precinct where the crime took place.
- **AREA NAME**: Descriptive name of the area.
- **Rpt Dist No**: Reporting district number.

### Crime Classification

- **Part 1-2**: Indicates whether the crime is a Part 1 (serious) or Part 2 (less serious) offense.
- **Crm Cd**: Crime code or classification number.
- **Crm Cd Desc**: Description of the crime code.
- **Mocodes**: Motivations or circumstances related to the crime.

### Victim Information

- **Vict Age**: Age of the victim.
- **Vict Sex**: Sex of the victim.
- **Vict Descent**: Racial or ethnic background of the victim.

### Location and Context

- **Premis Cd**: Premises code (e.g., residential, commercial).
- **Premis Desc**: Description of the premises.
- **Weapon Used Cd**: Code for the weapon used (if any).
- **Weapon Desc**: Description of the weapon.

### Additional Information

- **Status**: Current status of the case (e.g., open, closed).
- **Status Desc**: Description of the case status.
- **Crm Cd 1, 2, 3, 4**: Additional crime codes if applicable.
- **LOCATION**: General location of the crime.
- **Cross Street**: Intersection or nearby street.
- **LAT, LON**: Latitude and longitude coordinates of the crime location.

## Suggestions and Contributions

If you have any suggestions to improve this dataset or wish to contribute, feel free to add your input through the contribution guidelines.

---


## DVC

Nuestra herramienta de control de versiones de datos es DVC. Para poder trabajar con los datos originales, los cuales se encuentran almacenados en S3 se debe instalar DVC ejecutando:

- `pip install dvc`
- `pip install "dvc[s3]"`

Para descargar los datos localmente requeriras tener configurado:

Opcion 1: Instalar aws cli
- `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o ~/"awscliv2.zip" `
- `sudo apt install unzip`
- `unzip ~/awscliv2.zip -d ~/`
- `sudo ~/aws/install`
- `Configurar credenciales de AWS`
- `aws configure --> Se debe insertar la secret key y la acess key. La region debe ser us-east-1`
- `aws configure set aws_session_token SESSIONTOKEN`

Opcion 2: definir variables de entorno (Si no se instalo AWS CLI)

export AWS_SECRET_ACCESS_KEY=

export  AWS_ACCESS_KEY_ID=

export  AWS_SESSION_TOKEN=

Una vez se tenga instalado dvc y se cuente con acceso programatico a AWS se debe ejecutar el siguiente comando para traer del BucketS3 los archivos del proyecto, los cuales quedaran en el folder "data":
- `dvc pull`

## MLflow

Asegúrate de tener instalados los siguientes paquetes para poder registrar los experimentos de los modelos en MLflow:

- `pip3 install mlflow`
Ejecute la interfaz grafica de MLFLOW: mlflow ui —> Queda en el la dirección: http://localhost:5000/