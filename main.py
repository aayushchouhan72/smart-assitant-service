from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_service.rag import llm_search, get_context

app = FastAPI()


class QueryRequest(BaseModel):
    text: str
    query: str


@app.post("/chat")
def chat(data: QueryRequest):

    try:

        # Validation
        if not data.text.strip():
            raise ValueError("Text cannot be empty.")

        if not data.query.strip():
            raise ValueError("Query cannot be empty.")

        # Retrieve context
        context = get_context(
            query=data.query,
            text=data.text
        )

        # Generate answer
        res = llm_search(context)

        return {
            "success": True,
            "answer": res.content
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Server Error: {str(e)}"
        )