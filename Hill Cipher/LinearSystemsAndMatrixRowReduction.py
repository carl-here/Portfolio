import pandas as pd
from ics import Calendar, Event
from datetime import datetime
import pytz

def csv_to_ics(csv_file, ics_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Create a new Calendar
    cal = Calendar()

    # Define timezone (adjust as needed)
    timezone = pytz.timezone('Europe/Oslo')  # Example: Oslo timezone

    # Iterate over each row in the CSV
    for _, row in df.iterrows():
        event = Event()

        # Parse start and end dates (adjust column names as needed)
        start_date = datetime.strptime(row['start_date'], '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(row['end_date'], '%Y-%m-%d %H:%M')

        # Localize the datetime to the specified timezone
        start_date = timezone.localize(start_date)
        end_date = timezone.localize(end_date)

        # Set event properties
        event.name = row['summary']
        event.description = row['description']
        event.begin = start_date
        event.end = end_date
        event.location = row['location']

        # Add the event to the calendar
        cal.events.add(event)

    # Save the calendar to an ICS file
    with open(ics_file, 'w') as f:
        f.write(cal.serialize())

# Example usage
csv_file = 'events.csv'  # Replace with your CSV file path
ics_file = 'events.ics'  # Output ICS file path
csv_to_ics(csv_file, ics_file)

print(f"Successfully converted {csv_file} to {ics_file}")
