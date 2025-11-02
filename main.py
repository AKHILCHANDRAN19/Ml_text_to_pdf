import weasyprint
import os
import re

# --- Configuration: Set up all the paths ---
base_storage_path = '/storage/emulated/0' 
quiz_folder_name = 'Quiz'
quiz_folder_path = os.path.join(base_storage_path, quiz_folder_name)

# --- Path for the font ---
download_folder = '/storage/emulated/0/Download'
font_filename = 'AnekMalayalam-Bold.ttf'
font_path = os.path.join(download_folder, font_filename)

# --- This function remains the same ---
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

# --- Step 1: Perform initial setup (run only once) ---
# Create the 'Quiz' folder if it doesn't exist
if not os.path.exists(quiz_folder_path):
    print(f"Creating folder at: '{quiz_folder_path}'...")
    os.makedirs(quiz_folder_path)

# Check if the required font exists before starting the loop
if not os.path.exists(font_path):
    print(f"--- ERROR ---")
    print(f"Font file not found: '{font_filename}'")
    print(f"Please make sure it is in your Download folder: '{download_folder}'")
    exit()

# --- Main Loop to create multiple files ---
# This will now run forever until you stop it with Ctrl + C
while True:
    # --- Step 2: Get text input from the user ---
    print("\n\n--- Starting New File ---")
    print("Paste your text below. Type 'END' on a new line and press Enter to finish.")
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
        print("\nNo text was entered. Please try again.")
        continue # Skips to the next iteration of the main loop

    # --- Step 3: Ask for a filename (title) ---
    base_filename = input("Enter a title for your quiz files (e.g., 'Chapter_1_Quiz'): ")
    output_pdf_filename = f'{base_filename}.pdf'
    output_txt_filename = f'{base_filename}.txt'

    output_pdf_path = os.path.join(quiz_folder_path, output_pdf_filename)
    output_txt_path = os.path.join(quiz_folder_path, output_txt_filename)

    # --- Step 4: Create the HTML and CSS template ---
    html_template = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @font-face {{
                font-family: 'Anek Malayalam';
                src: url('{font_path}');
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

    # --- Step 5: Generate the PDF and the TXT file ---
    print(f"\nCreating files in '{quiz_folder_path}'...")
    try:
        html = weasyprint.HTML(string=html_template, base_url=download_folder)
        html.write_pdf(output_pdf_path)

        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(user_text_for_txt)

        # --- UPDATED SUCCESS MESSAGE ---
        print("\n--- SUCCESS! ---")
        print(f"PDF saved as: '{output_pdf_filename}'")
        print(f"TXT saved as: '{output_txt_filename}'")
        print(f"Saved in folder: '{quiz_folder_path}'")

    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"An error occurred: {e}")
        print("\nTROUBLESHOOTING:")
        print("1. Make sure the Python app has storage permissions.")
        print("2. In Termux, you may need to run 'termux-setup-storage' first.")
    
    # The loop will now automatically restart. Press Ctrl + C to exit.
