import customtkinter as ctk
import shutil
import cv2
import os
import threading
import time
import ffmpeg
import PyPDF2
import fitz
import pywinstyles
from tkinter import filedialog
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk

# UI

# Tab 1
def show_pdf_to_other_format():
    clear_frame(right_frame)

    # Title label
    label = ctk.CTkLabel(right_frame, text="PDF to Word, PNG, JPG Conversion", font=("Arial", 18))
    label.pack(padx=40, pady=10)
    
    # PDF File input row
    pdf_file_frame = ctk.CTkFrame(right_frame)
    pdf_file_frame.pack(pady=10, padx=40, fill="x")

    # Entry to display the selected PDF file location
    pdf_file_entry = ctk.CTkEntry(pdf_file_frame, width=300)
    pdf_file_entry.pack(side="left", fill="x", expand=True)
    pdf_file_entry.insert(0, "No file selected")

    # Button to select PDF
    pdf_file_button = ctk.CTkButton(pdf_file_frame, text="Select a File", command=lambda: select_file(pdf_file_entry, "pdf"))
    pdf_file_button.pack()

    # Output format selection row
    format_frame = ctk.CTkFrame(right_frame, fg_color=right_frame.cget("fg_color"))
    format_frame.pack(pady=10, padx=40)

    #Label for output format selection
    format_label = ctk.CTkLabel(format_frame, text="Select output format: ", font=("Arial",14))
    format_label.pack(side="left")
    
    # Segmented button for output format selection
    format_options = ["Word", "PNG", "JPEG"]
    format_segmented_button = ctk.CTkSegmentedButton(format_frame, values=format_options)
    format_segmented_button.pack()

    
    # Progress bar (initially hidden)
    progress_bar = ctk.CTkProgressBar(right_frame, width=300, height=20)
    progress_bar.pack(pady=10)
    progress_bar.set(0)  # Initialize progress
    progress_bar.pack_forget()  # Hide it initially

    # Convert button
    convert_button = ctk.CTkButton(right_frame, text="Convert", command=lambda: start_conversion_pdf(pdf_file_entry, format_segmented_button, convert_button, progress_bar))
    convert_button.pack(pady=20)

# Tab 2
def show_video_conversion():
    clear_frame(right_frame)

    # Title label
    label = ctk.CTkLabel(right_frame, text="Video Conversion", font=("Arial", 18))
    label.pack(padx=40, pady=10)
    
    # PDF File input row
    video_file_frame = ctk.CTkFrame(right_frame)
    video_file_frame.pack(pady=10, padx=40, fill="x")

    # Entry to display the selected PDF file location
    video_file_entry = ctk.CTkEntry(video_file_frame, width=300)
    video_file_entry.pack(side="left", fill="x", expand=True)
    video_file_entry.insert(0, "No file selected")

    # Button to select file
    video_file_button = ctk.CTkButton(video_file_frame, text="Select a File", command=lambda: select_file(video_file_entry, "video"))
    video_file_button.pack()

    # Output format selection row
    format_frame = ctk.CTkFrame(right_frame, fg_color=right_frame.cget("fg_color"))
    format_frame.pack(pady=10, padx=40)

    #Label for output format selection
    format_label = ctk.CTkLabel(format_frame, text="Select output format: ", font=("Arial",14))
    format_label.pack(side="left")

    # Segmented button for output format selection
    format_options = ['avi', 'mp4', 'mov', 'mkv', 'flv', 'webm', 'wmv']
    format_segmented_button = ctk.CTkSegmentedButton(format_frame, values=format_options)
    format_segmented_button.pack()

    
    # Progress bar (initially hidden)
    progress_bar = ctk.CTkProgressBar(right_frame, width=300, height=20)
    progress_bar.pack(pady=10)
    progress_bar.set(0)  # Initialize progress
    progress_bar.pack_forget()  # Hide it initially

    # Convert button
    convert_button = ctk.CTkButton(right_frame, text="Convert", command=lambda: start_conversion_video(video_file_entry, format_segmented_button, convert_button, progress_bar))
    convert_button.pack(pady=20)

# Tab 3
def show_pdf_editing():
    clear_frame(right_frame)

    # Frame for widgets
    pdf_frame = ctk.CTkFrame(right_frame, fg_color=right_frame.cget("fg_color"))
    pdf_frame.pack(fill="x")

    # Button Frame
    button_frame = ctk.CTkFrame(pdf_frame)
    button_frame.pack(fill="x")

    # Content Frame
    content_frame = ctk.CTkFrame(right_frame, fg_color=right_frame.cget("fg_color"))
    content_frame.pack(fill="both", expand=True)
    
    # Add buttons
    button1 = ctk.CTkButton(button_frame, text="Merge PDF", command=lambda: merge_pdf(content_frame))
    button1.pack(side="left", fill="x", expand=True)

    button2 = ctk.CTkButton(button_frame, text="Insert Page", command=lambda: insert_pdf_page(content_frame))
    button2.pack(side="left", fill="x", expand=True)

    button3 = ctk.CTkButton(button_frame, text="Remove Page", command=lambda: remove_pdf_page(content_frame))
    button3.pack(side="left", fill="x", expand=True)

    # Show the first content by default (Merge Pdf)
    merge_pdf(content_frame)

# Function to display content for PDF Conversion
def merge_pdf(frame):

    def drop_func(files):
        # Normalize each file path and ensure it's valid
        normalized_paths = [os.path.normpath(file_path) for file_path in files]
        file_str = ', '.join(normalized_paths)
        pdf_file_entry2.delete(0, ctk.END)  
        pdf_file_entry2.insert(0, file_str)
    
    clear_frame(frame)

    label1 = ctk.CTkLabel(frame, text="Select Base Pdf: ", font=("Arial", 18))
    label1.pack(padx=40, pady=5, anchor="w")

    # Base PDF File input row for PDF Conversion
    pdf_merge_frame1 = ctk.CTkFrame(frame)
    pdf_merge_frame1.pack(pady=10, padx=40, fill="x")

    # Entry to display the selected PDF file location
    pdf_file_entry1 = ctk.CTkEntry(pdf_merge_frame1, width=300)
    pdf_file_entry1.pack(side="left", fill="x", expand=True)
    pdf_file_entry1.insert(0, "No file selected")

    # Select PDF Button
    pdf_file_button = ctk.CTkButton(pdf_merge_frame1, text="Select a File", command=lambda: select_file(pdf_file_entry1, "pdf"))
    pdf_file_button.pack()

    label2 = ctk.CTkLabel(frame, text="Select other Pdf: ", font=("Arial", 18))
    label2.pack(padx=40, pady=5, anchor="w")

    # Other PDF File input row for PDF Conversion
    pdf_merge_frame2 = ctk.CTkFrame(frame)
    pdf_merge_frame2.pack(pady=5, padx=40, fill="x")

    # Entry to display the selected PDF file location
    pdf_file_entry2 = ctk.CTkEntry(pdf_merge_frame2, width=300)
    pdf_file_entry2.pack(side="left", fill="x", expand=True)
    pdf_file_entry2.insert(0, "No file selected")

    # Drag and Drop
    dnd = ctk.CTkFrame(frame)
    dnd.pack()

    canvas = ctk.CTkCanvas(dnd, bg=app.cget("fg_color")[0], highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    create_dotted_border(canvas, 5, 5, 352, 262, dot_size=5, spacing=5)
    pywinstyles.apply_dnd(canvas, drop_func)
    

    image = ctk.CTkImage(light_image=Image.open("assets/dnd.png"), dark_image=Image.open("assets/dnd.png"), size=(60, 60))
    image_label = ctk.CTkLabel(canvas, image=image, text="")
    image_label.pack(pady=10)

    label3= ctk.CTkLabel(canvas, text="Drag and drop your files here", font=("Arial", 16), text_color="#1E90FF")
    label3.pack(padx=40, pady=10, anchor="w")

    label4= ctk.CTkLabel(canvas, text="Or", font=("Arial", 14), text_color="#1E90FF")
    label4.pack()

    # Select PDF Button
    pdf_file_button = ctk.CTkButton(canvas, text="Select a File", command=lambda: select_file(pdf_file_entry2, "pdf"))
    pdf_file_button.pack(pady=15)
    
    # Merge Button
    merge_button = ctk.CTkButton(frame, text="Merge", command=lambda: merge(pdf_file_entry1, pdf_file_entry2))
    merge_button.pack(pady=10)

# Function to display content for Video Conversion
def insert_pdf_page(frame):
    clear_frame(frame)
    
    # Title for PDF Conversion section
    label = ctk.CTkLabel(frame, text="Insert pages in PDF", font=("Arial", 18))
    label.pack(pady=10)

    label1 = ctk.CTkLabel(frame, text="Select Pdf: ", font=("Arial", 18))
    label1.pack(padx=40, pady=10, anchor="w")

    # Base PDF File input row for PDF Conversion
    pdf_insert_frame1 = ctk.CTkFrame(frame)
    pdf_insert_frame1.pack(pady=10, padx=40, fill="x")

    # Entry to display the selected PDF file location
    pdf_file_entry1 = ctk.CTkEntry(pdf_insert_frame1, width=300)
    pdf_file_entry1.pack(side="left", fill="x", expand=True)
    pdf_file_entry1.insert(0, "No file selected")

    # Select PDF Button
    pdf_file_button = ctk.CTkButton(pdf_insert_frame1, text="Select a File", command=lambda: select_file(pdf_file_entry1, "pdf"))
    pdf_file_button.pack()

    # Page to be removed
    pdf_insert_frame2 = ctk.CTkFrame(frame)
    pdf_insert_frame2.pack(pady=10, padx=40, fill="x")

    # Label to display text
    label2 = ctk.CTkLabel(pdf_insert_frame2, text="Enter page number to be insert new page: ", font=("Arial", 18))
    label2.pack(padx=40, pady=10, side="left")
    
    # Entry to receive the page number
    pdf_file_entry2 = ctk.CTkEntry(pdf_insert_frame2, width=300)
    pdf_file_entry2.pack(side="left", fill="x", expand=True)
    pdf_file_entry2.insert(0, "0")

    #Label to show text
    label2 = ctk.CTkLabel(frame, text="Select Page: ", font=("Arial", 18))
    label2.pack(padx=40, pady=10, anchor="w")

    # Other PDF File input row for PDF Conversion
    pdf_insert_frame3 = ctk.CTkFrame(frame)
    pdf_insert_frame3.pack(pady=10, padx=40, fill="x")

    # Entry to display the selected PDF file location
    pdf_file_entry3 = ctk.CTkEntry(pdf_insert_frame3, width=300)
    pdf_file_entry3.pack(side="left", fill="x", expand=True)
    pdf_file_entry3.insert(0, "No file selected")

    # Select PDF Button
    pdf_file_button = ctk.CTkButton(pdf_insert_frame3, text="Select a File", command=lambda: select_file(pdf_file_entry3, "pdf"))
    pdf_file_button.pack()

    # Insert Button
    merge_button = ctk.CTkButton(frame, text="Insert", command=lambda: insert_page(pdf_file_entry1, pdf_file_entry2, pdf_file_entry3))
    merge_button.pack()



# Function to display content for PDF Operations
def remove_pdf_page(frame):
    clear_frame(frame)
    
    # Title for PDF Conversion section
    label = ctk.CTkLabel(frame, text="Remove pages in PDF", font=("Arial", 18))
    label.pack(pady=10)

    label1 = ctk.CTkLabel(frame, text="Select Pdf: ", font=("Arial", 18))
    label1.pack(padx=40, pady=10, anchor="w")

    # Base PDF File input row for PDF Conversion
    pdf_remove_frame1 = ctk.CTkFrame(frame)
    pdf_remove_frame1.pack(pady=10, padx=40, fill="x")

    # Entry to display the selected PDF file location
    pdf_file_entry1 = ctk.CTkEntry(pdf_remove_frame1, width=300)
    pdf_file_entry1.pack(side="left", fill="x", expand=True)
    pdf_file_entry1.insert(0, "No file selected")

    # Select PDF Button
    pdf_file_button = ctk.CTkButton(pdf_remove_frame1, text="Select a File", command=lambda: select_file(pdf_file_entry1, "pdf"))
    pdf_file_button.pack()

    # Page to be removed
    pdf_remove_frame2 = ctk.CTkFrame(frame)
    pdf_remove_frame2.pack(pady=10, padx=40, fill="x")

    # Label to display text
    label2 = ctk.CTkLabel(pdf_remove_frame2, text="Enter page number to be deleted: ", font=("Arial", 18))
    label2.pack(padx=40, pady=10, side="left")
    
    # Entry to receive the page number
    pdf_file_entry2 = ctk.CTkEntry(pdf_remove_frame2, width=300)
    pdf_file_entry2.pack(side="left", fill="x", expand=True)
    pdf_file_entry2.insert(0, "0")

    # Remove Button
    merge_button = ctk.CTkButton(frame, text="Remove", command=lambda: remove_page(pdf_file_entry1, pdf_file_entry2))
    merge_button.pack()


# Conversion related functions

# Pdf Converter

def start_conversion_pdf(input_file, output_format, convert_button, progress_bar):
    file_path = input_file.get()
    selected_format = output_format.get()

    if file_path == "No file selected" or not file_path:
        CTkMessagebox(title="Error", message="Please select a PDF file", icon="warning")
        return

    if selected_format not in ["Word", "PNG", "JPEG"]:
        CTkMessagebox(title="Error", message="Please select a valid output format", icon="warning")
        return

    # Show the progress bar during conversion
    progress_bar.pack(pady=10)
    progress_bar.set(0)  # Reset progress bar

    # Simulate the conversion process
    convert_button.configure(state="disabled")
    try:
        # Output path for saving the converted file
        output_path = os.path.splitext(file_path)[0]

        if selected_format == "Word":
            # Convert PDF to Word (DOCX)
            converter = Converter(file_path)
            converter.convert(output_path + ".docx")
            converter.close()
            

        elif selected_format in ["PNG", "JPEG"]:
            # Convert PDF to images (PNG/JPG)
            pdf_document = fitz.open(file_path)
            images = []

            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                output_filename = f"{file_path[:-4]}_page_{page_number + 1}.{selected_format.lower()}"
                img.save(output_filename, format=selected_format.lower())
                images.append(output_filename)
    
            pdf_document.close()
        update_progress_bar(progress_bar, convert_button)
        
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An error occurred during conversion: {str(e)}", icon="warning")
        convert_button.configure(state="normal")  # Enable the button in case of an error

# Function for Video Conversion

def start_conversion_video(input_file, output_format_button, convert_button, progress_bar):
    input_file_path = input_file.get()
    output_format = output_format_button.get()
    
    if not input_file_path:
        messagebox.showerror("Error", "Please select a video file.")
        return
    
    # List of supported input formats (based on OpenCV's capabilities and FFmpeg)
    supported_input_formats = ['.avi', '.mp4', '.mov', '.mkv', '.flv', '.webm', '.wmv', '.mpeg', '.3gp', '.ogv', '.asf']
    
    # Check if the input file format is supported
    if not any(input_file_path.endswith(ext) for ext in supported_input_formats):
        CTkMessagebox(title="Error", message="Unsupported input file format.", icon="warning")
        return

        
    progress_bar.pack(pady=10)
    progress_bar.set(0)  # Reset progress bar

    output_file = os.path.splitext(input_file_path)[0] + f'.{output_format}'

    # Simulate the conversion process
    convert_button.configure(state="disabled")  # Disable the Convert button during conversion
    update_progress_bar(progress_bar, convert_button)

    try:
        # Open the input video file
        cap = cv2.VideoCapture(input_file_path)
        if not cap.isOpened():
            CTkMessagebox(title="Error", message="Could not open the video file.", icon="cancel")
            return

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the codec for the output format
        if output_format == 'mp4':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # H.264 codec for .mp4
        elif output_format == 'avi':
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Xvid codec for .avi
        elif output_format == 'mov':
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # H.264 codec for .mov
        elif output_format == 'mkv':
            fourcc = cv2.VideoWriter_fourcc(*'vp80')  # VP8 codec for .mkv
        elif output_format == 'flv':
            fourcc = cv2.VideoWriter_fourcc(*'FLV1')  # FLV codec for .flv
        elif output_format == 'webm':
            fourcc = cv2.VideoWriter_fourcc(*'vp80')  # VP8 codec for .webm
        elif output_format == 'wmv':
            fourcc = cv2.VideoWriter_fourcc(*'WMV2')  # WMV codec for .wmv
        else:
            CTkMessagebox(title="Error", message=f"Unsupported output format: {output_format}", icon="cancel")
            return

        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Read and write frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        # Release everything
        cap.release()
        out.release()
        
    except Exception as e:
        CTkMessagebox(title="Error", message=str(e), icon="cancel")

# Pdf Editing

def merge(pdf_file_entry1, pdf_file_entry2):
    # Get the file paths from the entry widgets
    pdf_file_path1 = pdf_file_entry1.get()
    pdf_file_paths2 = pdf_file_entry2.get()

    if pdf_file_path1 == "No file selected" or pdf_file_paths2 == "No file selected":
        CTkMessagebox(title="Error", message="Please select at least one PDF file.", icon="warning")
        return

    # Get the list of files from the second entry (multiple file paths)
    pdf_files2 = pdf_file_paths2.split(", ")

    try:
        
        base_name = os.path.splitext(os.path.basename(pdf_file_path1))[0]
        directory = os.path.dirname(pdf_file_path1)
        
        # Open the base PDF
        with open(pdf_file_path1, "rb") as pdf1:
            # Create PDF reader for the base file
            pdf_reader1 = PyPDF2.PdfReader(pdf1)

            # Create a PDF writer object to save the merged PDF
            pdf_writer = PyPDF2.PdfWriter()

            # Add pages from the first PDF (base PDF)
            for page_num in range(len(pdf_reader1.pages)):
                pdf_writer.add_page(pdf_reader1.pages[page_num])

            # Loop through all selected PDFs in the second input
            for pdf_file_path in pdf_files2:
                with open(pdf_file_path, "rb") as pdf2:
                    # Create a PDF reader for each selected file
                    pdf_reader2 = PyPDF2.PdfReader(pdf2)

                    # Add pages from the second PDF
                    for page_num in range(len(pdf_reader2.pages)):
                        pdf_writer.add_page(pdf_reader2.pages[page_num])


            merged_file_name = f"{base_name}_merged.pdf"
            merged_file_path = os.path.join(directory, merged_file_name)
            
            
            # Save the merged PDF to a new file
            with open(merged_file_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)


            CTkMessagebox(title="Success", message="PDFs merged successfully.", icon="check")
        
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")


def insert_page(pdf_file_entry1, pdf_file_entry2, pdf_file_entry3):
    pdf_file_path1 = pdf_file_entry1.get()
    page_no = pdf_file_entry2.get()
    page_file_path2 = pdf_file_entry3.get()

    if pdf_file_path1 == "No file selected" or pdf_file_path3 == "No file selected":
        CTkMessagebox(title="Error", message="Please select at least one PDF file.", icon="warning")
        return
    elif (int(page_no) <= 0):
        CTkMessagebox(title="Error", message="Select a valid page number", icon="warning")
        return
    
    base_reader = PdfReader(pdf_file_path1)
    insert_reader = PdfReader(page_file_path2)

    if (int(page_no) > len(reader.pages)):
        CTkMessagebox(title="Error", message="Selected page number does not exist", icon="warning")
        return
    
    # Extract the page number where to insert (convert to 0-indexed)
    insert_position = int(page_no) - 1  # Make it 0-indexed
    
    # Create a PdfWriter object to write the new PDF
    writer = PdfWriter()
    
    # Add pages from the base PDF (entry1) up to the insertion point
    for page_num in range(insert_position):
        writer.add_page(base_reader.pages[page_num])
    
    # Insert the page from the second PDF (entry3)
    writer.add_page(insert_reader.pages[0])  # Only insert the first page of entry3
    
    # Add the remaining pages from the base PDF (entry1)
    for page_num in range(insert_position, len(base_reader.pages)):
        writer.add_page(base_reader.pages[page_num])

    # Modify the output file name to append "_modified" before the ".pdf" extension
    output_pdf = pdf_file_path1.replace(".pdf", "_modified.pdf")
    
    # Write the modified PDF to the new file
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    # Show info message with the new file name
    CTkMessagebox(title=f"Page inserted at position {page_no}.", message=f"New PDF saved as '{output_pdf}'.", icon="info")

def remove_page(pdf_file_entry1, pdf_file_entry2):
    # Get the file paths from the entry widgets
    pdf_file_path1 = pdf_file_entry1.get()
    page_no = pdf_file_entry2.get()

    if pdf_file_path1 == "No file selected":
        CTkMessagebox(title="Error", message="Please select at least one PDF file.", icon="warning")
        return
    elif (int(page_no) <= 0):
        CTkMessagebox(title="Error", message="Select a valid page number", icon="cancel")
        return
        
    # Load the PDFs
    reader = PdfReader(pdf_file_path1)

    if (int(page_no) > len(reader.pages)):
        CTkMessagebox(title="Error", message="Selected page number does not exist", icon="warning")
        return
    
    # Extract the page number to remove from entry2
    page_to_remove = int(page_no) - 1  # Page numbers are 0-indexed
    
    # Create a PdfWriter object to write the new PDF
    writer = PdfWriter()

    # Add pages from entry1, skipping the page to remove
    for page_num in range(len(reader.pages)):
        if page_num != page_to_remove:
            writer.add_page(reader.pages[page_num])

    # Write the modified PDF to a new file
    output_pdf = pdf_file_path1
    output_pdf = output_pdf.replace(".pdf","_modified.pdf")
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    CTkMessagebox(title=f"Page {page_no} removed",message=f"New PDF saved as '{output_pdf}'.", icon="info")


# Other Functions
def create_dotted_border(canvas, x1, y1, x2, y2, dot_size=5, spacing=3):
    # Draw a dotted rectangle border on the canvas.
    
    # Top border (dotted)
    for i in range(x1, x2, dot_size + spacing):
        canvas.create_oval(i, y1, i + dot_size, y1 + dot_size, outline="black", fill="black")
    
    # Bottom border (dotted)
    for i in range(x1, x2, dot_size + spacing):
        canvas.create_oval(i, y2 - dot_size, i + dot_size, y2, outline="black", fill="black")
    
    # Left border (dotted)
    for i in range(y1, y2, dot_size + spacing):
        canvas.create_oval(x1, i, x1 + dot_size, i + dot_size, outline="black", fill="black")
    
    # Right border (dotted)
    for i in range(y1, y2, dot_size + spacing):
        canvas.create_oval(x2 - dot_size, i, x2, i + dot_size, outline="black", fill="black")


def update_progress_bar(progress_bar, convert_button):
    # Function to update the progress bar
    def simulate_progress():
        for i in range(1, 101):
            progress_bar.set(i / 100)  # Update progress bar
            time.sleep(0.01)  # Simulate work being done
        progress_bar.after(0, on_thread_done)  # Call after thread finishes

    def on_thread_done():
        convert_button.configure(state="enabled")
        CTkMessagebox(title="Success",message="File converted Successfully!", icon="check", fade_in_duration= 2)
    # Run the progress simulation in a separate thread to avoid blocking the main UI thread
    threading.Thread(target=simulate_progress, daemon=True).start()


# Function to change content based on button click
def change_content(button_id):
    if button_id == 1:
        show_pdf_to_other_format()
    elif button_id == 2:
        show_video_conversion()
    elif button_id == 3:
        show_pdf_editing()

# Function to select file
def select_file(file_entry, input_type):
    # Function to select a PDF file (open file dialog)
    if (input_type=="pdf"):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    elif (input_type=="video"):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Video Files", "*.avi;*.mp4;*.mov;*.mkv;*.flv;*.webm;*.wmv"), ("All Files", "*.*")])

    if file_path:
        file_entry.delete(0, ctk.END)  # Clear the entry field
        file_entry.insert(0, file_path)  # Set the selected file path

    
# Function to clear the right section for new content
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Function to toggle theme
def toggle_theme():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        theme_toggle.configure(text="Light Theme")
    else:
        ctk.set_appearance_mode("Dark")
        theme_toggle.configure(text="Dark Theme")

# Initialize the main window
app = ctk.CTk()
app.geometry("800x500")
app.title("File Converter")
app.resizable(width=False, height=False)
app.iconbitmap("assets/arrow.ico")

# Create a left frame for buttons
left_frame = ctk.CTkFrame(app, width=200, height=500, corner_radius=10)
left_frame.pack(side="left", fill="y", padx=20, pady=20)

#Image
image = ctk.CTkImage(light_image=Image.open("assets/arrow.png"),
                                  dark_image=Image.open("assets/arrow.png"),
                                  size=(50, 50))
image_label = ctk.CTkLabel(left_frame, image=image, text="")
image_label.pack(pady=25)

# Create 4 buttons inside the left frame
button1 = ctk.CTkButton(left_frame, text="PDF Conversion", command=lambda: change_content(1))
button1.pack(pady=10, padx=20, fill="x")

button2 = ctk.CTkButton(left_frame, text="Video Conversion", command=lambda: change_content(2))
button2.pack(pady=10, padx=20, fill="x")

button3 = ctk.CTkButton(left_frame, text="PDF Operations", command=lambda: change_content(3))
button3.pack(pady=10, padx=20, fill="x")

# Add toggle theme button at the bottom
theme_toggle = ctk.CTkSwitch(left_frame, text="Light Theme", command=toggle_theme)
theme_toggle.pack(side="bottom", pady=20, padx=20, fill="x")

# Create the right section for content display
right_frame = ctk.CTkFrame(app, corner_radius=20)
right_frame.pack(side="right", fill="both", expand=True, pady=20, padx=15)


# Default

label = ctk.CTkLabel(right_frame, text="Convert and edit your files", font=("Arial", 28))
label.pack(fill="both", expand=True, padx=0, pady=0)
    
# Start the app
app.mainloop()
