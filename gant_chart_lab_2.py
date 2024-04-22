import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

activities = {
    'A': ("Choosing the pilot type", 6, 8, 9, []),
    'B': ("Drawing out of the technological scheme", 2, 5, 9, ['A']),
    'C': ("Elaboration of a mathematical model for the reactor", 1, 4, 6, ['A']),
    'D': ("Establishment of the physical properties in the domain of concentrations, temperature, and pressure", 25, 29, 37, ['A']),
    'E': ("Measure and control equipment acquisition", 22, 27, 33, ['B']),
    'F': ("Adjustment of the programs for experimental projects", 1, 1, 1, ['C']),
    'G': ("The use of the mathematical model for the reactor in a program", 1, 3, 9, ['C']),
    'H': ("Pilot building", 18, 24, 26, ['E']),
    'I': ("Raw materials acquisition", 13, 15, 16, ['E']),
    'J': ("Effectuation of the tests and adjustment of defects", 2, 5, 7, ['H']),
    'K': ("The establishment of the experiences program", 1, 2, 2, ['F']),
    'L': ("Pilot functioning", 3, 9, 10, ['I', 'J']),
    'M': ("The execution of the programmed experiences", 41, 75, 80, ['K', 'L']),
    'N': ("Validation of the experimental data", 1, 2, 3, ['M']),
    'O': ("Verification, adjustment, and perfecting of the mathematical model", 4, 11, 13, ['D', 'G', 'N']),
    'P': ("The elaboration of the documentation of the technological dimensioning of the reactor at an industrial scale", 20, 28, 29, ['O']),
}

start_date = datetime(2024, 4, 3)  # April 3, 2024

early_times = {
    'A': 0,
    'B': 6,
    'C': 6,
    'D': 6,
    'E': 11,
    'F': 9,
    'G': 9,
    'H': 38,
    'I': 38,
    'J': 62,
    'K': 10,
    'L': 54,
    'M': 66,
    'N': 141,
    'O': 143,
    'P': 154,
}

public_holidays = {
    "New Year's Day": datetime(2024, 1, 1),
    "Labor Day": datetime(2024, 9, 2),
    "Thanksgiving Day": datetime(2024, 11, 28),
    "Christmas Day": datetime(2024, 12, 25),
}

def next_working_day(date):
    while date.weekday() >= 5 or date in public_holidays.values():  # Saturday, Sunday, or public holiday
        date += timedelta(days=1) 
    return date

def calculate_end_date(start_date, duration):
    current_date = start_date
    while duration > 0:
        current_date = next_working_day(current_date + timedelta(days=1))
        duration -= 1
    return current_date

gantt_data = []
for activity, details in activities.items():
    name, a, b, c, prev = details  
    average_duration = (a + b + c) / 3  
    start_time = early_times[activity]  
    activity_start_date = calculate_end_date(start_date, start_time)  
    activity_end_date = calculate_end_date(activity_start_date, average_duration - 1)  
    gantt_data.append({
        'Activity': name,
        'Start Date': activity_start_date,
        'End Date': activity_end_date,
    })

df = pd.DataFrame(gantt_data)

fig = px.timeline(
    df,
    x_start="Start Date",
    x_end="End Date",
    y="Activity",
    color="Activity",
    title="Gantt Chart for Chemical Reactor Project",
    labels={"Start Date": "Start Date", "End Date": "End Date"},
)
fig.update_yaxes(categoryorder='total ascending')
fig.update_layout(showlegend=False) 
fig.show()
