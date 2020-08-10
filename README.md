# Plus Dental Data Engineering challenge
This is the solution repository for my PlusDental data engineering challenge. Here I have designed a command line application that can be run in two modes using the `run_as` argument - the api extractor tool and the dashboard applicatiion to visualize and explore the data collected.

The solution is also served using the functionality in two modules - `er_extractor` for the extractor applicatoon and `er_dashboard` for the dashboard application.


## Instructions for using the solution application
To set up the application on your machine
* I assume that you have docker running on your machine, if you don't have it then please [refer this page](https://docs.docker.com/get-docker/) to install docker.
* Clone this repository on your local and then use the docker-compose to build the target solution image. You can do it via this command:

    `docker-compose build` 
    
    Creating the build for the first time may take upto 2-3 minutes.
* Once the build is successful (Check [ss](https://raw.githubusercontent.com/rtspeaks360/exchange_rates_extractor/documentation/ss/docker-build.png) to see what a successful build looks like), we can fire up the application using docker-compose. You can do it via the following command: 

  `docker-compose up -d` 

  The -d flags runs the containers in daemon mode.
  <img src="https://raw.githubusercontent.com/rtspeaks360/exchange_rates_extractor/documentation/ss/docker%20compose.png">
* You can verify that the containers are live using `docker ps` command. This will show you all the live containers.
* Running the containers, runs the application in dashboard mode alongside a mysql db. You can visit the dashboard on your [localhost](http://0.0.0.0:8000). Right now you might see an empty graph since there would be no data that has been extracted from the API. See th following instructions to run the application in extractor mode.



## Using the application in extractor mode
In this step I assume, that you already have the docker containers running in daemon mode and you have access to your exchange rates dashboard.

Before running the application as extractor, let's first see what arguments are available using the -h flag. (We will be running the application inside the docker container)

You can get the list of arguments by using the following command:

  `docker exec -it exchange_rates_extractor_web_1 python main.py -h`

If everything worked for you, you should see the following help message
 
<img src='https://raw.githubusercontent.com/rtspeaks360/exchange_rates_extractor/documentation/ss/cmd%20docstrings.png'>

We can run the application as an extractor using the `run_as` argument. While running the application in extractor mode, you also need to specify the `get_data_by` sub argument. We can fetch data either for a date, or for a date range. We can also do an exhaustive fetch (Takes about 5 mins if multithreading is enabled). Or we can only get the data for the last 7 days (latest data).

If you plan to fetch rates for a high number of dates it is recommended to enable `multithreading` while running the application. You can also specify the number of threads you wish to create.

To show you an example command, let's say I wanted to fetch the data for the date range 2018-10-01 - 2019-10-31, the command would look like:

  `docker exec -it exchange_rates_extractor_web_1 python main.py --run_as extractor --multithreading --get_data_by date_range --start_date 2018-10-01 --end_date 2019-10-31`

Or if I wanted to do an exhaustive fetch:

`docker exec -it exchange_rates_extractor_web_1 python main.py --run_as extractor --multithreading --get_data_by exhaustive`

An example run looks like following, although in this run, no data is being fetched right now, this is just to give you an idea of how logging is handled:


<img src="https://raw.githubusercontent.com/rtspeaks360/exchange_rates_extractor/documentation/ss/example-run-extractor.png">


Once you have the data retrieved, your dashboard should have the latest data if you reload it. The updated dashboard looks like following:


<img src="https://raw.githubusercontent.com/rtspeaks360/exchange_rates_extractor/documentation/ss/example%20dashboard.png">


### Note on extractor:
All the points / feature requests for the extractor proicess can be handled / served using the 4 options for the subargument `get_data_by`. Any further enhancements can be made on top of the existing solution.
