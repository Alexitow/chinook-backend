from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from supabase_client import supabase

app = FastAPI(title="Chinook Invoice Backend")

class InvoiceHeader(BaseModel):
    invoice_id: int
    customer_id: int
    invoice_date: str
    billing_address: str | None = None
    billing_city: str | None = None
    billing_state: str | None = None
    billing_country: str | None = None
    billing_postal_code: str | None = None
    total: float

@app.get("/customers")
def get_customers():
    try:
        response = supabase.table("customer").select("customer_id, first_name, last_name").order("customer_id").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/invoice")
def create_invoice(header: InvoiceHeader):
    try:
        data = header.model_dump()
        response = supabase.table("invoice").upsert(data, on_conflict="invoice_id").execute()
        return {"status": "ok", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/invoice/bulk")
def create_invoices_bulk(headers: list[InvoiceHeader]):
    try:
        data = [h.model_dump() for h in headers]
        response = supabase.table("invoice").upsert(data, on_conflict="invoice_id").execute()
        return {"status": "ok", "inserted": len(response.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))