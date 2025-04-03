import json
import sys

import requests
from datetime import datetime, timedelta, timezone

GITHUB_API_URL='https://api.github.com/users/'
DB_PATH = 'github_db.json'

def load_json() -> dict:
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def save_json(database):
    with open(DB_PATH, 'w') as f:
        json.dump(database, f)

def terminate_application(error_message):
    print(f'Application terminated: {error_message}')
    sys.exit(1)

def get_github_user_info(user):

    user_url= GITHUB_API_URL + f'{user}/events'
    response = requests.get(user_url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        terminate_application(f'User not Found.')
    else:
        terminate_application(f'An error occured, please try again.')


def count_num_of_events(user_events):
    event_ctr = 0
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    events = {}
    for event in user_events:
        event_date = datetime.fromisoformat(event['created_at'].replace("Z", "+00:00"))
        if seven_days_ago <= event_date <= now:
            event_ctr += 1
            if events.get(event['type'], -1) == -1:
                events[event['type']] = 1
            else:
                events[event['type']] += 1
    return event_ctr, events

def process_github_tracker(user):
    database = load_json()


    if database.get(user, -1) == -1:
        print(f'{user} not found in database.')
        user_events = get_github_user_info(user)
        database[user] = user_events
        save_json(database)
    else:
        print(f'{user} found in database.')
        user_events = database[user]

    if not user_events:
        print(f'Public Events not found on username {user}.')
        sys.exit(1)

    event_ctr, events = count_num_of_events(user_events)
    print(f'{event_ctr} total events created within the past 7 days:')
    for event_name, event_num in events.items():
        print(f'\t{event_name}: {event_num}')
