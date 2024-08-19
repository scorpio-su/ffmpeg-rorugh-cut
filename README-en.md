# FFmpeg Rough Cut

This script generates a batch of `ffmpeg` commands based on data provided in a CSV file, enabling quick and efficient video trimming. The script is designed to work on both Windows and Linux/macOS systems, allowing you to easily generate a series of commands for cutting, copying, and processing video files.

## Features

- **Cross-platform Support**: Automatically formats paths and filenames for Windows or Linux/macOS based on user input.
- **ASCII Encoding**: Ensures that the generated command files are compatible with systems that require ASCII encoding, such as older versions of Windows.
- **Automatic File Extension Handling**: Automatically appends `.mp4` to output filenames if not provided in the CSV.

## Requirements

- Python 3.x
- `ffmpeg` installed and available in your system's PATH.

## Installation

Clone this repository or download the script directly to your local machine:

```bash
git clone https://github.com//scorpio-su/ffmpeg-rough-cut.git
cd ffmpeg-rough-cut
```

Ensure you have the necessary dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare Your CSV File**

   Create a CSV file with the following columns:

   - `start time`: The start time of the clip (e.g., `0:26:08`).
   - `end time`: The end time of the clip (e.g., `0:45:48`).
   - `input file path`: The path to the input video file.
   - `output file path`: The directory where the output file should be saved.
   - `output file name`: The desired name of the output file (no need to include `.mp4`).

   Example `input_data.csv`:

   ```csv
   start time,end time,input file path,output file path,output file name
   0:26:08,0:45:48,TR514/514-1.mkv,TR514_OK_OK/,Day 1
   ```

2. **Run the Script**

   Run the script from the command line:

   ```bash
   python script.py
   ```

   The script will prompt you to specify your operating system (Windows or Linux/macOS). Based on your input, it will generate a batch file (`.bat` for Windows) or a shell script (`.sh` for Linux/macOS).

3. **Execute the Generated Script**

   After running the script, a command file (`ffmpeg_commands.bat` or `ffmpeg_commands.sh`) will be created in the same directory. You can execute this file to run all the `ffmpeg` commands in sequence.

   - On Windows:
     ```cmd
     ffmpeg_commands.bat
     ```
   - On Linux/macOS:
     ```bash
     bash ffmpeg_commands.sh
     ```

## Example

Here is an example CSV file and the corresponding output command:

**CSV File (`input_data.csv`):**

```csv
 start time,end time,input file path,output file path,output file name
 0:26:08,0:45:48,TR514/514-1.mkv,TR514_OK_OK/,Day 1
```

**Generated Command:**

```bash
ffmpeg -ss 0:26:08 -i "TR514/514-1.mkv" -to 0:45:48 -c copy -avoid_negative_ts 1 "TR514_OK_OK/Day 1.mp4"
```
