import requests
from bs4 import BeautifulSoup


def fetch_schedule(day):
    # 请求网页
    url = "https://coscup.org/2024/zh-TW/session"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    # 输出找到的内容

    # 找到 class 为 'main-container' 的 <div> 元素
    main_container = soup.find("div", class_="main-container")

    # 如果找到该元素，则在其中进一步查找 <ul class="schedule-list" style="display: none;">
    if main_container:
        schedule_list_hidden = soup.find_all("a", class_="schedule-item")
        if schedule_list_hidden:
            print(schedule_list_hidden)
        else:
            print("未找到 <ul class='schedule-list' style='display: none;'> 元素")
    else:
        print("未找到 <div class='main-container'> 元素")
    # 将soup内容保存到文件
    with open("list.txt", "w", encoding="utf-8") as file:
        file.write(schedule_list_hidden)

    # print("Soup content has been saved to coscup_schedule.html")
    # # 根据用户选择Day1或Day2
    # if day == 1:
    #     schedule_list = soup.find(
    #         "ul",
    #         class_="schedule-list",
    #         style=lambda x: x is None or "display" not in x,
    #     )
    # elif day == 2:
    #     schedule_list = soup.find("ul", class_="schedule-list", style="display: none;")
    # else:
    #     print("Invalid input. Please enter 1 or 2.")
    #     return
    # print(schedule_list)
    # if schedule_list:
    #     # 提取议程标题
    #     titles = schedule_list.find_all(
    #         "h2", class_="title"
    #     )  # 寻找所有 <h2 class="title"> 标签

    #     for i, title in enumerate(titles, start=1):
    #         print(f"Session {i}: {title.get_text(strip=True)}")
    # else:
    #     print(f"Could not find the schedule for Day {day}")


# 获取用户输入
day = int(input("请输入你要查询的天数 (1 或 2): "))
fetch_schedule(day)
