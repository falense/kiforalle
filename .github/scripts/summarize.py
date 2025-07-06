
import os
import sys
import datetime
import pathlib
import base64
import re
import fitz  # PyMuPDF
from PIL import Image
import io
import google.generativeai as genai

def extract_figures_from_pdf(pdf_path):
    """
    Extract all figures/images from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of dictionaries containing figure data and metadata
    """
    print(f"=== Extracting figures from PDF ===")
    figures = []
    
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)
        print(f"Opened PDF with {len(doc)} pages")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images()
            
            print(f"Page {page_num + 1}: Found {len(image_list)} images")
            
            for img_index, img in enumerate(image_list):
                # Get image data
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                # Skip if image is too small (likely not a figure)
                if pix.width < 100 or pix.height < 100:
                    pix = None
                    continue
                
                # Convert to PIL Image
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_data = pix.tobytes("png")
                    pil_image = Image.open(io.BytesIO(img_data))
                    
                    # Create figure metadata
                    figure_info = {
                        'page': page_num + 1,
                        'index': img_index,
                        'width': pix.width,
                        'height': pix.height,
                        'image_data': img_data,
                        'pil_image': pil_image,
                        'id': f"fig_{page_num + 1}_{img_index}"
                    }
                    
                    figures.append(figure_info)
                    print(f"  Extracted figure {figure_info['id']}: {pix.width}x{pix.height}")
                
                pix = None
                
        doc.close()
        print(f"Total figures extracted: {len(figures)}")
        return figures
        
    except Exception as e:
        print(f"ERROR: Failed to extract figures: {e}")
        return []

def select_figure_for_summary(model, uploaded_figures, summary_text, audience_level):
    """
    Select the most appropriate figure for a given summary and audience level.
    
    Args:
        model: Gemini model instance
        uploaded_figures: List of uploaded figures with metadata
        summary_text: The summary text to match against
        audience_level: Target audience ('child', 'high_school', 'university')
        
    Returns:
        dict: Selected figure info or None if no appropriate figure found
    """
    if not uploaded_figures:
        print(f"No figures available for {audience_level} level selection")
        return None
    
    print(f"=== Selecting figure for {audience_level} level ===")
    
    # Create selection prompt
    selection_prompt = f"""
    You are analyzing figures from a research paper to select the most appropriate one for a specific audience level.
    
    Target Audience: {audience_level}
    Summary Text: {summary_text}
    
    I will show you several figures from the paper. Please:
    1. Analyze each figure for its relevance to the summary content
    2. Consider the complexity level appropriate for the target audience:
       - Child: Simple, visual, easy to understand diagrams or photos
       - High School: Moderately complex charts, clear illustrations
       - University: Complex graphs, technical diagrams, detailed visualizations
    3. Select the MOST appropriate figure, or respond with "NONE" if no figure is suitable
    
    Respond with only the figure number (e.g., "Figure 1") or "NONE".
    """
    
    try:
        # Prepare content for the model
        content = [selection_prompt]
        
        # Add each figure with a label
        for i, fig_info in enumerate(uploaded_figures):
            content.append(f"Figure {i+1}:")
            content.append(fig_info['gemini_file'])
        
        # Get model response
        response = model.generate_content(content)
        selection_result = response.text.strip()
        
        print(f"Model selection result: {selection_result}")
        
        # Parse the response
        if selection_result.upper() == "NONE":
            print(f"No appropriate figure selected for {audience_level} level")
            return None
        
        # Extract figure number
        if "Figure" in selection_result or "figure" in selection_result:
            try:
                # Extract number from response like "Figure 1" or "figure 2"
                import re
                match = re.search(r'[Ff]igure (\d+)', selection_result)
                if match:
                    fig_num = int(match.group(1)) - 1  # Convert to 0-based index
                    if 0 <= fig_num < len(uploaded_figures):
                        selected_fig = uploaded_figures[fig_num]
                        print(f"Selected figure {fig_num + 1} for {audience_level} level")
                        return selected_fig
            except (ValueError, IndexError):
                pass
        
        print(f"Could not parse figure selection result: {selection_result}")
        return None
        
    except Exception as e:
        print(f"ERROR: Failed to select figure for {audience_level} level: {e}")
        return None

def create_summary(paper_path):
    """
    Generates a blog post with summaries of a research paper for different audiences.

    Args:
        paper_path (str): The path to the PDF file of the research paper.
    """
    print(f"=== Starting summarization process ===")
    print(f"Paper path: {paper_path}")
    
    paper_name = pathlib.Path(paper_path).stem
    print(f"Paper name: {paper_name}")

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

    # --- Extract Figures from PDF ---
    print(f"=== Extracting figures from PDF ===")
    figures = extract_figures_from_pdf(paper_path)
    
    # Upload figures to Gemini for analysis
    uploaded_figures = []
    for figure in figures:
        try:
            # Save figure temporarily
            temp_fig_path = f"temp_{figure['id']}.png"
            figure['pil_image'].save(temp_fig_path)
            
            # Upload to Gemini
            uploaded_fig = genai.upload_file(path=temp_fig_path)
            uploaded_figures.append({
                'gemini_file': uploaded_fig,
                'metadata': figure,
                'temp_path': temp_fig_path
            })
            print(f"Uploaded figure {figure['id']} to Gemini")
            
        except Exception as e:
            print(f"ERROR: Failed to upload figure {figure['id']}: {e}")
            continue

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

    # --- Extract Paper Date ---
    print(f"=== Extracting paper date ===")
    date_prompt = """Extract the publication date or submission date from this arXiv paper. 
    Look for dates in formats like:
    - "Submitted on 15 Mar 2024"
    - "v1 [cs.AI] 15 Mar 2024"
    - Any date mentioned in the paper header or metadata
    
    Return only the date in YYYY-MM-DD format, nothing else. If no date is found, return "NOT_FOUND"."""
    print(f"Date extraction prompt: {date_prompt}")
    
    try:
        date_response = model.generate_content([date_prompt, pdf_file])
        extracted_date = date_response.text.strip()
        print(f"Raw date response: '{date_response.text}'")
        print(f"Cleaned date: '{extracted_date}'")
        
        # Validate and parse the extracted date
        paper_date = None
        if extracted_date and extracted_date.upper() != "NOT_FOUND":
            try:
                # Try to parse the date to validate it
                parsed_date = datetime.datetime.strptime(extracted_date, "%Y-%m-%d")
                paper_date = extracted_date
                print(f"Successfully parsed paper date: {paper_date}")
            except ValueError:
                print(f"Could not parse extracted date '{extracted_date}', trying alternative parsing...")
                # Try to extract date from various formats
                date_patterns = [
                    r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
                    r'(\d{1,2})\s+(\w{3})\s+(\d{4})',  # DD MMM YYYY
                    r'(\w{3})\s+(\d{1,2}),?\s+(\d{4})',  # MMM DD, YYYY
                ]
                
                for pattern in date_patterns:
                    match = re.search(pattern, extracted_date)
                    if match:
                        try:
                            if pattern == date_patterns[0]:  # YYYY-MM-DD
                                paper_date = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                            elif pattern == date_patterns[1]:  # DD MMM YYYY
                                month_map = {
                                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                                }
                                day = match.group(1).zfill(2)
                                month = month_map.get(match.group(2), '01')
                                year = match.group(3)
                                paper_date = f"{year}-{month}-{day}"
                            elif pattern == date_patterns[2]:  # MMM DD, YYYY
                                month_map = {
                                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                                }
                                month = month_map.get(match.group(1), '01')
                                day = match.group(2).zfill(2)
                                year = match.group(3)
                                paper_date = f"{year}-{month}-{day}"
                            
                            # Validate the constructed date
                            datetime.datetime.strptime(paper_date, "%Y-%m-%d")
                            print(f"Successfully parsed alternative date format: {paper_date}")
                            break
                        except (ValueError, KeyError):
                            continue
        
        if not paper_date:
            print("Could not extract or parse paper date, using current date as fallback")
            paper_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        print(f"Final paper date: {paper_date}")
        
    except Exception as e:
        print(f"ERROR: Failed to extract paper date: {e}")
        paper_date = datetime.datetime.now().strftime("%Y-%m-%d")
        print(f"Using current date as fallback: {paper_date}")

    # --- Set up post path using extracted date ---
    post_path = f"_posts/{paper_date}-{paper_name}.markdown"
    print(f"Output post path: {post_path}")

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

    # --- Select Figures for Each Summary Level ---
    print(f"=== Selecting figures for each summary level ===")
    
    # Select figure for university level
    selected_university_fig = select_figure_for_summary(
        model, uploaded_figures, advanced_summary, "university"
    )
    
    # Select figure for high school level
    selected_high_school_fig = select_figure_for_summary(
        model, uploaded_figures, high_school_summary, "high_school"
    )
    
    # Select figure for child level
    selected_child_fig = select_figure_for_summary(
        model, uploaded_figures, child_summary, "child"
    )
    
    # Save selected figures to assets directory
    selected_figures = {}
    paper_assets_dir = f"assets/papers/{paper_name}"
    
    if selected_university_fig or selected_high_school_fig or selected_child_fig:
        print(f"Creating assets directory: {paper_assets_dir}")
        try:
            os.makedirs(paper_assets_dir, exist_ok=True)
            
            # Save university figure
            if selected_university_fig:
                university_fig_path = f"{paper_assets_dir}/university_fig.png"
                selected_university_fig['metadata']['pil_image'].save(university_fig_path)
                selected_figures['university'] = f"/assets/papers/{paper_name}/university_fig.png"
                print(f"Saved university figure to: {university_fig_path}")
            
            # Save high school figure
            if selected_high_school_fig:
                high_school_fig_path = f"{paper_assets_dir}/high_school_fig.png"
                selected_high_school_fig['metadata']['pil_image'].save(high_school_fig_path)
                selected_figures['high_school'] = f"/assets/papers/{paper_name}/high_school_fig.png"
                print(f"Saved high school figure to: {high_school_fig_path}")
            
            # Save child figure
            if selected_child_fig:
                child_fig_path = f"{paper_assets_dir}/child_fig.png"
                selected_child_fig['metadata']['pil_image'].save(child_fig_path)
                selected_figures['child'] = f"/assets/papers/{paper_name}/child_fig.png"
                print(f"Saved child figure to: {child_fig_path}")
                
        except Exception as e:
            print(f"ERROR: Failed to save figures: {e}")
            selected_figures = {}
    
    print(f"Selected figures: {selected_figures}")

    # --- Create Markdown Blog Post ---
    print(f"=== Creating Markdown Blog Post ===")
    # Use extracted paper date with a default time
    paper_datetime = datetime.datetime.strptime(paper_date, "%Y-%m-%d")
    # Set time to 12:00 PM UTC for consistency
    paper_datetime = paper_datetime.replace(hour=12, minute=0, second=0, tzinfo=datetime.timezone.utc)
    full_timestamp = paper_datetime.strftime('%Y-%m-%d %H:%M:%S %z')
    print(f"Paper date timestamp: {full_timestamp}")

    # Build figure sections
    child_figure_section = ""
    if 'child' in selected_figures:
        child_figure_section = f'\n\n![Figure for barn]({selected_figures["child"]})\n'
    
    high_school_figure_section = ""
    if 'high_school' in selected_figures:
        high_school_figure_section = f'\n\n![Figure for videregående]({selected_figures["high_school"]})\n'
    
    university_figure_section = ""
    if 'university' in selected_figures:
        university_figure_section = f'\n\n![Figure for universitets- og høyskolenivå]({selected_figures["university"]})\n'

    file_content = f"""---
layout: tabbed_post
title:  "{paper_title}"
paper_id: "{paper_name}"
authors: "{paper_authors}"
date:   {full_timestamp}
categories: ai forskning
---

## For Barn

{child_summary}{child_figure_section}

## For Videregåendeelever

{high_school_summary}{high_school_figure_section}

## For Universitets- og Høyskolenivå

{advanced_summary}{university_figure_section}
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
    
    # --- Clean up uploaded files ---
    print(f"=== Cleaning up uploaded files ===")
    try:
        print(f"Deleting PDF file: {pdf_file.name}")
        genai.delete_file(pdf_file.name)
        print("PDF file deleted successfully.")
    except Exception as e:
        print(f"ERROR: Failed to delete uploaded PDF file: {e}")
        # Don't raise here as the main task is complete
    
    # Clean up uploaded figures
    for fig_info in uploaded_figures:
        try:
            print(f"Deleting figure: {fig_info['gemini_file'].name}")
            genai.delete_file(fig_info['gemini_file'].name)
            
            # Remove temporary file
            if os.path.exists(fig_info['temp_path']):
                os.remove(fig_info['temp_path'])
                print(f"Removed temporary file: {fig_info['temp_path']}")
                
        except Exception as e:
            print(f"ERROR: Failed to delete figure {fig_info['gemini_file'].name}: {e}")
            # Don't raise here as the main task is complete
        
    print(f"=== Summarization process completed successfully! ===")
    print(f"Final output: {post_path}")
    
    # --- Output metadata for GitHub Actions ---
    print(f"=== Outputting metadata for GitHub Actions ===")
    print(f"PAPER_TITLE={paper_title}")
    print(f"PAPER_AUTHORS={paper_authors}")
    print(f"PAPER_ID={paper_name}")
    print(f"POST_PATH={post_path}")
    
    # Write metadata to a file that GitHub Actions can read
    metadata_file = "_paper_metadata.txt"
    try:
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write(f"PAPER_TITLE={paper_title}\n")
            f.write(f"PAPER_AUTHORS={paper_authors}\n")
            f.write(f"PAPER_ID={paper_name}\n")
            f.write(f"POST_PATH={post_path}\n")
        print(f"Metadata written to: {metadata_file}")
    except Exception as e:
        print(f"ERROR: Failed to write metadata file: {e}")
        # Don't raise here as the main task is complete


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <path_to_paper.pdf>")
        sys.exit(1)
    paper_path_arg = sys.argv[1]
    create_summary(paper_path_arg)
