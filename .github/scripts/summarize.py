
import os
import sys
import datetime
import pathlib
import google.generativeai as genai

def create_summary(paper_path):
    """
    Generates a blog post with summaries of a research paper for different audiences.

    Args:
        paper_path (str): The path to the PDF file of the research paper.
    """
    paper_name = pathlib.Path(paper_path).stem
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    post_path = f"_posts/{current_date}-{paper_name}.markdown"

    # --- API Configuration ---
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # --- File Reading ---
    print(f"Reading paper: {paper_path}")
    pdf_file = genai.upload_file(path=paper_path)
    print(f"Completed uploading file: {pdf_file.name}")


    # --- Advanced Summary Generation ---
    advanced_prompt = "Summarize this research paper for university/college level students, focusing on key concepts, methodologies, and findings:"
    advanced_summary_response = model.generate_content([advanced_prompt, pdf_file])
    advanced_summary = advanced_summary_response.text
    print("Advanced Summary Generated.")

    # --- High School Summary Generation ---
    high_school_prompt = f"Based on the following advanced summary, create a summary suitable for high school students. Simplify complex terms and focus on the main ideas and implications: Advanced Summary: {advanced_summary}"
    high_school_summary_response = model.generate_content([high_school_prompt, pdf_file])
    high_school_summary = high_school_summary_response.text
    print("High School Summary Generated.")

    # --- Child Summary Generation ---
    child_prompt = f"Based on the following high school summary, create a very simple summary for children. Use simple language and analogies: High School Summary: {high_school_summary}"
    child_summary_response = model.generate_content([child_prompt, pdf_file])
    child_summary = child_summary_response.text
    print("Child Summary Generated.")

    # --- Create Markdown Blog Post ---
    full_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z')

    file_content = f"""---
layout: tabbed_post
title:  "{paper_name}"
date:   {full_timestamp}
categories: ai forskning
---

## For Barn

{child_summary}

## For Videregåendeelever

{high_school_summary}

## For Universitets- og Høyskolenivå

{advanced_summary}
"""

    os.makedirs(os.path.dirname(post_path), exist_ok=True)
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"Blog post created at: {post_path}")
    
    # --- Clean up the uploaded file ---
    print(f"Deleting file: {pdf_file.name}")
    genai.delete_file(pdf_file.name)
    print("File deleted.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <path_to_paper.pdf>")
        sys.exit(1)
    paper_path_arg = sys.argv[1]
    create_summary(paper_path_arg)
