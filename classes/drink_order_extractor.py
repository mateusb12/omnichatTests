import spacy
from spacy.matcher import Matcher
from fuzzywuzzy import process
from constants import NUMERAL_MAP, DRINK_MAP


class DrinkOrderExtractor:
    def __init__(self):

        self.nlp = spacy.load("pt_core_news_sm")
        self.matcher = Matcher(self.nlp.vocab)

        patterns = [
            [{"LOWER": {
                "IN": ["um", "uma", "dois", "duas", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]},
              "OP": "?"}, {"LIKE_NUM": True, "OP": "?"}, {"LOWER": {"REGEX": "^coca.*"}}],
            [{"LOWER": {
                "IN": ["um", "uma", "dois", "duas", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]},
              "OP": "?"}, {"LIKE_NUM": True, "OP": "?"}, {"LOWER": {"REGEX": "^guaran.*"}}]
        ]

        self.matcher.add("DRINK_PATTERN", patterns)

    def extractDrinkOrder(self, userMessage: str) -> dict:
        doc = self.nlp(userMessage)
        matches = self.matcher(doc)
        order = {}

        for match_id, start, end in matches:
            span = doc[start:end]
            if len(span) < 2:
                continue
            num = span[0].text
            drink = span[1].text
            print(span, num, drink)
            drink = self.__closest_match(drink, DRINK_MAP)

            quantity = int(num) if num.isdigit() else self.__closest_match(num, NUMERAL_MAP)

            if drink in list(DRINK_MAP.keys()):
                order[drink] = quantity
        return order

    @staticmethod
    def __closest_match(word: str, choices) -> str | None:
        """Retorna a escolha mais próxima da palavra, se a pontuação for alta o suficiente."""
        best_match, score = process.extractOne(word, choices.keys())
        # print(word, best_match, score)
        if score > 70:  # Você pode ajustar esse limite conforme necessário
            if choices == NUMERAL_MAP:
                return choices[best_match]
            return best_match
        return None
