# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, select


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine)

print(Base.classes.keys())

# reflect an existing database into a new model

# reflect the tables

Station = Base.classes.station
Measurement = Base.classes.measurement


# Save references to each table


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    session.close()
    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp
    # Return the JSON representation of your dictionary
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Query the list of stations
    results = session.query(Station.station, Station.name).all()
    session.close()
    # Convert the query results to a list of dictionaries
    stations_list = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations_list.append(station_dict)
    # Return the JSON representation of your list
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session link from Python to the database
    session = Session(engine)

    # Query all temperature data for dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Close the session
    session.close()

    # Convert query results to a list of dictionaries
    start_temps = []
    for min_temp, avg_temp, max_temp in results:
        temp_dict = {}
        temp_dict["Min Temperature"] = min_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_dict["Max Temperature"] = max_temp
        start_temps.append(temp_dict)

    return jsonify(start_temps)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create session link from Python to the database
    session = Session(engine)

    # Query all temperature data for dates between the start and end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Close the session
    session.close()

    # Convert query results to a list of dictionaries
    start_end_temps = []
    for min_temp, avg_temp, max_temp in results:
        temp_dict = {}
        temp_dict["Min Temperature"] = min_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_dict["Max Temperature"] = max_temp
        start_end_temps.append(temp_dict)

    return jsonify(start_end_temps)