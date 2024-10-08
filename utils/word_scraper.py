import requests
from bs4 import BeautifulSoup

class WordScraper:
    def __init__(self):
        self.MAIN_URL = "https://www.merriam-webster.com/word-of-the-day"
        self.AUDIO_URL = "https://rss.art19.com/episodes/"

    def scrape_data(self):
        response = requests.get(self.MAIN_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        word_element = soup.find(class_="word-header-txt")
        self.word = word_element.get_text(strip=True)

        meaning_element = soup.find("p")
        self.meaning = meaning_element.get_text(" ", strip=True)

        example_elements = soup.find_all("p")[1:]
        self.example = ""
        for example_element in example_elements:
            if example_element.get_text(strip=True) == "See the entry >":
                break
            self.example += "\n" + example_element.get_text(" ", strip=True)

        pronunciation_element = soup.find(class_="word-attributes")
        self.pronunciation = pronunciation_element.get_text(" | ", strip=True)

        context_element = soup.find(class_="left-content-box")
        self.context = context_element.get_text(" ", strip=True)

        facts_elements = soup.find(class_="did-you-know-wrapper")
        facts_element = facts_elements.find("p")
        self.facts = facts_element.get_text(" ", strip=True,)

        audio_id = soup.find(id="art19-podcast-player")["data-episode-id"]
        self.podcast = self.AUDIO_URL + audio_id + ".mp3"

    def generate(self):
        self.scrape_data()

        scraped_data = {
            "word": self.word,
            "pronunciation": self.pronunciation,
            "meaning": self.meaning,
            "example": self.example,
            "context": self.context,
            "facts": self.facts,
            "podcast": self.podcast
        }

        return scraped_data
