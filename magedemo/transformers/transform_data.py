import pandas

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
    # drop nulls
    data = data[data.airline.notnull()]

    # drop 0 passenger fligths
    data = data[data['travelled_passengers'] > 0]

    # type case
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
def test_airline(output, *args) -> None:
    assert output['airline'].isnull().sum()==0, 'airline value exists for all records'

@test
def test_passenger_count(output, *args) -> None:
    assert output['travelled_passengers'].isin([0]).sum()==0, 'passenger count is greater than 0'

@test 
def test_start_end(output, *args) -> None:
    assert (output['start'] == output['destination']).sum()==0, 'start and destination always differ'

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
