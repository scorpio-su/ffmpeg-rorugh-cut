import csv
import os
import pandas as pd
from typing import List
from room import make_session


def create_dataframe(output_file_names: List[str]) -> pd.DataFrame:
    """
    Create a DataFrame with the specified output file names.
    All other fields will be left blank.

    :param output_file_names: List of output file names
    :return: DataFrame with the required headers and data
    """
    data = {
        "start time": [""] * len(output_file_names),
        "end time": [""] * len(output_file_names),
        "input file path": [""] * len(output_file_names),
        "output file path": [""] * len(output_file_names),
        "output file name": output_file_names,
    }
    return pd.DataFrame(data)


def save_dataframe_to_csv(df: pd.DataFrame, csv_file_path: str) -> None:
    """
    Save the given DataFrame to a CSV file.

    :param df: DataFrame to be saved
    :param csv_file_path: Path where the CSV file will be saved
    """
    df.to_csv(csv_file_path, index=False)


def generate_csv_file(output_file_names: List[str], csv_file_path: str) -> None:
    """
    Generate a CSV file based on the provided list of output file names.

    :param output_file_names: List of output file names
    :param csv_file_path: Path where the CSV file will be saved
    """
    df = create_dataframe(output_file_names)  # Create the DataFrame
    save_dataframe_to_csv(df, csv_file_path)  # Save it as a CSV file


def generate_ffmpeg_command(start_time, end_time, input_file, output_file):
    """
    Generate the ffmpeg command based on the given parameters.
    """
    return (
        f'ffmpeg -ss {start_time} -to {end_time} -i "{input_file}" '
        f"-c copy -avoid_negative_ts 1 "
        f'"{output_file}"\n'
    )


def process_csv_row(row, is_windows):
    """
    Process each row of the CSV file to generate an ffmpeg command.
    """
    start_time = row["start time"]
    end_time = row["end time"]
    input_file = row["input file path"]
    output_file_path = row["output file path"]
    output_file_name = row["output file name"]

    # Automatically append .mp4 to the output file name if not present
    if not output_file_name.endswith(".mp4"):
        output_file_name += ".mp4"

    # Handle file path formatting for Windows or Linux
    if is_windows:
        output_file = os.path.join(output_file_path, output_file_name).replace(
            "/", "\\"
        )
    else:
        output_file = os.path.join(output_file_path, output_file_name).replace(
            "\\", "/"
        )

    return generate_ffmpeg_command(start_time, end_time, input_file, output_file)


def generate_ffmpeg_commands_from_csv(csv_file, output_script_file, is_windows=True):
    """
    Read data from the CSV file and generate an ffmpeg commands file.
    Save the file in ASCII encoding for compatibility with Windows.
    """
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        with open(
            output_script_file, "w", encoding="utf-8", errors="replace"
        ) as script:
            for row in reader:
                ffmpeg_command = process_csv_row(row, is_windows)
                script.write(ffmpeg_command)

    print(f"The ffmpeg commands have been saved to {output_script_file}")


def ask_user_for_os():
    """
    Ask the user if they are using Windows or Linux/macOS.
    """
    while True:
        user_input = (
            input("Are you using Windows or Linux/macOS? (w/l): ").strip().lower()
        )
        if user_input == "w":
            return True
        elif user_input == "l":
            return False
        else:
            print("Invalid input. Please enter 'w' for Windows or 'l' for Linux/macOS.")


def main():
    csv_file = "input_data.csv"  # Path to your CSV file

    # Ask the user for their operating system
    is_windows = ask_user_for_os()

    # Set the output script file based on the operating system
    output_script_file = "ffmpeg_commands.bat" if is_windows else "ffmpeg_commands.sh"

    generate_ffmpeg_commands_from_csv(csv_file, output_script_file, is_windows)


def main2():
    # Get session data
    sessions_by_day = make_session()
    output_file_names = []
    for _, sessions in enumerate(sessions_by_day, start=1):
        for session in sessions:
            output_file_names.append(session["zh"]["title"])
    # print(output_file_names, len(output_file_names))

    csv_file_path = "input_data.csv"

    generate_csv_file(output_file_names, csv_file_path)


# Example usage
if __name__ == "__main__":
    if 0:
        main()
    else:
        main2()
