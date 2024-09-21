# import requests
# from bs4 import BeautifulSoup


# def fetch_schedule(day):
#     # 请求网页
#     url = "https://coscup.org/2024/zh-TW/session"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     # print(soup)
#     # 输出找到的内容

#     # 找到所有 class 为 'schedule-item' 的 <a> 元素
#     schedule_items = soup.find_all("a", class_="schedule-item")

#     if schedule_items:
#         print("找到以下議程：")
#         for item in schedule_items:
#             # 在每個 schedule-item 中尋找 class 為 'title' 的元素
#             title = item.find("div", class_="title")
#             if title:
#                 print(title.get_text(strip=True))
#             else:
#                 print("此項目沒有標題")
#     else:
#         print("未找到任何議程項目")

#     # 將找到的議程標題保存到文件
#     with open("list.txt", "w", encoding="utf-8") as file:
#         for item in schedule_items:
#             title = item.find("div", class_="title")
#             if title:
#                 file.write(title.get_text(strip=True) + "\n")

#     if day == 1:
#         print("Day 1 議程已保存到 list.txt")
#     elif day == 2:
#         print("Day 2 議程已保存到 list.txt")
#     else:
#         print("無效的輸入。請輸入 1 或 2。")
#     # print("Soup content has been saved to coscup_schedule.html")
#     # # 根据用户选择Day1或Day2
#     # if day == 1:
#     #     schedule_list = soup.find(
#     #         "ul",
#     #         class_="schedule-list",
#     #         style=lambda x: x is None or "display" not in x,
#     #     )
#     # elif day == 2:
#     #     schedule_list = soup.find("ul", class_="schedule-list", style="display: none;")
#     # else:
#     #     print("Invalid input. Please enter 1 or 2.")
#     #     return
#     # print(schedule_list)
#     # if schedule_list:
#     #     # 提取议程标题
#     #     titles = schedule_list.find_all(
#     #         "h2", class_="title"
#     #     )  # 寻找所有 <h2 class="title"> 标签

#     #     for i, title in enumerate(titles, start=1):
#     #         print(f"Session {i}: {title.get_text(strip=True)}")
#     # else:
#     #     print(f"Could not find the schedule for Day {day}")


# # 获取用户输入
# day = int(input("请输入你要查询的天数 (1 或 2): "))
# fetch_schedule(day)

import json
from datetime import datetime


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


def main():
    # Example usage
    file_path = "./data.json"
    target_room = "TR213"
    event_days = 2

    # Get session data
    sessions_by_day = get_sessions_by_room_and_days(file_path, target_room, event_days)

    # Display session information
    display_sessions(sessions_by_day)


if __name__ == "__main__":
    main()
