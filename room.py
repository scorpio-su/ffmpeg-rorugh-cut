import json
import requests
from datetime import datetime
from typing import Any
from pathlib import Path


# Load and parse JSON data
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Calculate the time difference using timedelta
def calculate_time_difference(start_time_str, end_time_str):
    # Define the time format
    time_format = "%H:%M:%S"

    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
    # The difference between two datetime objects is a timedelta object
    return end_time - start_time


def fetch_json_data(url: str) -> Any:
    """
    Fetch JSON data from the given URL.

    :param url: URL to request JSON data from
    :return: Parsed JSON data if the request is successful, otherwise None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.RequestException as req_err:
        print(f"Error fetching data from {url}: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error parsing JSON data: {json_err}")
    return None


def save_json_to_file(data: Any, file_path: str) -> None:
    """
    Save the JSON data to a file.

    :param data: JSON data to be saved
    :param file_path: Path where the JSON file will be saved
    """
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON data successfully saved to {file_path}")
    except IOError as io_err:
        print(f"Error saving JSON data to {file_path}: {io_err}")


# Retrieve sessions based on room and number of event days
def get_sessions_by_room_and_days(file_path, target_room, event_days):
    data = load_data(file_path)

    # Extract all session dates and find the earliest one
    all_dates = [session["start"].split("T")[0] for session in data["sessions"]]
    earliest_date = min(all_dates)
    start_date = datetime.strptime(earliest_date, "%Y-%m-%d")

    # Create a 2D list to store sessions for each event day
    sessions_by_day = [[] for _ in range(event_days)]

    # Iterate over sessions and categorize by day
    for session in data["sessions"]:
        session_date = session["start"].split("T")[0]
        session_date_obj = datetime.strptime(session_date, "%Y-%m-%d")
        session_room = session["room"]

        # Only include sessions that match the target room
        if session_room == target_room:
            # Calculate which day the session belongs to
            day_index = (session_date_obj - start_date).days
            if 0 <= day_index < event_days:
                sessions_by_day[day_index].append(session)

    return sessions_by_day


# Display session information and time differences
def display_sessions(sessions_by_day):
    for day_index, sessions in enumerate(sessions_by_day, start=1):
        print(f"=== Day {day_index} Sessions ===")
        for session in sessions:
            start_time_str = session["start"].split("T")[1].split("+")[0]
            end_time_str = session["end"].split("T")[1].split("+")[0]
            time_difference = calculate_time_difference(start_time_str, end_time_str)

            # Output session information
            print(f"Room: {session['room']}")
            print(f"Date: {session['start'].split('T')[0]}")
            print(f"Start Time: {start_time_str}")
            print(f"End Time: {end_time_str}")
            print(f"Time Difference: {time_difference}")
            print(f"Title: {session['zh']['title']}")
            print("=" * 40)


def make_session():
    # Prompt for the year (default to 2024 if input is empty)
    year = input("Enter the year (default is 2024): ").strip() or "2024"

    # Construct the URL with the specified or default year
    url = f"https://coscup.org/{year}/json/session.json"
    file_path = "data.json"  # File to save or load JSON data

    # Check if the file exists
    if not Path(file_path).exists():
        print(f"{file_path} not found. Fetching data from {url}...")
        data = fetch_json_data(url)
        if data:
            save_json_to_file(data, file_path)
        else:
            print("Failed to fetch data. Exiting.")
            return

    # If the file exists or was just created, proceed to filter and display sessions
    target_room = input("Enter the room (default is TR213): ").strip() or "TR213"
    event_days = 2

    # Get session data
    sessions_by_day = get_sessions_by_room_and_days(file_path, target_room, event_days)

    return sessions_by_day


def main() -> None:
    """
    Main function to check if data.json exists; if not, fetch JSON data from URL,
    save it, and then proceed to filter sessions by room and display them.
    """
    # Prompt for the year (default to 2024 if input is empty)
    year = input("Enter the year (default is 2024): ").strip() or "2024"

    # Construct the URL with the specified or default year
    url = f"https://coscup.org/{year}/json/session.json"
    file_path = "data.json"  # File to save or load JSON data

    # Check if the file exists
    if not Path(file_path).exists():
        print(f"{file_path} not found. Fetching data from {url}...")
        data = fetch_json_data(url)
        if data:
            save_json_to_file(data, file_path)
        else:
            print("Failed to fetch data. Exiting.")
            return

    # If the file exists or was just created, proceed to filter and display sessions
    target_room = "TR213"
    event_days = 2

    # Get session data
    sessions_by_day = get_sessions_by_room_and_days(file_path, target_room, event_days)

    # Display session information
    display_sessions(sessions_by_day)


if __name__ == "__main__":
    main()
