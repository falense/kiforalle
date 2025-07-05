
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

    # --- Extract Paper Title ---
    title_prompt = "Extract the title of this research paper. Return only the title, nothing else:"
    title_response = model.generate_content([title_prompt, pdf_file])
    paper_title = title_response.text.strip()
    print(f"Extracted paper title: {paper_title}")
    
    # Fallback to filename if title extraction fails or is too short
    if not paper_title or len(paper_title) < 5:
        paper_title = paper_name
        print(f"Using filename as title: {paper_title}")

    # --- Extract Authors ---
    authors_prompt = "Extract the authors of this research paper. Return only the authors' names separated by commas, nothing else:"
    authors_response = model.generate_content([authors_prompt, pdf_file])
    paper_authors = authors_response.text.strip()
    print(f"Extracted authors: {paper_authors}")
    
    # Clean up authors string and validate
    if paper_authors and len(paper_authors) > 2:
        # Remove any extra text that might be included
        paper_authors = paper_authors.replace("Authors:", "").replace("By:", "").strip()
        # Ensure it doesn't look like an error message
        if "unable" in paper_authors.lower() or "cannot" in paper_authors.lower() or "error" in paper_authors.lower():
            paper_authors = ""
    else:
        paper_authors = ""
    
    if not paper_authors:
        print("No authors extracted, leaving blank")

    # --- Advanced Summary Generation ---
    advanced_prompt = """
    You are a research paper summarizer. Create a comprehensive summary of this research paper for university/college level students.
    
    Requirements:
    - Focus on key concepts, methodologies, and findings
    - Include the research question, methodology, main results, and implications
    - Use academic language appropriate for university students
    - Be thorough but concise (aim for 300-500 words)
    - Write in English initially
    
    Summarize this research paper:
    """
    advanced_summary_response = model.generate_content([advanced_prompt, pdf_file])
    advanced_summary = advanced_summary_response.text
    print("Advanced Summary Generated.")

    # --- High School Summary Generation ---
    high_school_prompt = f"""
    You are a research paper summarizer. Based on the following advanced summary, create a summary suitable for high school students.
    
    Requirements:
    - Simplify complex terms and concepts
    - Focus on the main ideas and their real-world implications
    - Use language appropriate for 16-18 year olds
    - Make it engaging and relatable
    - Be concise (aim for 200-300 words)
    - Write in English initially
    
    Advanced Summary: {advanced_summary}
    
    Create a high school level summary:
    """
    high_school_summary_response = model.generate_content([high_school_prompt, pdf_file])
    high_school_summary = high_school_summary_response.text
    print("High School Summary Generated.")

    # --- Child Summary Generation ---
    child_prompt = f"""
    You are a research paper summarizer. Based on the following high school summary, create a very simple summary for children (ages 8-12).
    
    Requirements:
    - Use very simple language and short sentences
    - Include analogies and examples children can understand
    - Focus on why this research matters in everyday life
    - Make it fun and engaging
    - Be brief (aim for 100-150 words)
    - Write in English initially
    
    High School Summary: {high_school_summary}
    
    Create a child-friendly summary:
    """
    child_summary_response = model.generate_content([child_prompt, pdf_file])
    child_summary = child_summary_response.text
    print("Child Summary Generated.")

    # --- Translation to Norwegian ---
    print("Translating summaries to Norwegian...")
    
    # Translate Advanced Summary
    advanced_translation_prompt = f"""
    Translate the following academic summary to Norwegian. Maintain the academic tone and technical accuracy.
    Use Norwegian academic terminology where appropriate.
    
    Text to translate: {advanced_summary}
    """
    advanced_norwegian_response = model.generate_content([advanced_translation_prompt])
    advanced_summary_no = advanced_norwegian_response.text
    print("Advanced summary translated to Norwegian.")

    # Translate High School Summary
    high_school_translation_prompt = f"""
    Translate the following high school level summary to Norwegian. Maintain the appropriate language level for Norwegian teenagers.
    Use Norwegian terminology that high school students would understand.
    
    Text to translate: {high_school_summary}
    """
    high_school_norwegian_response = model.generate_content([high_school_translation_prompt])
    high_school_summary_no = high_school_norwegian_response.text
    print("High school summary translated to Norwegian.")

    # Translate Child Summary
    child_translation_prompt = f"""
    Translate the following child-friendly summary to Norwegian. Use simple Norwegian that Norwegian children would understand.
    Keep the fun and engaging tone. Use Norwegian words and expressions that are familiar to Norwegian children.
    
    Text to translate: {child_summary}
    """
    child_norwegian_response = model.generate_content([child_translation_prompt])
    child_summary_no = child_norwegian_response.text
    print("Child summary translated to Norwegian.")

    # --- Reflection and Quality Check ---
    print("Performing quality reflection on Norwegian summaries...")
    
    reflection_prompt = f"""
    You are a quality reviewer for Norwegian academic summaries. Review the following three Norwegian summaries of the same research paper and assess:

    1. Do they accurately reflect the content and findings of the original paper?
    2. Are they appropriate for their target audiences (university, high school, children)?
    3. Is the Norwegian language natural and correct?
    4. Are there any important details missing or misrepresented?
    5. Do they maintain consistency in key facts across all three levels?

    Original Paper Context: [You have access to the full paper]
    
    Advanced Summary (Norwegian): {advanced_summary_no}
    
    High School Summary (Norwegian): {high_school_summary_no}
    
    Child Summary (Norwegian): {child_summary_no}
    
    Provide a brief assessment and any recommended improvements. If the summaries are satisfactory, simply state "Summaries are accurate and appropriate for their target audiences."
    """
    reflection_response = model.generate_content([reflection_prompt, pdf_file])
    reflection_result = reflection_response.text
    print(f"Quality reflection completed: {reflection_result}")

    # Use Norwegian summaries for the final output
    advanced_summary = advanced_summary_no
    high_school_summary = high_school_summary_no
    child_summary = child_summary_no

    # --- Create Markdown Blog Post ---
    full_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z')

    file_content = f"""---
layout: tabbed_post
title:  "{paper_title}"
paper_id: "{paper_name}"
authors: "{paper_authors}"
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
