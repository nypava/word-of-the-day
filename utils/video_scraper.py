from bs4 import BeautifulSoup
import requests
import re
import os

class VideoScraper:
    url = "https://yarn.co/yarn-find?text="

    def __init__(self) -> None:
        pass

    def _scrap_videos(self, word:str) -> list:
        soups = []
        videos_list = []
        
        for page in range(2):
            response = requests.get(f"{self.url} + '{word}&p={page}" ) 
            soups.append(BeautifulSoup(response.text, "html.parser"))
        
        for soup in soups:
            for video_div in soup.find_all("div", "clip bg-t rel nomob"):
                video_subtitle = video_div.div.find_all("a")[-1].div.string

                if word.lower() not in video_subtitle.lower():
                    continue
                
                video_id = video_div.div.a["href"].split("/")[-1]
                video_length = "".join(re.findall(r"\d+[.]\d+|\d+", str(video_div.div.a.div.find("div", "play-time ab fwb").contents[-1])))

                videos_list.append({"video_id": video_id, 
                                "video_length": video_length, 
                                "video_subtitle": video_subtitle})

        videos_list.sort(key=lambda video: video["video_length"])

        if len(videos_list) >= 6:
            return videos_list[-6:]
        
        return videos_list

    def get_videos(self, word:str) -> list[dict]:
        return self._scrap_videos(word)
    
    @staticmethod
    def cache_clr(dir) -> None:
        for file in os.listdir(dir):
            file_path = os.path.join(dir, file)
            os.remove(file_path)
        
    def download(self, dir, videos_list) -> None:
        for video in videos_list:
            if not os.path.exists(os.path.join(dir, f"{video['video_id']}.mp4")):
                continue

            with requests.get(f"https://y.yarn.co/{video['video_id']}.mp4") as response:
                with open(os.path.join(dir, f"{video['video_id']}.mp4"), "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
