import csv
import os


def generate_ffmpeg_command(start_time, end_time, input_file, output_file):
    """
    Generate the ffmpeg command based on the given parameters.
    """
    return (
        f'ffmpeg -ss {start_time} -i "{input_file}" '
        f"-to {end_time} -c copy -avoid_negative_ts 1 "
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


# Example usage
if __name__ == "__main__":
    csv_file = "input_data.csv"  # Path to your CSV file

    # Ask the user for their operating system
    is_windows = ask_user_for_os()

    # Set the output script file based on the operating system
    output_script_file = "ffmpeg_commands.bat" if is_windows else "ffmpeg_commands.sh"

    generate_ffmpeg_commands_from_csv(csv_file, output_script_file, is_windows)
