import os
import sys
from datetime import datetime
import google.generativeai as genai
from google.generativeai import types
import httpx

def create_summary(paper_path):
    paper_name = os.path.splitext(os.path.basename(paper_path))[0]
    date_str = datetime.now().strftime("%Y-%m-%d")
    post_path = f"_posts/{date_str}-{paper_name}.markdown"

    # Configure Gemini API
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Read PDF as bytes
    with open(paper_path, "rb") as f:
        doc_data = f.read()

    # Generate advanced summary
    advanced_prompt = "Summarize this research paper for university/college level students, focusing on key concepts, methodologies, and findings:"
    advanced_summary_response = model.generate_content(
        contents=[
            genai.types.Blob(data=doc_data, mime_type='application/pdf'),
            advanced_prompt
        ]
    )
    advanced_summary = advanced_summary_response.text
    print("Advanced Summary Generated.")

    # Reflection for advanced summary (for internal use/logging)
    advanced_reflection_prompt = f"Review the following advanced summary and the original paper content. Does the summary accurately reflect the key concepts, methodologies, and findings of the paper? Provide a brief critique.\n\nAdvanced Summary:\n{advanced_summary}"
    advanced_reflection_response = model.generate_content(
        contents=[
            genai.types.Blob(data=doc_data, mime_type='application/pdf'),
            advanced_reflection_prompt
        ]
    )
    advanced_reflection = advanced_reflection_response.text
    print(f"Advanced Summary Reflection: {advanced_reflection}")

    # Generate high school summary
    high_school_prompt = f"Based on the following advanced summary, create a summary suitable for high school students. Simplify complex terms and focus on the main ideas and implications:\n\nAdvanced Summary:\n{advanced_summary}"
    high_school_summary_response = model.generate_content(
        contents=[
            genai.types.Blob(data=doc_data, mime_type='application/pdf'),
            high_school_prompt
        ]
    )
    high_school_summary = high_school_summary_response.text
    print("High School Summary Generated.")

    # Reflection for high school summary
    high_school_reflection_prompt = f"Review the following high school summary and the advanced summary. Is the high school summary clear, concise, and appropriate for the target audience, while still accurately conveying the main points?\n\nAdvanced Summary:\n{advanced_summary}\n\nHigh School Summary:\n{high_school_summary}"
    high_school_reflection_response = model.generate_content(
        contents=[
            genai.types.Blob(data=doc_data, mime_type='application/pdf'),
            high_school_reflection_prompt
        ]
    )
    high_school_reflection = high_school_reflection_response.text
    print(f"High School Summary Reflection: {high_school_reflection}")

    # Generate child summary
    child_prompt = f"Based on the following high school summary, create a very simple summary for children. Use simple language and analogies:\n\nHigh School Summary:\n{high_school_summary}"
    child_summary_response = model.generate_content(
        contents=[
            genai.types.Blob(data=doc_data, mime_type='application/pdf'),
            child_prompt
        ]
    )
    child_summary = child_summary_response.text
    print("Child Summary Generated.")

    # Reflection for child summary
    child_reflection_prompt = f"Review the following child summary and the high school summary. Is the child summary easy to understand for a young audience and does it capture the essence of the paper in a simplified way?\n\nHigh School Summary:\n{high_school_summary}\n\nChild Summary:\n{child_summary}"
    child_reflection_response = model.generate_content(
        contents=[
            genai.types.Blob(data=doc_data, mime_type='application/pdf'),
            child_reflection_prompt
        ]
    )
    child_reflection = child_reflection_response.text
    print(f"Child Summary Reflection: {child_reflection}")

    with open(post_path, "w") as f:
        f.write(f"""---
layout: tabbed_post
title:  "{paper_name}"
date:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S +0200')}
categories: ai forskning
---

## For Barn

{child_summary}

## For Videregåendeelever

{high_school_summary}

## For Universitets- og Høyskolenivå

{advanced_summary}
""")

if __name__ == "__main__":
    paper_path = sys.argv[1]
    create_summary(paper_path)
