import weasyprint
import os
import re # We'll use the regular expression module to find question numbers

# --- Configuration: Set up all the paths ---
download_folder = '/storage/emulated/0/Download'
font_filename = 'AnekMalayalam-Bold.ttf'
font_path = os.path.join(download_folder, font_filename)
# Let's give the output a new name
output_filename = 'My_Malayalam_Note_Compact.pdf'
output_pdf_path = os.path.join(download_folder, output_filename)


# --- Step 1: Check if the required font exists ---
if not os.path.exists(font_path):
    print(f"--- ERROR ---")
    print(f"Font file not found: '{font_filename}'")
    print(f"Please make sure it is in your Download folder.")
    exit()

def format_text_for_html(lines):
    """
    This function intelligently processes the user's text to create
    a compact HTML layout. It removes empty lines and adds a small
    space only before a new question.
    """
    html_output = []
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue # Skip empty lines completely

        # Check if the line starts with a number followed by a dot (e.g., "1.", "10.")
        if re.match(r"^\d+\.", cleaned_line):
            # This is a new question, so we give it a special class to add space above it
            html_output.append(f'<p class="question">{cleaned_line}</p>')
        else:
            # This is a regular line (intro, option, etc.)
            html_output.append(f'<p>{cleaned_line}</p>')
            
    return "\n".join(html_output)


# --- Step 2: Get text input from the user ---
print("--- Compact Malayalam PDF Creator ---")
print("Enter your text below. Type 'END' on a new line and press Enter to finish.")
print("-----------------------------------------------------------------------")

user_lines = []
while True:
    line = input()
    if line.strip().upper() == 'END':
        break
    user_lines.append(line)

# Process the input text using our new function
formatted_text = format_text_for_html(user_lines)

if not formatted_text:
    print("\nNo text was entered. Exiting.")
    exit()

# --- Step 3: Create the HTML and CSS template ---
# This CSS is specifically designed for minimum wasted space.
html_template = f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {{
            font-family: 'Anek Malayalam';
            src: url('{font_filename}');
        }}

        body {{
            font-family: 'Anek Malayalam', sans-serif;
            /* Smaller font size for more text */
            font-size: 13pt; 
            /* Reduced page margins */
            margin: 1.5cm; 
        }}
        
        /* Style for ALL paragraphs */
        p {{
            /* This is the key part: very little space between lines */
            margin-top: 0;
            margin-bottom: 0.2em; /* Tiny space after each line */
            line-height: 1.3;     /* Tighter line spacing */
        }}

        /* Style ONLY for paragraphs that are questions */
        .question {{
            /* Adds a bit of space ABOVE a new question to separate it */
            margin-top: 0.8em; 
        }}
    </style>
</head>
<body>
    {formatted_text}
</body>
</html>
"""

# --- Step 4: Generate the PDF ---
print("\nCreating compact PDF...")
try:
    html = weasyprint.HTML(string=html_template, base_url=download_folder)
    html.write_pdf(output_pdf_path)

    print("\n--- SUCCESS! ---")
    print(f"Compact PDF created successfully.")
    print(f"File saved as '{output_filename}' in your Download folder.")

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An error occurred: {e}")
