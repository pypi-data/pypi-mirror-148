## What is it?

**usgs-riverdata** is a Python package that exposes to the United State Geological Survey (USGS) waterdata api to python. The [USGS Waterdata](https://waterdata.usgs.gov/nwis/) system contains hydrologic data for United States rivers and tributaries.

## Usage

Import using 

```python
import usgs_riverdata
```

The core functionality of this library is the Gage class. 

Initializing an object of this class requires a [site code](http://help.waterdata.usgs.gov/codes-and-parameters/codes#search_station_nm). Each USGS data source has unique location code used to retrive data. The default data length is 7 days, this is configurable using an ISO-8601 Duration format, as specifed [here](https://waterservices.usgs.gov/rest/IV-Service.html#Specifying). Additional parameters are optional and specified [here](https://waterservices.usgs.gov/rest/IV-Service.html#Specifying).

## Dependencies
There are no outside dependencies. If Pandas is available, it will return data in a pandas.Dataframe.