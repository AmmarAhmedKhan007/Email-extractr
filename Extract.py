import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO
import re
import pandas as pd

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    # Create a file-like object from the uploaded file
    pdf_stream = BytesIO(pdf_file.read())
    with fitz.open(stream=pdf_stream, filetype="pdf") as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

# Function to extract emails from text
def extract_emails(text):
    # Regular expression for matching email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails

# Function to convert emails to CSV format
def emails_to_csv(emails):
    df = pd.DataFrame(emails, columns=["Email"])
    csv = df.to_csv(index=False)
    return csv

# Streamlit app
def main():
    st.title("PDF Email Extractor")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("Processing PDF...")
        text = extract_text_from_pdf(uploaded_file)
        emails = extract_emails(text)
        
        # Convert emails to CSV
        csv = emails_to_csv(emails)
        
        # Download button
        st.download_button(
            label="Download Emails as CSV",
            data=csv,
            file_name='emails.csv',
            mime='text/csv'
        )
        
        st.subheader("Extracted Emails")
        if emails:
            # Display emails
            st.write("Here are the emails extracted from the PDF:")
            for email in emails:
                st.write(email)
        else:
            st.write("No emails found.")

if __name__ == "__main__":
    main()
