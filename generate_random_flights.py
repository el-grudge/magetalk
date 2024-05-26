import random
from datetime import datetime, timedelta
import pandas as pd

def generate_flight_data(n, start_date, end_date):
    """Generate flight data."""
    flight_records = []
    
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    
    for _ in range(n):
        # Generate flight ID
        flight_id = "FL" + str(random.randint(1, 9999)).zfill(4)
        
        # Decide if airline field should be null
        if random.random() < 0.03:  # 3% chance
            airline = None
        else:
            # Generate airline
            airlines = [
                "Airline A", "Airline B", "Airline C", "Airline D", "Airline E"
            ]
            airline = random.choice(airlines)
        
        # Generate start and destination
        start = generate_airport()
        destination = generate_airport()
        while destination == start:  # Ensure start and destination are different
            destination = generate_airport()
        
        # Generate number of seats, booked passengers, and travelled passengers
        num_of_seats = random.randint(50, 300)
        max_booked_passengers = int(num_of_seats * 1.05)  # Allow up to 5% overbooking
        booked_passengers = random.randint(0, max_booked_passengers)
        travelled_passengers = random.randint(0, booked_passengers)
        
        # Generate scheduled takeoff datetime
        scheduled_takeoff_datetime = generate_datetime(start_datetime, end_datetime)
        
        # Decide if actual takeoff datetime should differ
        if random.random() < 0.2:  # 20% chance
            actual_takeoff_datetime = scheduled_takeoff_datetime + timedelta(hours=random.randint(1, 6))
        else:
            actual_takeoff_datetime = scheduled_takeoff_datetime
        
        # Generate landing datetime
        landing_datetime = actual_takeoff_datetime + timedelta(hours=random.randint(1, 8))
        
        flight_records.append((flight_id, airline, start, destination, num_of_seats, booked_passengers,
                                travelled_passengers, scheduled_takeoff_datetime, actual_takeoff_datetime,
                                landing_datetime))
    
    return flight_records

def generate_airport():
    """Generate a random airport code."""
    airports = [
        "JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SFO", "LAS", "SEA", "EWR",
        "MCO", "CLT", "PHX", "IAH", "MIA", "BOS", "MSP", "FLL", "DTW", "PHL"
        # Add more airports as needed
    ]
    return random.choice(airports)

def generate_datetime(start_datetime, end_datetime):
    """Generate a random datetime within the specified range."""
    return start_datetime + timedelta(seconds=random.randint(0, int((end_datetime - start_datetime).total_seconds())))

if __name__ == "__main__":
    n = 100000  # Number of records to generate
    start_date = ["2024-01-01","2024-02-01","2024-03-01","2024-04-01"]              
    end_date = ["2024-02-01","2024-03-01","2024-04-01","2024-05-01"]   
    colnames = ['flight_id','airline','start','destination','num_of_seats','booked_passengers','travelled_passengers','scheduled_takeoff_datetime','actual_takeoff_datetime','landing_datetime']
    
    for i, (s, e) in enumerate(zip(start_date, end_date)):
        flight_data = generate_flight_data(n, s, e)
        df = pd.DataFrame(flight_data, columns=colnames)
        df.to_csv(f"flight_data_0{i+1}2024.csv", index=False)
    