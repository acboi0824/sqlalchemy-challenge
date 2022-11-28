# import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

###################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an hawaii database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference of the tables
measurements = Base.classes.measurement
station = Base.classes.station

################################
session = Session(engine)

# find the last date in the database
last_date = session.query(measurements.date).order_by(measurements.date.desc()).first()
last_date = dt.datetime.strptime(last_date[0],'%Y-%m-%d')
last_date = dt.date(last_date.year,last_date.month,last_date.day)

# Calculate the date 1 year ago from the last data point in the database
query_date = dt.date(last_date.year-1,last_date.month,last_date.day)

session.close()
################################

# Create an app
app = Flask(__name__)

################################
# Flask Routes
# Define what to do when user hits the index route
@app.route("/")
def home():
    """All available api routes."""
    return(
        f"Welcome to Sun's Hawaii Weather Tracker Page<br/> "
        f"<br/>" 
        f"Available Routes:<br/>"
        f"<br/>"  
        f"List of All Dates and Precipitation for Hawaii:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Link: <a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a><br/>"
        f"<br/>"
        f"List of Stations and Names in Hawaii:<br/>"
        f"/api/v1.0/stations<br/>"
        f"Link: <a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a><br/>"
        f"<br/>"
        f"List Temperature Observation from 08/23/2016 - 08/23/2017:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Link: <a href='/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a><br/>"
        f"<br/>"
        f"Min, Max, and Avg of temperatures for given start date: (Use 'yyyy-mm-dd' format):<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2011-01-01' target='_blank'>/api/v1.0/min_max_avg/2011-01-01</a><br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;<br/>"
        f"<br/>"
        f"Min, Max, and Avg of temperatures for given start and end date: (Use 'yyyy-mm-dd'/'yyyy-mm-dd' format for start and end values):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2012-01-01/2016-12-31' target='_blank'>/api/v1.0/min_max_avg/2012-01-01/2016-12-31</a>"
    )
    
######################################################

# create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session link
    session = Session(engine)

    """Return the dictionary for date and precipitation info"""
    # Query precipitation and date values 
    results = session.query(measurements.date, measurements.prcp).all()
        
    session.close()
    
    # Create a dictionary as date the key and prcp as the value
    precipitation = []
    for result in results:
        r = {}
        r["date"]= result[0]
        r["prcp_value"] = result[1]
        precipitation.append(r)

    return jsonify(precipitation )

#################################################################

# create stations route    
@app.route("/api/v1.0/stations")
def stations():
    # Create the session link
    session = Session(engine)
    
    """Return a JSON list of stations from the dataset."""
    # Query data to get stations list
    results = session.query(station.station, station.name).all()
    
    session.close()

    # Convert list of tuples into list of dictionaries for each station and name
    station_list = []
    for result in results:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_list.append(r)
    
    # jsonify the list
    return jsonify(station_list)

##################################################################

# create temperatures route
@app.route("/api/v1.0/tobs")
def tobs():
    # create session link
    session = Session(engine)
    
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # query tempratures from a year from the last data point. 
    #query_date  is "2016-08-23" for the last year query
    results = session.query(measurements.tobs, measurements.date).filter(measurements.date >= query_date).all()

    session.close()

    # convert list of tuples to show date and temprature values
    tobs_list = []
    for result in results:
        r = {}
        r["date"] = result[1]
        r["temprature"] = result[0]
        tobs_list.append(r)

    # jsonify the list
    return jsonify(tobs_list)

######################################################################

# create start route
@app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
    # create session link
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    # take any date and convert to yyyy-mm-dd format for the query
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

    # query data for the start date value
    results = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).filter(measurements.date >= start_dt).all()

    session.close()

    # Create a list to hold results
    t_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_list.append(r)

    # jsonify the result
    return jsonify(t_list)

##################################################################
@app.route("/api/v1.0/min_max_avg/<start>/<end>")
def start_end(start, end):
    # create session link
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end dates."""

    # take start and end dates and convert to yyyy-mm-dd format for the query
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")

    # query data for the start date value
    results = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).filter(measurements.date >= start_dt).filter(measurements.date <= end_dt)

    session.close()

    # Create a list to hold results
    t_list = []
    for result in results:
        r = {}
        r["StartDate"] = start_dt
        r["EndDate"] = end_dt
        r["TMIN"] = result[0]
        r["TAVG"] = result[1]
        r["TMAX"] = result[2]
        t_list.append(r)

    # jsonify the result
    return jsonify(t_list)

##########################################################
#run the app
if __name__ == "__main__":
    app.run(debug=True)