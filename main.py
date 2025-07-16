from fastapi import FastAPI
from manager import ComplaintManager
from schemas import ComplaintCreate, ComplaintResponse
import uvicorn  # Импортируем uvicorn

app = FastAPI()
manager = ComplaintManager()

@app.post("/complaints/", response_model=ComplaintResponse)
async def create_complaint(complaint: ComplaintCreate):
    return await manager.create_complaint(complaint)

@app.get("/complaints/open/")
async def get_open_complaints(since: int):
    return await manager.get_open_complaints(since)
@app.get("/")
async def read_root():
    return {
        "message": "Complaint System API",
        "endpoints": {
            "create_complaint": "POST /complaints/",
            "get_open_complaints": "GET /complaints/open/?since=<timestamp>"
        }
    }
# Явный запуск сервера при выполнении файла

if __name__ == "__main__":
    import asyncio
    from database import Database


    async def test_db():
        db = Database()
        # Тест создания записи
        complaint_id = await db.insert_complaint("Тестовая жалоба")
        print(f"Создана запись с ID: {complaint_id}")

        # Тест чтения записи
        complaint = await db.get_complaint(complaint_id)
        print("Запись из БД:", complaint)


    asyncio.run(test_db())
    uvicorn.run(app, host="0.0.0.0", port=8000)