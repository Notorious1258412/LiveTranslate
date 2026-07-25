from translator.nllb_engine import NLLBTranslator


translator = NLLBTranslator()


text = """
Welcome to today's live stream.
This is a test translation.
"""


result = translator.translate(text)


print("翻譯:")
print(result)