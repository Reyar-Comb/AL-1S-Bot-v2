import requests
from bs4 import BeautifulSoup


def request_comp():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://cubing.com/competition"
    response = requests.get(url, headers=headers)
    return response.text
    
def get_comp():
    answer = ""
    data = request_comp()
    soup = BeautifulSoup(data, features="html.parser")
    index = 0
    for row in soup.find_all("tr"):
        row_class = row.get("class", [])
        if "danger" in row_class:
            status = "报名中"
        elif "info" in row_class:
            status = "已截止"
        elif "active" in row_class:
            status = "已结束"
            continue
        else: 
            status = "wtf"
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if len(cols) > 0:
            if cols[1].endswith("秒"):
                cols[1] = cols[1][:-5]
            answer += f"{cols[0]} {status}\n{cols[1]}\n\n"
            index += 1
        if index >= 5:
            break
    return answer
if __name__ == "__main__":
    print(get_comp())