# С помощью pytest необходимо написать тест, который просит ввести в консоли любую фразу короче 15 символов. А затем с
# помощью assert проверяет, что фраза действительно короче 15 символов.

class TestExample:
    def test_length_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15, f"Длина фразы более 15 символов"
