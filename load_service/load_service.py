from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Dict, Any, Optional
import pandas as pd
import os
import uuid

app = FastAPI()

DATA_DIR = "./load_service/data"  # Directory to store loaded files
os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/load")
def load_data(
    file: UploadFile = File(...),
    batch_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Accepts a JSON file (transformed data), saves it to disk, and returns a confirmation with batch_id.
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported.")
    try:
        contents = file.file.read()
        df = pd.read_json(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    if batch_id is None:
        batch_id = str(uuid.uuid4())
    out_path = os.path.join(DATA_DIR, f"batch_{batch_id}.json")
    with open(out_path, "wb") as f:
        f.write(contents)
    return {"batch_id": batch_id, "rows_loaded": len(df), "file_path": out_path}

@app.get("/batches")
def list_batches() -> List[str]:
    """
    List all loaded batch files.
    """
    return [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

@app.get("/batch/{batch_id}")
def get_batch(batch_id: str) -> Any:
    """
    Retrieve the contents of a loaded batch by batch_id.
    """
    path = os.path.join(DATA_DIR, f"batch_{batch_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Batch not found.")
    with open(path, "r") as f:
        return pd.read_json(f.read()).to_dict(orient="records")
