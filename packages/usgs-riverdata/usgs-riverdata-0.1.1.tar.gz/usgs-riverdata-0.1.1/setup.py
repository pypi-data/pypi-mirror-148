# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usgs_riverdata']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usgs-riverdata',
    'version': '0.1.1',
    'description': 'Pulls data from the USGS Water Data service',
    'long_description': '## What is it?\n\n**usgs-riverdata** is a Python package that exposes to the United State Geological Survey (USGS) waterdata api to python. The [USGS Waterdata](https://waterdata.usgs.gov/nwis/) system contains hydrologic data for United States rivers and tributaries.\n\n## Usage\n\nThe core functionality of this library is the Gage class. \n\nInitializing an object of this class requires a [site code](http://help.waterdata.usgs.gov/codes-and-parameters/codes#search_station_nm). Each USGS data source has unique location code used to retrive data. The default data length is 7 days, this is configurable using an ISO-8601 Duration format, as specifed [here](https://waterservices.usgs.gov/rest/IV-Service.html#Specifying). Additional parameters are optional and specified [here](https://waterservices.usgs.gov/rest/IV-Service.html#Specifying).\n\n## Dependencies\nThere are no outside dependencies. If Pandas is available, it will return data in a pandas.Dataframe.',
    'author': 'William French',
    'author_email': 'wdfrench13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wdfrench13/usgs-waterdata',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
