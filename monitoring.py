import time
import asyncio
import aiohttp
import os
from typing import Dict, Optional


class APIMonitor:
    def __init__(self):
        self.usage: Dict[str, Dict[str, int]] = {
            "sentiment": {"used": 0, "limit": 100, "reset_timestamp": 0},
            "openai": {"used": 0, "limit": 1000, "reset_timestamp": 0}
        }
        self.last_checked = 0
        self.update_interval = 3600  # Проверять каждый час

    def increment(self, api_name: str):
        """Увеличивает счетчик использования API"""
        if api_name in self.usage:
            self.usage[api_name]["used"] += 1

    async def check_limits(self):
        """Проверяет текущее использование API (асинхронно)"""
        current_time = time.time()
        if current_time - self.last_checked < self.update_interval:
            return

        self.last_checked = current_time
        await self._update_sentiment_limits()
        await self._update_openai_limits()

    async def _update_sentiment_limits(self):
        """Обновляет данные по квотам APILayer"""
        url = "https://api.apilayer.com/usage"
        headers = {"apikey": os.getenv("SENTIMENT_API_KEY")}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.usage["sentiment"]["used"] = data.get("used", 0)
                        self.usage["sentiment"]["limit"] = data.get("limit", 100)
                        self.usage["sentiment"]["reset_timestamp"] = data.get("reset_timestamp", 0)
        except Exception as e:
            print(f"Failed to update sentiment limits: {str(e)}")

    async def _update_openai_limits(self):
        """Обновляет данные по квотам OpenAI"""
        import openai
        try:
            usage = await openai.Usage.acreate()
            self.usage["openai"]["used"] = usage.get("total_usage", 0) / 1000  # Переводим в доллары
            # Для OpenAI лимит обычно в деньгах, возьмем из переменных окружения
            self.usage["openai"]["limit"] = float(os.getenv("OPENAI_LIMIT", 10.0))  # $10 по умолчанию
        except Exception as e:
            print(f"Failed to update OpenAI limits: {str(e)}")

    def get_status(self, api_name: str) -> Dict[str, str]:
        """Возвращает статус использования API"""
        if api_name not in self.usage:
            return {"error": "Unknown API"}

        data = self.usage[api_name]
        used = data["used"]
        limit = data["limit"]
        percentage = (used / limit) * 100 if limit > 0 else 0

        status = "OK"
        if percentage > 80:
            status = "WARNING"
        elif percentage >= 100:
            status = "LIMIT EXCEEDED"

        reset_time = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(data["reset_timestamp"])
        ) if data["reset_timestamp"] else "N/A"

        return {
            "used": used,
            "limit": limit,
            "percentage": f"{percentage:.1f}%",
            "status": status,
            "reset_time": reset_time
        }


# Глобальный экземпляр монитора
monitor = APIMonitor()