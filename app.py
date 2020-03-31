from dhooks import Webhook, Embed
import cloudscraper
from bs4 import BeautifulSoup as bs
import json
import datetime
import time

old = ""
hook = Webhook("https://discordapp.com/api/webhooks/694383657636593706/puT4e94YhHvFI2bVGkytmfQkdoOG8AHVkY0PgPO6D4914cLtJb7sHdldLZR-Fyv7Xveu")
scraper = cloudscraper.create_scraper()

headers = {
    "user-agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
}

def monitor():
    datas = []
    r = scraper.get("https://www.youtube.com/channel/UC7V18bBk4EGwmxf114i1w6Q/videos", headers=headers)
    soup = bs(r.text, "html.parser")
    videos = soup.find('div', id="initial-data")
    text = str(videos).split("<div id=\"initial-data\"><!-- ")[1]
    text = text.split(" --></div>")[0]
    data = json.loads(text)
    json_formatted_str = json.dumps(data, indent=2)
    videos = data['contents']['singleColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

    for video in videos:
        base = "https://www.youtube.com/watch?v="
        thumbnail = ""
        id = ""
        url = ""
        title = ""
        vid = video['compactVideoRenderer']
        id = str(vid['videoId'])
        thumbs = vid['thumbnail']['thumbnails']
        for thumb in thumbs:
            thumbnail = str(thumb['url'])
        title = vid['title']['runs'][0]['text']
        url = base + id
        ts = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
        print(f"[{ts}] - Title: " + title)
        print(f"[{ts}] - Thumbnail: " + thumbnail)
        print(f"[{ts}] - URL: " + url)
        video = [str(title), str(url), str(thumbnail)]
        datas.append(video)
    return datas

def send(title, url, thumb):
    embed = Embed(title=title, url=url, color=0xEFFF26)
    embed.set_image(url=thumb)
    embed.set_footer(text="connorstevens#0001 for Jeeshmoji")
    return embed

while(True):
    das = monitor()
    if das[0] == old:
        pass
    else:
        ts = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        print(f"[{ts}] - Sending {das[0]}")
        hook.send(embed=send(das[0][0], das[0][1], das[0][2]))
        hook.send(content="@everyone, New BotterBoyNova Video Detected!")
        old = das[0]
    time.sleep(30)