# Ventib

Ventib offers the capability of parsing your speech and generating valuable statistics based on environmental factors. It also provides a search function, allowing users to sift through their past speech.

Ventib uses speech pattern analysis to provide statistics based on users’ real-time speech habits. Ventib analyses the content, location, and timing of your speech.

Chart.js and Google Maps' geotagging API are used to locate, graph, and extrapolate users’ speech

## Running Ventib
Using a virtualenv3 is highly recommended.
Install dependencies:

 - `python3`
 - `python3-devel`
 - `mysql`

Install Pip dependencies: `pip3 install -r requirements.txt`
Configurate your instance: `cp config.py web/ && vi web/config.py`
Run Ventib: `python3 run.py`

--

The mobile application:

https://github.com/cydrobolt/ventibapp
(Android)
