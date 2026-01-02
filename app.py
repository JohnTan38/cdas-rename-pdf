import datetime as datetime #rename pdf files, move to folder
import glob, os, os.path
import tkinter as tk
from tkinter import ttk
import shutil
import time

def get_yesterday_date():
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            return yesterday

def get_username_date_to_download():
    window = tk.Tk()
    window.title("CDAS User Input")

    input_labels = ["Username", "Date_To_Rename"]
    for i, label in enumerate(input_labels):
        ttk.Label(window, text=label).grid(row=0, column=i, padx=10, pady=5, sticky='s')

    entries = {'username': [], 'date_to_download': []} #, 'start_time': [], 'finish_time': []
    list_username_date_to_download =[]

    def get_user_input():
        for row in range(len(entries['username'])):
            username = entries['username'][row].get()
            date_to_download = entries['date_to_download'][row].get()

    for row in range(1, 2):
            username_var = tk.StringVar()
            username_entry = ttk.Entry(window, textvariable=username_var)
            username_entry.grid(row=row, column=0, padx=10, pady=5)
            entries['username'].append(username_var)

            date_to_download_var = tk.StringVar()
            date_to_download_entry = ttk.Entry(window, textvariable=date_to_download_var)
            date_to_download_entry.grid(row=row, column=1, padx=10, pady=5)
            entries['date_to_download'].append(date_to_download_var)

    submit_button = tk.Button(window, text="Submit", command=get_user_input)
    submit_button.grid(row=14, column=0, columnspan=2, pady=10)

    window.mainloop()
    list_username_date_to_download.append(entries['username'][0].get())
    list_username_date_to_download.append(entries['date_to_download'][0].get())
    print(list_username_date_to_download)
    return list_username_date_to_download


username = str(get_username_date_to_download()[0]) #'rpa.uat'
date_to_download = str(get_username_date_to_download()[1])
file_path_rename = r'C:/Users/'+ username+ r'/Downloads/cdas_merged/'
pdf_files = [f for f in os.listdir(file_path_rename) if (f.lower().endswith('.pdf'))]
#print(pdf_files)
if not pdf_files:
            print(f"Error check: No PDF files found in the directory '{file_path_rename}'.")
                
# define function to rename pdf file in dir
def rename_pdf_in_dir(file_path, pdf_file, date_to_download):
            """
            Renames a PDF file in the specified directory.
            Args:
                file_path (str): The full path to the directory containing the PDF file.
                file_name (str): The new name for the PDF file (without the .pdf extension).
            Returns:
                str: A message indicating success or failure.
         """
            try:
                # Check if the directory exists
                if not os.path.exists(file_path):
                    return f"Error: The directory '{file_path}' does not exist."

                # Find the first PDF file in the directory
                #pdf_files = [f for f in os.listdir(file_path) if f.lower().endswith('.pdf')]
                #if not pdf_files:
                    #return f"Error: No PDF files found in the directory '{file_path}'."

                #yesterday_date = str(get_yesterday_date()).replace('-', '')
                date_to_download = date_to_download

                pdf_file_path = os.path.join(file_path, pdf_file)
                old_file_name = pdf_file
                #old_file_name = old_file_name.replace('.pdf', '')
                old_file_path = os.path.join(file_path, old_file_name)                

                # Create the new file name with .pdf extension
                new_file_name = f"{old_file_name}_{date_to_download}.pdf"
                new_file_path = os.path.join(file_path, new_file_name)
                

                # Check if a file with the new name already exists
                if os.path.exists(new_file_path):
                    return f"Error: A file with the name '{new_file_name}' already exists in '{file_path}'."

                # Rename the file
                os.rename(old_file_path, new_file_path)
                return f"Success: File '{old_file_name}' renamed to '{new_file_name}' in '{file_path}'."

            except Exception as e:
                return f"Error: An unexpected error occurred - {str(e)}"

rename_pdf =0 
for pdf_file in pdf_files:
            try:                  
                    rename_pdf_in_dir(file_path_rename, pdf_file, date_to_download)
                    rename_pdf += 1
            except Exception as e:
                    print(e)
                    break
print(f"Total PDF files renamed: {rename_pdf}")


def check_folder_exists(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path

dest_dir = check_folder_exists(file_path_rename + date_to_download + '/')

def move_pdf_to_date_folder(src_dir, dest_dir, date_to_download):
        """
        Moves a PDF file from the source directory to the destination directory.
        Args:
            src_dir (str): The full path to the source directory containing the PDF file.
            dest_dir (str): The full path to the destination directory where the PDF file will be moved.
        Returns:
            str: A message indicating success or failure.
        """
        try:
            # Check if the source directory exists
            if not os.path.exists(src_dir):
                return f"Error: Source directory '{src_dir}' does not exist."

            # Check if the destination directory exists; if not, create it
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)  # Create the destination directory if it doesn't exist
                print(f"Info: Destination directory '{dest_dir}' created.")

            # Find the first PDF file in the source directory
            pdf_files = [f for f in os.listdir(src_dir) if (f.lower().endswith('.pdf') and date_to_download in f)]
            if not pdf_files:
                return f"Error: No PDF files found in the source directory '{src_dir}'."
            
            # Get the first PDF file (assuming there's only one PDF file to move)
            for pdf_file in pdf_files:
                pdf_file_name = pdf_file#pdf_files[0]
                src_file_path = os.path.join(src_dir, pdf_file_name)
                dest_file_path = os.path.join(dest_dir, pdf_file_name)

                # Check if a file with the same name already exists in the destination directory
                if os.path.exists(dest_file_path):
                    return f"Error: A file with the name '{pdf_file_name}' already exists in '{dest_dir}'."

                # Copy and Move the file
                shutil.copy(src_file_path, dest_file_path)
                shutil.move(src_file_path, dest_file_path)
                return f"Success: File '{pdf_file_name}' moved from '{src_dir}' to '{dest_dir}'."

        except PermissionError:
            return f"Error: Permission denied. Check if you have the necessary permissions to access '{src_dir}' or '{dest_dir}'."
        except FileNotFoundError:
            return f"Error: The file '{pdf_file_name}' was not found in '{src_dir}'."
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"


for pdf_file in pdf_files:
        move_pdf_to_date_folder(file_path_rename, dest_dir, date_to_download)

