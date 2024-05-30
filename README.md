# magetalk

## Prerequisites
Follow this [link](./prerequisite.md) for instructions on how to install the requirement prerequisites.

## Demo

### 1- Setup
Test postgres connection
```bash
psql -U postgres
```
Check existing tables
```sql
\d
```
Create a new directory for the project
```bash
mkdir magedemo
```
Create a virtual environment
```bash
# create venv
python3 -m venv venv
source venv/bin/activate
```
Test docker 
```bash
docker ps
```

### 2- Setup pgadmin to manage postgres
Pgadmin is a GUI for postgres. Pull and run its docker image with these commands 
```bash
docker pull dpage/pgadmin4  
docker run -p 8080:80 \
-e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' \
-e 'PGADMIN_DEFAULT_PASSWORD=SuperSecret' \
-e 'WTF_CSRF_CHECK_DEFAULT=False' \
-d dpage/pgadmin4  
```
To kill the container use this command
```bash
docker container kill [container id]
```

### 3- Start Mage with docker-compose
use this [link](https://github.com/mage-ai/compose-quickstart)
```bash
git clone https://github.com/mage-ai/compose-quickstart.git
```
Keep only the following files
- Dockerfile
- docker-compose.yml
- dev.env 
- requirements.txt

Add your project name in dev.env, then rename the file to `.env`.  

Start mage with this command:
```bash
docker-compose up -d
```

### 4- Create a new pipeline

### 5- Create a data loader block
Make sure to use raw.github file links. 

#### Note: You can add additional packages to mage by running `pip freeze > requirements.txt`.

### 5- Explore the data in a scratchpad block
Nulls and data types
```python
df.info() # remove nulls + typecase
```
Zeros
```python
df.describe()
```

Zero passenger flights
```python
# 0 passengers
mask = df['travelled_passengers'] == 0
df[mask][['num_of_seats', 'booked_passengers', 'travelled_passengers']].head(100)
```

Overbooked flights
```python
# overbooked
mask = df['booked_passengers'] > df['num_of_seats'] # create is_overbooked flag
df[mask][['num_of_seats', 'booked_passengers', 'travelled_passengers']].head(100) 
```

Delayed flights
```python
# convert to dates
import pandas as pd
df['actual_takeoff_datetime'] = pd.to_datetime(df['actual_takeoff_datetime'])
df['scheduled_takeoff_datetime'] = pd.to_datetime(df['scheduled_takeoff_datetime'])
# delayed
mask = df['actual_takeoff_datetime'] > df['scheduled_takeoff_datetime'] # create is_delayed flag
df[mask][['scheduled_takeoff_datetime', 'actual_takeoff_datetime']].head(100) 
```

### 6- Create a transformer block and link it to data loader
```python
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    # remove null airline
    data = data[data.airline.notna()]

    # remove 0 passengers flight
    mask = data.travelled_passengers > 0
    data = data[mask]

    # type cast
    data_types = {
        'flight_id': 'str',
        'airline': 'str',
        'start': 'str',
        'destination': 'str',
        'num_of_seats': 'Int64',
        'booked_passengers': 'Int64',
        'travelled_passengers': 'Int64',
        'scheduled_takeoff_datetime': 'datetime64', 
        'actual_takeoff_datetime': 'datetime64',
        'landing_datetime': 'datetime64'
    }
    data = data.astype(data_types)

    # create is_overbooked flag
    data['is_overbooked'] = (data['booked_passengers'] > data['num_of_seats']).astype(int)

    # create is_delayed flag
    data['is_delayed'] = (data['actual_takeoff_datetime'] > data['scheduled_takeoff_datetime']).astype(int)

    return data

@test 
def test_airline_name(output, *args) -> None:
    """
    Test for nulls in airline field
    """
    assert output.airline.isna().sum() == 0, 'The airline field has nulls'


@test 
def test_passenger_count(output, *args) -> None:
    """
    Test for nulls in airline field
    """
    assert (output.travelled_passengers == 0).sum() == 0, 'Flights can not have 0 passengers'


@test 
def test_start_end(output, *args) -> None:
    """
    Test that start is not destination
    """
    assert (output['start'] == output['destination']).sum()==0, 'Start and destination must always differ'


@test 
def test_landing_time(output, *args) -> None:
    """
    Test that flights don't arrive before leaving
    """
    assert (pd.to_datetime(output.landing_datetime) < pd.to_datetime(output.actual_takeoff_datetime)).sum() == 0, 'Flights can not arrive before taking off'


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
```

### 7- Test connection using a sql data loader
![sql data loader](./images/sqldataloader.png)

### 8- Set up postgres in mage   
Update postgres connection settings in io_config.yaml 
```yaml
POSTGRES_CONNECT_TIMEOUT: 10
POSTGRES_DBNAME: postgres
POSTGRES_SCHEMA: public # Optional
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_HOST: hostname # Replace hostname with IP 
POSTGRES_PORT: 5432
```

### 9- Data exporter
Load to postgres, and set if_exists = 'merge'

### 10- Create a docker container for your pipeline
First, create a new docker file magedemo.dockerfile
```docker
FROM mageai/mageai:latest

# Note: this overwrites the requirements.txt file in your new project on first run. 
# You can delete this line for the second run :) 
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PROJECT_NAME=magedemo
ENV MAGE_CODE_PATH=/home/mage_code
ENV USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

WORKDIR ${MAGE_CODE_PATH}

# Create the destination directory
RUN mkdir -p ${USER_CODE_PATH}

# Copy files from the host to the container
COPY mage_data mage_data
COPY magedemo ${USER_CODE_PATH}
```
Next, build the image and upload it to dockerhub
```bash
# build the image
docker build -t magedemo:v001 -f magedemo.dockerfile .
# upload to dockerhub
docker tag magedemo:v001 minasonbol/magedemo:magedemo
docker login
# enter your credentials
docker push minasonbol/magedemo:magedemo
```
Finally, pull the image and run it
```
# pull image from docker hub
docker pull minasonbol/magedemo:magedemo
# run image
docker run -d -p 6789:6789 minasonbol/magedemo:magedemo
```


## demo steps

- [x] local postgres running  
- [x] connect pgadmin to local postgres (for host use ip `hostname -I`)
- [x] files in github repo
- [x] load: load file and assert is not null
- [x] transform: use a datascratch to show df.info(), remove null rows, create is delayed flag, create is overbooked flag
- [x] export: dump to local postgres

### alternatively

- [ ] load from api (github)
- [ ] transform - type cast, add columns, take care of nulls
- [ ] export to gcs as parquet
- [ ] extract from parquet
- [ ] export to postgres


