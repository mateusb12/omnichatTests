import pytest

from omnichatTests.classes.order_handler import parsePizzaOrder, convertMultiplePizzaOrderToText, buildFullOrder
from omnichatTests.classes.drink_order_extractor import DrinkOrderExtractor


class TestOrderProcessing:

    @classmethod
    def setUpClass(cls):
        cls.processor = DrinkOrderExtractor()

    def test_extractOrderWithWordQuantities(self):
        userMessage = 'duas cocas e dois guaranás'
        expected_output = {'coca-cola': 2.0, 'guaraná': 2.0}
        assert self.processor.extractDrinkOrder(userMessage) == expected_output

    def test_extractOrderWithNumericQuantities(self):
        userMessage = '3 coca e 4 guarana'
        expected_output = {'coca-cola': 3.0, 'guaraná': 4.0}
        assert self.processor.extractDrinkOrder(userMessage) == expected_output

    def test_extractOrderWithBeverageSynonyms(self):
        userMessage = '3 coca cola 2L'
        expected_output = {'coca-cola': 3.0}
        assert self.processor.extractDrinkOrder(userMessage) == expected_output

    def test_parsePizzaOrder(self):
        parameterInput = {'flavor': ['calabresa', 'margherita', 'quatro queijos'], 'number': [1.0]}
        userMessage = 'vou querer duas calabresas e uma pizza meio margherita meio quatro queijos'
        expected_output = [{'calabresa': 2.0}, {'margherita': 0.5, 'queijo': 0.5}]
        assert parsePizzaOrder(userMessage, parameterInput) == expected_output

    def test_convertMultiplePizzaOrderToText(self):
        pizzaOrder = [{'frango': 3.0}, {'calabresa': 0.5, 'margherita': 0.5}, {'calabresa': 1.0}]
        expected_output = 'três inteiras frango, meia calabresa meia margherita, uma inteira calabresa'
        assert convertMultiplePizzaOrderToText(pizzaOrder) == expected_output

    def test_buildFullOrder(self):
        orderTest = {'drinks': [{"suco de laranja": 1.0}], 'pizzas': [[{'calabresa': 1.0}]],
                     'secret': 'Mensagem secreta'}
        expected_output = {'Bebida': [{'suco de laranja': 1.0}], 'Pizza': {'calabresa': 1.0}}
        assert buildFullOrder(orderTest) == expected_output
