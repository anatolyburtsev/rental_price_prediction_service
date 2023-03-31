# Rental Price Prediction Service 

## 1. Overview
That document contains high level design of the service to predict rental price of apartment or house based on predefined input params.

## 2. Requirements

### Functional requirements (What)
- [FR1] Service provides monthly rental price for a given apartment or house based on predefined customer-input data


### Non-functional requirements (How)
- [NFR1] Service provides a REST endpoint
- [NFR2] Service has a web interface (stretch requirement)
- [NFR3] Service build on the top of ML model
- [NFR4] Model trained on data from at least 2 sources
- [NFR5] Service is able to detect model drift (TODO: clarify what is that) and retrain and redeploy model fully automatically 
- [NFR6] Service can be rolled back to previous model version semi-automatically
- [NFR7] Latency `p99 < 1s`
- [NFR8] Accuracy: `MAE < 5%`
- [NFR9] Data collection takes less than 24 hours
- [NFR10] Model training and evaluation take less than an hour

## 3. Design proposal
TBD

## 4. Design analysis
TBD

## 5. Implementation details
TBD

## 6. References
[Track's url](https://ods.ai/tracks/ml-in-production-spring-23)


## 7. Appendix

### Appendix A: Project requirements
- Read and merge data from different files/formats 
- Moderate data size to simplify storing and versioning data
- EDA (charts for existing values, data distributions, calculation of standard statistics, e.g. mean, median etc)
- Extend dataset by fetching data from external sources, e.g. via API / parsing web pages
- Data engineering 
- Using multiple possible solutions for future comparative analysis
- Explanation of used quality metrics 