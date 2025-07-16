import asyncio
from manager import ComplaintManager
from schemas import ComplaintCreate

async def test_complaint_creation():
    manager = ComplaintManager()
    complaint = ComplaintCreate(text="Не приходит SMS-код")
    result = await manager.create_complaint(complaint)
    print("Test result:", result)

if __name__ == "__main__":
    asyncio.run(test_complaint_creation())