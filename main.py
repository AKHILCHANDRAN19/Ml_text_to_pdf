import weasyprint
import os
import re

# --- Configuration: Set up all the paths ---
# This is the base path for your phone's user-accessible storage.
base_storage_path = '/storage/emulated/0' 
quiz_folder_name = 'Quiz'
# We now join the base path directly with your desired folder name.
quiz_folder_path = os.path.join(base_storage_path, quiz_folder_name)

# --- Path for the font (assuming it's still in the Download folder) ---
download_folder = '/storage/emulated/0/Download'
font_filename = 'AnekMalayalam-Bold.ttf'
font_path = os.path.join(download_folder, font_filename)


# --- Step 1: Create the 'Quiz' folder if it doesn't exist ---
# This will now create the folder at /storage/emulated/0/Quiz
if not os.path.exists(quiz_folder_path):
    print(f"Creating folder at: '{quiz_folder_path}'...")
    os.makedirs(quiz_folder_path)


# --- Step 2: Ask for a filename and set the final output paths ---
base_filename = input("Enter a name for your quiz files (e.g., 'Chapter_1_Quiz'): ")
output_pdf_filename = f'{base_filename}.pdf'
output_txt_filename = f'{base_filename}.txt'

output_pdf_path = os.path.join(quiz_folder_path, output_pdf_filename)
output_txt_path = os.path.join(quiz_folder_path, output_txt_filename)


# --- Step 3: Check if the required font exists ---
if not os.path.exists(font_path):
    print(f"--- ERROR ---")
    print(f"Font file not found: '{font_filename}'")
    print(f"Please make sure it is in your Download folder: '{download_folder}'")
    exit()


def format_text_for_html(lines):
    html_output = []
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        if re.match(r"^\d+\.", cleaned_line):
            html_output.append(f'<p class="question">{cleaned_line}</p>')
        else:
            html_output.append(f'<p>{cleaned_line}</p>')
    return "\n".join(html_output)


# --- Step 4: Get text input from the user ---
print("--- Compact Malayalam PDF & TXT Creator ---")
print("Enter your text below. Type 'END' on a new line and press Enter to finish.")
print("-----------------------------------------------------------------------")

user_lines = []
while True:
    line = input()
    if line.strip().upper() == 'END':
        break
    user_lines.append(line)

user_text_for_txt = "\n".join(user_lines)
formatted_text = format_text_for_html(user_lines)

if not formatted_text:
    print("\nNo text was entered. Exiting.")
    exit()

# --- Step 5: Create the HTML and CSS template ---
html_template = f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @font-face {{
            font-family: 'Anek Malayalam';
            src: url('{font_path}'); /* Using the full path to the font now */
        }}
        body {{
            font-family: 'Anek Malayalam', sans-serif;
            font-size: 13pt; 
            margin: 1.5cm; 
        }}
        p {{
            margin-top: 0;
            margin-bottom: 0.2em;
            line-height: 1.3;
        }}
        .question {{
            margin-top: 0.8em; 
        }}
    </style>
</head>
<body>
    {formatted_text}
</body>
</html>
"""

# --- Step 6: Generate the PDF and the TXT file ---
print(f"\nCreating PDF and TXT files in '{quiz_folder_path}'...")
try:
    # We must provide the base_url so WeasyPrint knows where to find the font file
    html = weasyprint.HTML(string=html_template, base_url=download_folder)
    html.write_pdf(output_pdf_path)

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(user_text_for_txt)

    print("\n--- SUCCESS! ---")
    print(f"Files created successfully.")
    print(f"Saved in folder: '{quiz_folder_path}'")

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An error occurred: {e}")
    print("\nTROUBLESHOOTING:")
    print("1. Make sure the Python app (e.g., Termux, Pydroid) has storage permissions.")
    print("2. In Termux, you may need to run the command 'termux-setup-storage' first.")
