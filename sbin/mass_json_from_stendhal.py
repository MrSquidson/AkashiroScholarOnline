import sys
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

SERVERS = ["Abexilas", "Rathnir", "Eldham", "Kanahulu"]

def select_server():
    def on_select(event=None):
        selected_server = server_var.get()
        if selected_server:
            root.quit()
            root.destroy()
        else:
            messagebox.showerror("Error", "Server name cannot be empty.")
    
    root = tk.Tk()
    root.title("Select Server")

    tk.Label(root, text="Please select the server:").pack(pady=10)

    server_var = tk.StringVar(root)
    server_var.set(SERVERS[0])  # Default value

    server_menu = tk.OptionMenu(root, server_var, *SERVERS)
    server_menu.pack(pady=10)

    tk.Button(root, text="OK", command=on_select).pack(pady=10)

    root.mainloop()

    return server_var.get()

def print_json_book_from_stendhal(fpath, item_origin):
    title = None
    author = None
    with open(fpath,encoding='utf-8', mode="r") as file:
        while True:
            line = file.readline().strip()
            if line == "pages:":
                break
            elif line.startswith("title: "):
                title = line[len("title: "):]
            elif line.startswith("author: "):
                author = line[len("author: "):]
        rem = "\n" + file.read()
        pages = rem.split("\n#- ")

    book = {
        'item_origin': item_origin,
        'item_title': title,
        'signee': author,
        'pages': [json.dumps({"text": page}) for page in pages if page.strip()],
    }
    return book

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select a directory")
    return directory

def main():
    directory = select_directory()
    if not directory:
        print("No directory selected. Exiting.")
        sys.exit(1)

    item_origin = select_server()  # You can change this to the appropriate value
    books = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            book_json = print_json_book_from_stendhal(filepath, item_origin)
            books.append(book_json)

    # Create the export directory if it doesn't exist
    export_directory = os.path.join(os.getcwd(), 'stendhalJsonExports')
    os.makedirs(export_directory, exist_ok=True)

    # Save the output file in the export directory
    output_filepath = os.path.join(export_directory, "books.json")
    with open(output_filepath,encoding='utf-8',mode= "w") as outfile:
        for book in books:
            json.dump(book, outfile, separators=(',', ':'))
            outfile.write('\n')
    output_filepath = os.path.join(export_directory,".gitignore")
    with open(output_filepath,encoding='utf-8',mode= "w") as outfile:
        outfile.write('*')

    print(f"Processed files have been saved to {output_filepath}")

if __name__ == "__main__":
    main()
