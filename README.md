# A Restful API for Reference Interval Estimation in Metagenome Data
Welcome to the documentation for our RESTful API. The Reference Interval Estimation API allows you to estimate the reference intervals of the functional abundance of gut microbiota across multiple metabolic pathways. This API provides various endpoints to interact with the data and obtain reference interval estimates. Below are the details for installation and usage of the API.

The application programming interface (API) was developed using the open-source Python programming language and the Flask framework as the software development platform. Any operating system can be selected as the server, and it is recommended to choose a Linux-based operating system.

## Installation:

To set up the Docker container for running the Restful API. You can pull the latest version from Docker Hub.
Commands to download the Restful API for Reference Interval Estimation image:

```
docker pull lemanbinokay/api
```

To run the container:

```
docker run -d -p 5001:5000 lemanbinokay/api
```

## Usage
To access the functions of the API, registration is required. Clicking on the "Register" option in the upper-right corner will open the registration page. After providing the necessary information, the registration process will be completed. Once the user logs in using the login section, the pages containing the functions will become accessible. 

### Data Preparation

Before using this API, ensure that you have the following prerequisites installed on your system:

1- Nextflow (If not installed, you can set up a Conda environment as described below)
2- Conda
3- Docker (for nf-core/ampliseq)
4- Python (for PICRUSt2)

#### Conda Environment Setup (for Nextflow)
If Nextflow is not installed, you can set up a Conda environment as follows:

```
conda create --name nextflow_stable python=3.8
conda activate name
conda install -c bioconda nextflow
```
If you need more assistance with the Nextflow installation, please visit this page: https://nf-co.re/docs/usage/installation.

#### Microbiome Analysis with nf-core/ampliseq
Run the nf-core/ampliseq pipeline with the following command:

```
nextflow run nf-core/ampliseq \
    -r 2.3.2 \
    -profile docker \
    --input "data" \
    --FW_primer GTGYCAGCMGCCGCGGTAA \
    --RV_primer GGACTACNVGGGTWTCTAAT \
    --picrust \
    --outdir "ampliseq_outputs"
```
You can modify this code as you wish, but make sure to use the --picrust parameter. If you need more assistance with the Nextflow installation, please visit this page: https://nf-co.re/ampliseq/2.6.1/docs/usage/.

#### Running PICRUSt2
After running nf-core/ampliseq, you need to run PICRUSt2 using the following command to analyze functional abundances:

```
pathway_pipeline.py -i /path/to/KO_metagenome_out/pred_metagenome_unstrat.tsv.gz \
    -o /path/to/picrust2_results \
    -m /path/to/database.txt \
    -p 1 --no_regroup --coverage --skip_minpath
```

PICRUSt2 is a tool for predicting functional abundances of microbiota pathways based on KEGG databases. The database.txt file contains KEGG pathway IDs related to the selected pathways.
After running PICRUSt2, you will have a functional abundance file that represents the activity of selected pathways in the microbiome data. You can upload this file to our API to estimate reference intervals.

### Data Upload to API
The API provides users with three versatile output formats: a web interface (HTML), JSON output for integration with other programs, and PDF output for end-user convenience. To easily incorporate data in CSV file format into the database, simply click the "Upload CSV" button on the "Upload New Data" page. Users can then upload the edited data in the specified file format using the "Sample File" button on the same page.

### Browse Function
The database encompasses functional abundance results from 57 individuals for 11 distinct pathways. Users have the flexibility to contribute data for these 11 pathways or opt for different pathways of their choice. For user convenience and quick access to desired data, the "Browse" page offers a comprehensive list of functional abundances based on the selected sample. Additionally, the "Browse" page allows users to cross-check pathway abundances against reference intervals for the chosen sample.

### Estimation of Reference Intervals
The API facilitates data retrieval in JSON format through the "JSON Output" button, in HTML format, or as a downloadable PDF using the "PDF" button. On the "Estimate Reference Interval" page, users can estimate reference intervals for the selected pathway and obtain outputs in JSON format through the "JSON Output" button, in HTML format, or as a downloadable PDF using the "PDF" button.

## End Points of the API
| Method | Endpoint | Description |
| -------- | -------- | -------- |
| GET | http://127.0.0.1:5000/listPathways/| List pathway abundance or check pathway abundances to the reference intervals |
| POST | http://127.0.0.1:5000/listPathways/json2/| Listed pathway abundances for selected id in JSON format |
| POST | http://127.0.0.1:5000/listPathways/json/| Result for checking pathway abundances to the reference intervals in JSON format |
| POST | http://127.0.0.1:5000/listPathwaysWithID2/| Listed pathway abundances for selected sample id in HTML format |
| POST | http://127.0.0.1:5000/listPathwaysWithID/ | Result for checking pathway abundances to the reference intervals|
| GET  | http://127.0.0.1:5000/Pathways/pdf/{id}/ | Listed pathway abundances for selected sample id in PDF format |
| GET, POST| http://127.0.0.1:5000/createPathways/| Add pathway abundance results |
| GET, POST| http://127.0.0.1:5000/editPathways/{id}/ | Edit in listed pathway abundances for selected sample id  |
| POST | http://127.0.0.1:5000/deletePathways/{id}/ | Delete in listed pathway abundances for selected sample id  |
| POST | http://127.0.0.1:5000/uploadCSV/ | Upload CSV file of pathway abundance results|
| POST | http://127.0.0.1:5000/referenceInterval/ | Reference interval estimation |
| POST | http://127.0.0.1:5000/referenceIntervalResults/ | Reference interval estimation results for selected sample ID and selected pathway in HTML format |
| POST | http://127.0.0.1:5000/refiner/pdf/ | Reference interval estimation results for selected sample ID and selected pathway in PDF format|
| POST | http://127.0.0.1:5000/referenceIntervalResults/json/| Reference interval estimation results for selected sample id and selected pathway in JSON format|

You can make HTTP requests to the specified endpoints using appropriate methods (GET or POST) to interact with the API and perform actions such as listing pathways, estimating reference intervals, and managing pathway abundance data. Please note that you need to replace http://127.0.0.1:5000/ with the actual URL where your API is hosted if it's not running locally. For further assistance or inquiries, please contact the API administrator.

## Conclusion

In conclusion, the Reference Interval Estimation API for Metagenome Data provides a powerful tool for researchers and analysts working with gut microbiota functional abundance data. This API, built using Python and Flask, offers a range of endpoints to assist in data preparation, analysis, and visualization. Before using the API, it's essential to ensure that you have the necessary prerequisites installed, such as Nextflow, Conda, Docker, and Python, depending on your specific analysis needs. The API's key features include data upload and management, pathway abundance browsing, and the estimation of reference intervals. Users can conveniently upload their data in CSV format, explore pathway abundances, and estimate reference intervals for selected pathways and samples. The API endpoints are well-documented, with clear descriptions of their functionality, HTTP methods, and URL paths. Users can interact with the API by making HTTP requests to the appropriate endpoints, allowing them to integrate this functionality into their workflows seamlessly. 

If you have any questions, require assistance, or need further information, don't hesitate to contact the API administrator for support. This API opens up exciting possibilities for researchers to gain insights into the functional abundance of gut microbiota and its relation to metabolic pathways, contributing to advances in microbiome research and personalized healthcare.
