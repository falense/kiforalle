
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
    print(f"=== Starting summarization process ===")
    print(f"Paper path: {paper_path}")
    
    paper_name = pathlib.Path(paper_path).stem
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    post_path = f"_posts/{current_date}-{paper_name}.markdown"
    
    print(f"Paper name: {paper_name}")
    print(f"Current date: {current_date}")
    print(f"Output post path: {post_path}")

    # --- API Configuration ---
    print(f"=== Configuring Gemini API ===")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    print(f"API key found: {api_key[:10]}...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Gemini model configured successfully.")

    # --- File Reading ---
    print(f"=== Uploading PDF file ===")
    print(f"Reading paper: {paper_path}")
    try:
        pdf_file = genai.upload_file(path=paper_path)
        print(f"Successfully uploaded file: {pdf_file.name}")
        print(f"File size: {pdf_file.size_bytes} bytes")
        print(f"File MIME type: {pdf_file.mime_type}")
    except Exception as e:
        print(f"ERROR: Failed to upload file: {e}")
        raise

    # --- Extract Paper Title ---
    print(f"=== Extracting paper title ===")
    title_prompt = "Extract the title of this research paper. Return only the title, nothing else:"
    print(f"Title extraction prompt: {title_prompt}")
    
    try:
        title_response = model.generate_content([title_prompt, pdf_file])
        paper_title = title_response.text.strip()
        print(f"Raw title response: '{title_response.text}'")
        print(f"Cleaned title: '{paper_title}'")
        print(f"Title length: {len(paper_title)} characters")
    except Exception as e:
        print(f"ERROR: Failed to extract title: {e}")
        paper_title = ""
    
    # Fallback to filename if title extraction fails or is too short
    if not paper_title or len(paper_title) < 5:
        paper_title = paper_name
        print(f"Title too short or empty, using filename as title: {paper_title}")
    else:
        print(f"Successfully extracted title: {paper_title}")

    # --- Extract Authors ---
    print(f"=== Extracting authors ===")
    authors_prompt = "Extract the authors of this research paper. Return only the authors' names separated by commas, nothing else:"
    print(f"Authors extraction prompt: {authors_prompt}")
    
    try:
        authors_response = model.generate_content([authors_prompt, pdf_file])
        paper_authors = authors_response.text.strip()
        print(f"Raw authors response: '{authors_response.text}'")
        print(f"Cleaned authors: '{paper_authors}'")
        print(f"Authors length: {len(paper_authors)} characters")
    except Exception as e:
        print(f"ERROR: Failed to extract authors: {e}")
        paper_authors = ""
    
    # Clean up authors string and validate
    if paper_authors and len(paper_authors) > 2:
        print(f"Processing authors string...")
        # Remove any extra text that might be included
        paper_authors = paper_authors.replace("Authors:", "").replace("By:", "").strip()
        print(f"After cleanup: '{paper_authors}'")
        
        # Ensure it doesn't look like an error message
        if "unable" in paper_authors.lower() or "cannot" in paper_authors.lower() or "error" in paper_authors.lower():
            print("Authors string contains error indicators, clearing...")
            paper_authors = ""
    else:
        print("Authors string too short, clearing...")
        paper_authors = ""
    
    if not paper_authors:
        print("Final result: No authors extracted, leaving blank")
    else:
        print(f"Final authors: {paper_authors}")

    # --- Advanced Summary Generation ---
    print(f"=== Generating Advanced Summary ===")
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
    print(f"Advanced summary prompt prepared ({len(advanced_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for advanced summary...")
        advanced_summary_response = model.generate_content([advanced_prompt, pdf_file])
        advanced_summary = advanced_summary_response.text
        print(f"Advanced summary generated successfully!")
        print(f"Advanced summary length: {len(advanced_summary)} characters")
        print(f"Advanced summary preview: {advanced_summary[:200]}...")
    except Exception as e:
        print(f"ERROR: Failed to generate advanced summary: {e}")
        raise

    # --- High School Summary Generation ---
    print(f"=== Generating High School Summary ===")
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
    print(f"High school summary prompt prepared ({len(high_school_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for high school summary...")
        high_school_summary_response = model.generate_content([high_school_prompt, pdf_file])
        high_school_summary = high_school_summary_response.text
        print(f"High school summary generated successfully!")
        print(f"High school summary length: {len(high_school_summary)} characters")
        print(f"High school summary preview: {high_school_summary[:200]}...")
    except Exception as e:
        print(f"ERROR: Failed to generate high school summary: {e}")
        raise

    # --- Child Summary Generation ---
    print(f"=== Generating Child Summary ===")
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
    print(f"Child summary prompt prepared ({len(child_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for child summary...")
        child_summary_response = model.generate_content([child_prompt, pdf_file])
        child_summary = child_summary_response.text
        print(f"Child summary generated successfully!")
        print(f"Child summary length: {len(child_summary)} characters")
        print(f"Child summary preview: {child_summary[:200]}...")
    except Exception as e:
        print(f"ERROR: Failed to generate child summary: {e}")
        raise

    # --- Translation to Norwegian ---
    print(f"=== Translating summaries to Norwegian ===")
    
    # Translate Advanced Summary
    print(f"=== Translating Advanced Summary ===")
    advanced_translation_prompt = f"""
    Translate the following academic summary to Norwegian. Maintain the academic tone and technical accuracy.
    Use Norwegian academic terminology where appropriate.
    
    Text to translate: {advanced_summary}
    """
    print(f"Advanced translation prompt prepared ({len(advanced_translation_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for advanced summary translation...")
        advanced_norwegian_response = model.generate_content([advanced_translation_prompt])
        advanced_summary_no = advanced_norwegian_response.text
        print(f"Advanced summary translated successfully!")
        print(f"Norwegian advanced summary length: {len(advanced_summary_no)} characters")
        print(f"Norwegian advanced summary preview: {advanced_summary_no[:200]}...")
    except Exception as e:
        print(f"ERROR: Failed to translate advanced summary: {e}")
        raise

    # Translate High School Summary
    print(f"=== Translating High School Summary ===")
    high_school_translation_prompt = f"""
    Translate the following high school level summary to Norwegian. Maintain the appropriate language level for Norwegian teenagers.
    Use Norwegian terminology that high school students would understand.
    
    Text to translate: {high_school_summary}
    """
    print(f"High school translation prompt prepared ({len(high_school_translation_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for high school summary translation...")
        high_school_norwegian_response = model.generate_content([high_school_translation_prompt])
        high_school_summary_no = high_school_norwegian_response.text
        print(f"High school summary translated successfully!")
        print(f"Norwegian high school summary length: {len(high_school_summary_no)} characters")
        print(f"Norwegian high school summary preview: {high_school_summary_no[:200]}...")
    except Exception as e:
        print(f"ERROR: Failed to translate high school summary: {e}")
        raise

    # Translate Child Summary
    print(f"=== Translating Child Summary ===")
    child_translation_prompt = f"""
    Translate the following child-friendly summary to Norwegian. Use simple Norwegian that Norwegian children would understand.
    Keep the fun and engaging tone. Use Norwegian words and expressions that are familiar to Norwegian children.
    
    Text to translate: {child_summary}
    """
    print(f"Child translation prompt prepared ({len(child_translation_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for child summary translation...")
        child_norwegian_response = model.generate_content([child_translation_prompt])
        child_summary_no = child_norwegian_response.text
        print(f"Child summary translated successfully!")
        print(f"Norwegian child summary length: {len(child_summary_no)} characters")
        print(f"Norwegian child summary preview: {child_summary_no[:200]}...")
    except Exception as e:
        print(f"ERROR: Failed to translate child summary: {e}")
        raise

    # --- Reflection and Quality Check ---
    print(f"=== Performing Quality Reflection ===")
    
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
    print(f"Quality reflection prompt prepared ({len(reflection_prompt)} characters)")
    
    try:
        print("Sending request to Gemini for quality reflection...")
        reflection_response = model.generate_content([reflection_prompt, pdf_file])
        reflection_result = reflection_response.text
        print(f"Quality reflection completed successfully!")
        print(f"Reflection result length: {len(reflection_result)} characters")
        print(f"Quality reflection result: {reflection_result}")
    except Exception as e:
        print(f"ERROR: Failed to perform quality reflection: {e}")
        print("Continuing with summaries despite reflection failure...")
        reflection_result = "Quality reflection failed but summaries generated successfully."

    # Use Norwegian summaries for the final output
    print(f"=== Using Norwegian summaries for final output ===")
    advanced_summary = advanced_summary_no
    high_school_summary = high_school_summary_no
    child_summary = child_summary_no
    print("Successfully switched to Norwegian summaries for final output.")

    # --- Create Markdown Blog Post ---
    print(f"=== Creating Markdown Blog Post ===")
    full_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z')
    print(f"Full timestamp: {full_timestamp}")

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

    print(f"Blog post content prepared ({len(file_content)} characters)")
    print(f"Creating directory: {os.path.dirname(post_path)}")
    
    try:
        os.makedirs(os.path.dirname(post_path), exist_ok=True)
        print("Directory created successfully.")
        
        print(f"Writing blog post to: {post_path}")
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"Blog post created successfully at: {post_path}")
        
        # Verify file was created
        if os.path.exists(post_path):
            file_size = os.path.getsize(post_path)
            print(f"File verification: {post_path} exists ({file_size} bytes)")
        else:
            print(f"WARNING: File verification failed - {post_path} does not exist")
            
    except Exception as e:
        print(f"ERROR: Failed to create blog post: {e}")
        raise
    
    # --- Clean up the uploaded file ---
    print(f"=== Cleaning up uploaded file ===")
    try:
        print(f"Deleting file: {pdf_file.name}")
        genai.delete_file(pdf_file.name)
        print("File deleted successfully.")
    except Exception as e:
        print(f"ERROR: Failed to delete uploaded file: {e}")
        # Don't raise here as the main task is complete
        
    print(f"=== Summarization process completed successfully! ===")
    print(f"Final output: {post_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <path_to_paper.pdf>")
        sys.exit(1)
    paper_path_arg = sys.argv[1]
    create_summary(paper_path_arg)
