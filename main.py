import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class Interface(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # width and height of 800x600
        self.master.geometry("800x600")
        self.master.resizable(0, 0)
        # title of the window
        self.master.title("Organize your files")
        self.instruction_label = tk.Label(self, text="To use the program, follow these steps:")
        self.instruction_label.pack(pady=10)


class App:
    folder_paths_to_ignore = []
    ignore_folders = [".git", "venv", "env", "node_modules", "organized", "dist", "build", "migrations", "static", "templates", "media", "logs", "bin", "lib", "include", "share", "src", "tests", "docs",
                        "data", "assets", "public", "node_modules", "dist", "build", "migrations", "static", "templates", "media", "logs", "bin", "lib", "include", "share", "src", "tests", "docs", "data", "assets", "public"]
    folder_path = None
    folder_path_to_save = None
    button_yes_ignore_clicked = False
    button_yes_clicked = False
    
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.create_log_frame()

    def create_widgets(self):
        """ Create the widgets of the interface"""

        # create a button to ask where to organize the files
        self.folder_button = ttk.Button(
            self.root, text="1. Select Folder", command=self.browse_folder)
        self.folder_button.pack(pady=5)

        # create a button to ask where to save the organized files
        self.folder_to_save = ttk.Button(
            self.root, text="2. Select the folder to save the files", command=self.save_folder)
        self.folder_to_save.pack(pady=5)

        # create a button to ask if the user wants to ignore some folders
        self.folder_to_ignore = ttk.Button(
            self.root, text="3. Do you want to ignore folders?", command=self.show_folders_to_ignore)
        self.folder_to_ignore.pack(pady=5)

        # create a button to organize the files
        self.organize_button = ttk.Button(
            self.root, text="4. Organize", command=self.organize_your_files)
        self.organize_button.pack(pady=10)
        self.organize_button.configure(state=tk.DISABLED)

    def create_log_frame(self):
        """ Create the log frame and the log label"""

        self.log_label = tk.Label(self.root, text="Logs")
        self.log_label.pack(pady=10)

        self.log_frame = tk.Frame(self.root)
        self.log_frame.pack(pady=10)
        self.log_text = tk.Text(self.log_frame, width=80, height=20)
        self.log_text.pack()

    def browse_folder(self):
        """ Browse the folder to organize"""

        current_dir = os.getcwd()
        self.folder_path = filedialog.askdirectory(initialdir=current_dir)
        if self.folder_path:

            self.log_step("Carpeta seleccionada: " + self.folder_path)

    def save_folder(self):
        """ Select the folder to save the organized files"""

        self.folder_path_to_save = filedialog.askdirectory()
        if self.folder_path_to_save:
            os.chdir(self.folder_path_to_save)  # change the current directory
            self.folder_to_ignore.configure(state=tk.NORMAL)
            self.log_step("Selected folder to save: " +
                          self.folder_path_to_save)

    def select_folders_to_ignore(self, pop):
        """ Select the folders to ignore"""

        while True:
            folder_path = filedialog.askdirectory()
            if folder_path:
                self.folder_paths_to_ignore.append(folder_path)
            else:
                break

        if self.folder_paths_to_ignore:
            self.log_step("Selected folders to ignore:" +
                          ", ".join(self.folder_paths_to_ignore))
        
        self.organize_button.configure(state=tk.NORMAL)
        self.button_yes_ignore_clicked = True
        pop.destroy()

    def log_step(self, message):
        """Log a message in the log_text widget"""
        
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def organize_your_files(self):
        """Organize the files"""


        if not self.folder_path:
            messagebox.showerror(
                "Error", "No folder selected to organize")
            return
        if not self.folder_path_to_save:
            messagebox.showerror(
                "Error", "No folder was selected to save the files")
            return
        # if self.button_yes_ignore_clicked == False:
        #     messagebox.showerror(
        #         "Error", "No se seleccionó ninguna carpeta para ignorar")
        #     return
        self.log_step("\nOrganizing files...")
        self.log_step("\n")
        self.organize_folders(self.folder_path, self.folder_path_to_save, self.folder_paths_to_ignore)
        messagebox.showinfo("File Organization", "Everything was organized correctly!")

    def show_folders_to_ignore(self):
        """ Show a pop-up to ask if the user wants to ignore some folders"""

        popup = tk.Toplevel()
        popup.title("Ventana emergente")

        label = tk.Label(popup, text="Do you want to ignore any folder?")
        label.pack(padx=20, pady=20)

        button_frame = tk.Frame(popup)  # Create a frame to hold the buttons
        button_frame.pack()

        button_yes = tk.Button(button_frame, text="Yes",
                               command=lambda: self.select_folders_to_ignore(popup))
        button_yes.pack(side=tk.LEFT, padx=5)

        button_no = tk.Button(button_frame, text="No",
                              command=popup.destroy)
        button_no.pack(side=tk.LEFT, padx=5)
        
        popup.wait_window()

        if self.button_yes_ignore_clicked == False:
            self.organize_button.configure(state=tk.NORMAL)
            self.button_yes_ignore_clicked = True

    def show_overwrite_files(self, file):
        """ Show a pop-up to ask if the user wants to overwrite the files"""

        popup = tk.Toplevel()
        popup.title("Overwrite")

        label = tk.Label(popup, text="The following file is already in the destination folder: " + file)
        label.pack(padx=20, pady=20)

        label = tk.Label(popup, text="Do you want to overwrite it? ")
        label.pack(padx=20, pady=20)
        
        button_frame = tk.Frame(popup)  # Create a frame to hold the buttons
        button_frame.pack()

        self.button_yes_clicked = False

        button_yes = tk.Button(button_frame, text="Yes",
                            command=lambda: self.handle_overwrite_files(True, popup))
        button_yes.pack(side=tk.LEFT, padx=5)

        button_no = tk.Button(button_frame, text="No",
                            command=lambda: self.handle_overwrite_files(False, popup))
        button_no.pack(side=tk.LEFT, padx=5)
        
        popup.wait_window()

    def handle_overwrite_files(self, overwrite, popup):
        """Handle the user's choice on file rewriting"""

        if overwrite:
            self.button_yes_clicked = True

        popup.destroy()
            
    def organize_folders(self, current_directory, folder_to_save, folder_paths_to_ignore):
        """ Initialize the class"""

        current_directory = current_directory  # current directory
        self.folder_to_save = folder_to_save  # folder to save the organized files
        self.ignore_folders += folder_paths_to_ignore  # add the folders to ignore
        total_files_moved = self.organize_files(current_directory)

        if total_files_moved == 0:
            self.log_step("No files were moved. Everything is organized! ;)")
        else:
            # print(f"Se movieron {total_files_moved} archivos.")
            self.log_step(f"{total_files_moved} files were moved.")

        self.log_step("\nEnded process.")

    def organize_files(self, directory):
        """ Organize the files in the directory"""

        total_files_moved = 0
        organized_folder = self.create_folder(os.path.join(self.folder_to_save, "Organized"))

        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                if dir in self.ignore_folders:
                    dirs.remove(dir)
                    continue

            for file in files:
                if file == "main.py" or file == "interface.py" or os.path.isdir(file):
                    continue

                file_path = os.path.join(root, file)  # Actualizar esta línea
                name, extension_file = os.path.splitext(file)
                extension_file = extension_file.lower()

                folder_name = self.check_extension(extension_file[1:])
                file_moved = self.move_file_to_folder(
                    file_path, os.path.join(organized_folder, folder_name))

                if file_moved:
                    total_files_moved += 1

        return total_files_moved

    def move_file_to_folder(self, file_path, folder_name):

        if not os.path.exists(file_path):
            return False

        if os.path.dirname(file_path) == folder_name:
            return False

        if any(ignore_folder in os.path.dirname(file_path) for ignore_folder in self.ignore_folders):
            """ If the file is in a folder to ignore, don't move it"""
            return False

        destination_path = os.path.join(
            folder_name, os.path.basename(file_path))
        if os.path.abspath(file_path) == os.path.abspath(destination_path):
            return False

        if os.path.exists(destination_path):
            # selected_option = self.show_overwrite_files(file_path)
            self.show_overwrite_files(file_path)

            if not self.button_yes_clicked:
                return False

        self.create_folder(folder_name)
        shutil.move(file_path, destination_path)

        file_name = os.path.basename(file_path)
        # print(f"El archivo {file_name} se movió a la carpeta {folder_name}")
        self.log_step(f"File {file_name} was moved to {folder_name} folder")

        return True

    def create_folder(self, name):
        """Create a folder if it doesn't exist"""

        if not os.path.exists(name):
            os.makedirs(name)
            return os.path.abspath(name)
        else:
            return os.path.abspath(name)

    def check_extension(self, ext: str) -> str:
        extensions = {
            "images": ["jpg", "jpeg", "png", "gif", "bmp"],
            "documents": ["txt", "doc", "docx", "pdf", "odt"],
            "spreadsheets": ["xlsx", "csv", "ods"],
            "presentations": ["ppt", "pptx", "odp"],
            "executables": ["exe", "msi", "sh"],
            "archives": ["zip", "rar", "tar", "gz"],
            "audio": ["mp3", "wav", "flac", "aac"],
            "video": ["mp4", "avi", "mkv", "mov"],
            "data": ["json", "xml", "csv", "yaml"],
        }

        for k, v in extensions.items():
            if ext in v:
                return k
        else:
            return "other"


root = Interface(tk.Tk())
app = App(root)
root.mainloop()
