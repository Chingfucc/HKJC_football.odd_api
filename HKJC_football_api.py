# author: chingfucc

# source
# 1. visualize unstructured data
# https://bet.hkjc.com/football/getJSON.aspx?jsontype=search_result.aspx&startdate=20191013&enddate=20191014&teamid=default
# 2. source code: https://github.com/tanjt107/hkjc-football-api/blob/main/example.py

import json
import math
import pandas as pd
import requests
from datetime import date

start_date = "2003-01-01"
end_date = date.today()

month_starts = pd.date_range(start=start_date, end=end_date, freq="MS")
month_ends = pd.date_range(start=start_date, end=end_date, freq="M")

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

matches = []
for month_end, month_start in zip(month_ends, month_starts):
    try:
        response = session.post(
            "https://bet.hkjc.com/football/getJSON.aspx",
            headers=headers,
            params={
                "jsontype": "search_result.aspx",
                "startdate": month_start.strftime("%Y%m%d"),
                "enddate": month_end.strftime("%Y%m%d"),
                "pageno": 1,
            },
        )
        try:
            if text := json.loads(response.text):
                data = text[0]
            else:
                continue
        except json.JSONDecodeError:
            continue
        matchescount = data["matchescount"]
        print(month_end)
        print("################################################################")
    
        for page in range(1, math.ceil(int(matchescount) / 20) + 1):
            response = session.post(
                "https://bet.hkjc.com/football/getJSON.aspx",
                headers=headers,
                params={
                    "jsontype": "search_result.aspx",
                    "startdate": month_start.strftime("%Y%m%d"),
                    "enddate": month_end.strftime("%Y%m%d"),
                    "pageno": page,
                },
            )
            try:
                if text := json.loads(response.text):
                    data = text[0]
            except json.JSONDecodeError:
                continue
    
            matches.extend(data["matches"])
            print("page")
            print(page)
            print("finished")
    except json.JSONDecodeError:
        continue

df = pd.DataFrame(matches)
df.to_csv("matches_add.csv", index=False, encoding="utf-8_sig")


