from fastapi import FastAPI, UploadFile, File, HTTPException,Form
from fastapi.middleware.cors import CORSMiddleware
from ingestors.email_ingestor import load_email_from_file
from ingestors.pdf_ingestor import extract_text_from_pdf
from processors.llm_extractor import extract_fields
from writers.csv_writer import write_to_csv
from ingestors.imap_email_fetcher import fetch_all_unread_email_texts
from typing import Optional
import json
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract/emails/bulk")
async def extract_filtered_emails_from_imap(
    email_user: str = Form(...),
    email_pass: str = Form(...),
    fields_to_extract: str = Form(...),
    imap_host: Optional[str] = Form("imap.gmail.com")
):
    try:
        email_texts = fetch_all_unread_email_texts(imap_host, email_user, email_pass)
        if not email_texts:
            return {"status": "no_emails_found", "data": []}

        extracted_results = []

        for idx, text in enumerate(email_texts):
            full_prompt = (
                "You are a smart extractor. Only extract data if the email is relevant to the user's intent.\n"
                f"Email:\n{text}\n\n"
                f"Intent: Extract data only from emails like this:\n{fields_to_extract}\n\n"
                "Respond ONLY with a JSON object. If the email is irrelevant, respond with: null"
            )

            try:
                output = extract_fields(text, full_prompt).strip()

                if output.lower().startswith("null") or output.strip() == "":
                    continue  

                structured_data = json.loads(output)
                write_to_csv(structured_data, "output.csv")
                extracted_results.append(structured_data)

            except Exception as e:
                print(f"[Email {idx}] Skipped due to error: {e}")
                continue

        return {
            "status": "success",
            "processed": len(email_texts),
            "extracted": len(extracted_results),
            "data": extracted_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract/pdf")
async def extract_from_pdf(file: UploadFile = File(...),fields_to_extract: str = Form(...),):
    try:
        filepath = f"temp_{file.filename}"
        with open(filepath, "wb") as f:
            f.write(await file.read())

        pdf_text = extract_text_from_pdf(filepath)
        
        full_prompt = (
            "You are an AI assistant that extracts structured data from unstructured documents.\n"
            f"Document:\n{pdf_text}\n\n"
            f"Extract the following fields and return as JSON:\n{fields_to_extract}"
        )
        extracted = extract_fields(pdf_text, full_prompt)
        structured_data = json.loads(extracted)
        write_to_csv(structured_data, "output.csv")

        os.remove(filepath)
        return {"status": "success", "data": structured_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
