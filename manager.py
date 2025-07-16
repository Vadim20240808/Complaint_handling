from database import Database
from integrations import SentimentAnalyzer, CategoryClassifier
from schemas import ComplaintCreate
import asyncio
import logging

logger = logging.getLogger(__name__)


class ComplaintManager:
    def __init__(self):
        self.db = Database()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.category_classifier = CategoryClassifier()
        logger.info("ComplaintManager initialized")

    async def create_complaint(self, complaint: ComplaintCreate) -> dict:
        logger.info(f"Creating complaint: {complaint.text[:50]}...")
        complaint_id = await self.db.insert_complaint(complaint.text)
        logger.info(f"Complaint created with ID: {complaint_id}")

        try:
            sentiment = await self.sentiment_analyzer.analyze(complaint.text)
            logger.info(f"Sentiment for {complaint_id}: {sentiment}")
            await self.db.update_sentiment(complaint_id, sentiment)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            await self.db.update_sentiment(complaint_id, "unknown")

        # Асинхронно определяем категорию
        asyncio.create_task(self._process_category(complaint_id, complaint.text))

        return await self.db.get_complaint(complaint_id)

    async def _process_category(self, complaint_id: int, text: str):
        try:
            category = await self.category_classifier.classify(text)
            logger.info(f"Category for {complaint_id}: {category}")
            await self.db.update_category(complaint_id, category)
        except Exception as e:
            logger.error(f"Category classification failed: {str(e)}")
            await self.db.update_category(complaint_id, "другое")

    async def get_open_complaints(self, since: int):
        # Реализация будет позже
        return []