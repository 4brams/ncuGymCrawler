import csv
import io
import logging
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import requests

SOURCE_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTi7PeVb_4bE22ioWlIMlYwoaDbOQiq7fdn3VRAmS_5V60_9cmTh3P8e97jfvT5X867teqRsMoGY_Ou/"
    "pub?gid=0&single=true&output=csv"
)

OUTPUT_FILE = "/app/data/occupancy.csv"
TIMEZONE = ZoneInfo("Asia/Taipei")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def fetch_data():
    response = requests.get(
        SOURCE_URL,
        timeout=20,
        headers={"User-Agent": "GymOccupancyCollector/1.0"},
    )
    response.raise_for_status()

    # 避免把登入頁面或錯誤頁面當成 CSV
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type.lower():
        raise ValueError("取得的是 HTML，不是預期的 CSV")

    text = response.content.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))

    if not rows:
        raise ValueError("試算表沒有資料")

    return rows


def collect():
    timestamp = datetime.now(TIMEZONE).isoformat(timespec="seconds")

    try:
        rows = fetch_data()
        # print(rows)

        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        file_exists = os.path.exists(OUTPUT_FILE)

        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)

            if not file_exists or os.path.getsize(OUTPUT_FILE) == 0:
                writer.writerow(["timestamp", "num_of_people"])

            b = rows[1][1] if len(rows[1]) > 1 else ""

            writer.writerow([timestamp, b])

        logging.info("抓取成功，共取得 %d 列", len(rows))

    except Exception:
        logging.exception("抓取失敗")


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Taipei")

    # 每小時的第 10 分與第 40 分執行
    scheduler.add_job(
        collect,
        CronTrigger(minute="10,40", timezone="Asia/Taipei"),
        id="gym_occupancy",
        max_instances=1,
        coalesce=True,
    )

    # 啟動時先抓取一次（可選）
    # collect()

    scheduler.start()
