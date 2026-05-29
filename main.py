from fastapi import FastAPI

app = FastAPI()

@app.post("/chat")

def chat(data:dict):

    prompt=data.get("message")

    return {
        "answer":f"AI says: {prompt}"
    }