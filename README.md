# NYC-Parking-Violations-Data-Analysis

### Skills:
* Containerization
* Terminal Navigation
* Pyhton Scripting
* AWS EC2 Provisioning

### Steps: 
* Provision an EC2 instances in AWS. 
* Create a docker container and write a python script to consume data from NYC Open Data website. 
* Provision an ElasticSearch cluster in AWS to stream data using Socrata Open Data API. 
* Use Kabana to analyze and visualize. 

### To build docker container run:

docker build -t bigdata1:1.0 project01/

### To run docker: 

docker run \
  -v ${PWD}:/app \
  -e APP_TOKEN= \
  -e ES_HOST= \
  -e ES_PASSWORD= \
  -e ES_USERNAME= \
  -e DATASET_ID= \
  bigdata1:1.0 --page_size=2 --num_pages=3

Note: Arguments like page_size is to indicate how many rows to download and num_pages how many pages to download. I used threading module to optimize the script. 

#### Data loaded: 630,348 rows.
#### Key findings:

1) 5 Most common violations in the state of NY are:
  - Wrong Way counts for 84.66%
  - Vehicle for Sale (Dealers only)
  - Vacant Lot
  - Unauthorized Bus Layover
  - Unaltered Comm Veh-NME/Address
2) Top 6 Average fine amount handed by agency type in state of NY:
  - The top average fine is 180$ by NYC Court Officers Agency
3) Status case violations shows:
  - over 60k observations have a status "Hearing Held Not Guilty"
  - over 20k observations have a status "Hearing Pending"
4) Average Fine Amount By Violation indicates: 
  - the highest average fine around 500$ for violations such: Failure to Display Bus Permit, Unauthorized Passenger Pick-up. 
  - on the lower range of over 100$ fine for Double Parking
  
![Screen Shot 2021-03-28 at 3 52 56 PM](https://user-images.githubusercontent.com/64224466/120901502-58197200-c609-11eb-8a86-2f8e345dfcc1.png)
![screencapture-search-sta9760s2021olesea-va5fbwnax6jpze3x2pyxcccdre-us-east-2-es-amazonaws-plugin-kibana-app-dashboards-2021-03-27-14_52_08](https://user-images.githubusercontent.com/64224466/120901507-5ea7e980-c609-11eb-9546-d86fc0161acd.png)





