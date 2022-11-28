# sqlalchemy-challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following sections outline the steps you must take to accomplish this task.
----------------
### Part 1: Climate Analysis and Exploration

In this section, you’ll use Python and SQLAlchemy to perform basic climate analysis and data exploration of your climate database. Complete the following tasks by using SQLAlchemy ORM queries, Pandas, and Matplotlib.
1. Use SQLAlchemy’s `create_engine` to connect to your SQLite database.
2. Use SQLAlchemy’s `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.
3. Link Python to the database by creating a SQLAlchemy session.

![Code](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/part_1_code.PNG)
---------------------

#### Precipitation Analysis

Perform an analysis of precipitation in the area
1. Find the most recent date in the dataset.
2. Select only the `date` and `prcp` values.
3. Load the query results into a Pandas DataFrame, and set the index to the date column.
4. Sort the DataFrame values by `date`.
5. Plot the results by using the DataFrame `plot` method
![Precip Code 1](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/part_2_code.PNG)
6. Use Pandas to print the summary statistics for the precipitation data.
![Precip Code 2](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/part_2_summary.PNG)
-----------------------

#### Station Analysis

Perform an analysis of stations in the area
1. Design a query to calculate the total number of stations in the dataset.
2. Design a query to find the most active stations (the stations with the most rows).
- List the stations and observation counts in descending order.
- Which station id has the highest number of observations?
![stn Code 1](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/stn_analysis_1.PNG)
- Using the most active station id, calculate the lowest, highest, and average temperatures.
3. Design a query to retrieve the previous 12 months of temperature observation data (TOBS).
- Filter by the station with the highest number of observations.
- Query the previous 12 months of temperature observation data for this station.
![stn code 2](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/stn_analysis_2.PNG)
- Plot the results as a histogram with `bins=12`

![stn histogram](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/histogram_most_active_st_temps.png)
--------------------

### Part 2: Design Your Climate App
Now that you have completed your initial analysis, you’ll design a Flask API based on the queries that you have just developed.

Use Flask to create your routes, as follows:

* `/`

    * Homepage.

    * List all available routes.

* `/api/v1.0/precipitation`

    * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

    * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

    * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

    * Query the dates and temperature observations of the most active station for the previous year of data.

    * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

    * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.

    * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.

    * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).
    
![climate app](https://github.com/acboi0824/sqlalchemy-challenge/blob/main/Instructions/Images/climate_app.PNG)
