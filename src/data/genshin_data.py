from .characters import ALL_MAIN_CHARACTERS
import re
from bs4 import BeautifulSoup
import requests
import json
import fitz


class GenshinData:

    def __init__(self, path_char_data=None, path_lore_data=None):

        if path_char_data is not None:
            with open(path_char_data, "r") as file:
                self.personal_data = json.load(file)
        else:
            self.personal_data = self.charachers_data()

        if path_lore_data is not None:
            with open(path_lore_data, "r") as file:
                self.lore_data = json.load(file)

        else:
            self.lore_data = self.get_lore_data("./pdf/Genshin Impact_ A full story.pdf")

    def parse_character_name(self, name: str):
        url = f"https://genshin-impact.fandom.com/wiki/{name}/Lore"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            lore_section = soup.find("div", {"class": "mw-parser-output"})
            if lore_section is None:
                return f"Character {name} not found"

            paragraphs = lore_section.find_all("p")
            paragraph_chunks = [paragraph.text.strip() for paragraph in paragraphs if
                                paragraph.text.strip() and not paragraph.text.strip().startswith("Friendship Lv.")]

            return paragraph_chunks

        except Exception as e:
            return f"Error during character lore parsing: {str(e)}"

    def charachers_data(self):
        all_data = {}
        for character in ALL_MAIN_CHARACTERS:
            print(f"Processing character: {character}")

            chunks = self.parse_character_name(character)

            if f"Character {character} not found" in chunks:
                return "Cannot find all characters"

            all_data[character] = chunks
        return all_data

    def save_data(self, path, data):
        with open(path, "w") as file:
            json.dump(data, file)

    def get_lore_data(self, pdf_path):
        doc = fitz.open(pdf_path)
        page_chunks = {}

        for page_num in range(doc.page_count):
            page = doc[page_num]
            text = page.get_text("text")

            text = re.sub(r'[•○◦■●]', '', text)

            page_chunks[f"Page {page_num + 1}"] = text.strip()

        doc.close()

        return page_chunks

    def get_all_chunks(self) -> list:
        all_chunks = []
        for character in self.personal_data:
            all_chunks.extend(self.personal_data[character])

        all_chunks.extend(self.lore_data.values())

        return all_chunks


if __name__ == "__main__":
    genshin_data = GenshinData()

    genshin_data.save_data("./json/characters_data.json", genshin_data.personal_data)

    genshin_data.save_data("./json/lore_data.json", genshin_data.lore_data)

    print("Data saved successfully")
    print(genshin_data.get_all_chunks())
