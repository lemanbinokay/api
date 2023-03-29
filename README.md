# A Restful API for Reference Interval Estimation in Metagenome Data
With the help of the API, the reference intervals of the functional abundance of the gut microbiota can be estimated across multiple metabolic pathways.

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
| POST | http://127.0.0.1:5000/referenceIntervalResults/ | Reference interval estimation results for selected sample id and selected pathway in HTML format |
| POST | http://127.0.0.1:5000/refiner/pdf/ | Reference interval estimation results for selected sample id and selected pathway in PDF format|
| POST | http://127.0.0.1:5000/referenceIntervalResults/json/| Reference interval estimation results for selected sample id and selected pathway in JSON format

 |
