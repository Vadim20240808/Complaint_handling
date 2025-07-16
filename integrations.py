import aiohttp
import os
from typing import Optional
import logging
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    async def analyze(self, text: str) -> str:
        try:
            # ... существующий код ...
            logger.info(f"Sentiment response: {data}")
        except Exception as e:
            logger.error(f"Sentiment error: {str(e)}")

class SentimentAnalyzer:
    async def analyze(self, text: str) -> str:
        url = "https://api.apilayer.com/sentiment/analysis"
        headers = {"apikey": os.getenv("SENTIMENT_API_KEY")}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json={"text": text}) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("sentiment", "unknown").lower()
        except Exception:
            pass
        return "unknown"


class CategoryClassifier:
    async def classify(self, text: str) -> str:
        # Реализация через OpenAI
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f'Определи категорию жалобы: "{text}". Варианты: техническая, оплата, другое. Ответ только одним словом.'
                }]
            )
            category = response.choices[0].message.content.strip().lower()
            return category if category in ["техническая", "оплата"] else "другое"
        except Exception:
            return "другое"


# точка входа
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()


    async def test_integrations():
        # Тест анализа тональности
        sentiment = await SentimentAnalyzer().analyze("У меня все работает прекрасно!")
        print("Sentiment:", sentiment)

        # Тест классификации категории
        category = await CategoryClassifier().classify("Не могу оплатить счет")
        print("Category:", category)


    asyncio.run(test_integrations())