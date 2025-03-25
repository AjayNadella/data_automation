from ingestors.email_ingestor import load_email_from_file
from processors.llm_extractor import extract_fields
from writers.csv_writer import write_to_csv
from ingestors.pdf_ingestor import extract_text_from_pdf
import json


if __name__ == '__main__':
    source = input("Choose input type (email/pdf): ").strip().lower()

    if source == 'email':
        text = load_email_from_file("../backend/ingestors/sample_email.eml")
    if source == 'pdf':
        text = extract_text_from_pdf("../backend/ingestors/sample_ticket.pdf")
    else:
        print("Invalid input type.")
        exit()

    print("\nExtracting with LLaMA...")
    prompt_template = open("prompts/support_email_prompt.txt").read()
    extracted = extract_fields(text, prompt_template)

    print("\nStructured Output:\n", extracted)

    structured_data = json.loads(extracted)
    write_to_csv(structured_data, "output.csv")

    print("\n✅ Data written to output.csv")
