# Weather report 

Procest is a weather app written in Python basen on data ftom Openweathermap.org.

## Features

- Import weather data from any point on globe from Openweathermap.org
- Store actual weather condition in local database
- plot historical data and forecast

## Installation

Project requred Python (tested on Python 3.9.2 on Debian). 

All instruction will be writen fo Debian system.

##### Clone of repository.

```sh
git clone https://github.com/Thagord/weather_report.git
```

##### Creation and activating of virtual environment for Python.

``` sh
cd weather_report
python -m venv venv
source venv/bin/activate
```

##### Install the dependencies.

```sh
pip isntall -r requrements.txt
```

## Run project

You need a API key form service openweathermap.org. It can by obtain by creating a account.
It must be writen to env variable.

```sh
export WEATHER_API_KEY="your_key"
```

Next step is to create a database file. So open the python console and paste code bellow.

```sh
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
engine = create_engine('sqlite:///sqlite.db', echo=True)

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    temperature = Column(Integer)
    wind_str = Column(Integer)
    wind_dir = Column(Integer)


Base.metadata.create_all(engine)
```

Now you can run project by typing
```sh
python main.py
```