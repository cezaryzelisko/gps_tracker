# GPS Tracker

author: Cezary Zelisko

email: cezary.zelisko@gmail.com

## Description
GPS Tracker project consists of 3 subprojects:

1. [this](https://github.com/cezaryzelisko/gps-tracker) repository - locator,
2. [RESTful API](https://github.com/cezaryzelisko/gps-tracker-api) that is responsible for
handling requests from the locator (1.) and the mobile app (3.),
3. [mobile app](https://github.com/cezaryzelisko/gps-tracker-mobile) that retrieves data
from the API and visualizes it.

Locator is a Python app that publishes new coordinates of the device with the desired
frequency.

Authorization is based on the JSON Web Token (JWT) standard.

Currently only dummy locator is available. In the future a Raspberry PI-related solution
will be added.

## Install
In order to install `gps_tracker` package you should install all Python requirements.
They are collected in the `requirements.txt` file so to install them at once:

1. navigate to the directory where `gps_tracker` package is stored:

    ```cd /path/to/the/directory/of/gps_tracker```

2. issue the following command in a terminal:

    ```sudo pip3 install -r requirements.txt```

3. make sure that `gps_tracker` package can be imported (i.e. it's parent directory is
on the `PYTHONPATH`),

4. create a file named `credentials.json` and inside of it add two fields: `username` and
`password` that are valid credentials for your API user. Remember to use valid JSON
formatting,

5. ensure that the endpoints specified in the `config.json` file are valid and correspond
to those set in the GPS Tracker API.

## Test
You can run the prepared tests with the command (from the package directory):

```python -m unittest```

## Run
Dummy GPS Tracker can be run with the following command (remember to navigate to the
package directory first):

```python3 utils/dummy_gps_locator```
