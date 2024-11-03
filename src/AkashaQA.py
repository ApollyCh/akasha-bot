from .data.faiss_db import FaissDB
from .data.genshin_data import GenshinData
from .model.generator import AnswerGenerator
from .model.cache_manager import CacheManager

characters_data = "src/data/json/characters_data.json"
lore_data = "src/data/json/lore_data.json"


class AkashaQA:
    def __init__(self):
        self.genshin_data = GenshinData(characters_data, lore_data)
        self.faiss_db = FaissDB("mixedbread-ai/mxbai-embed-large-v1", 512)
        self.generator = AnswerGenerator()
        self.cache = CacheManager()

        all_chunks = self.genshin_data.get_all_chunks()
        self.faiss_db.add_documents(all_chunks)

    def get_answer(self, question):
        cached_answer = self.cache.get(question)
        if cached_answer:
            return cached_answer

        context = " ".join(self.faiss_db.search(question))
        answer = self.generator.generate(question, context)

        self.cache.set(question, answer)
        return answer
