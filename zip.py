import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os


class FSProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FS to ZIP Creator")
        self.root.geometry("400x200")
        self.root.configure(bg="black")
        
        # Dados carregados do arquivo .fs
        self.files_to_process = []
        
        # Botão para carregar arquivo .fs
        self.load_button = tk.Button(
            root, text="Load .fs File", command=self.load_fs_file, bg="white", fg="black"
        )
        self.load_button.pack(pady=10)
        
        # Botão para criar arquivo .zip
        self.save_button = tk.Button(
            root, text="Save as .zip", command=self.save_zip_file, bg="white", fg="black"
        )
        self.save_button.pack(pady=10)
        
        # Rótulo de status
        self.status_label = tk.Label(
            root, text="", bg="black", fg="white", wraplength=350
        )
        self.status_label.pack(pady=10)

    def load_fs_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("FS Files", "*.fs"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Processar o conteúdo do arquivo .fs
            self.files_to_process = []
            for item in content.split("|"):
                parts = item.split("#")
                if len(parts) != 2:
                    continue
                file_name, file_text = parts
                self.files_to_process.append((file_name.strip(), file_text.strip()))

            self.status_label.config(text=f"Loaded {len(self.files_to_process)} entries.")
            messagebox.showinfo("Success", f"Loaded {len(self.files_to_process)} entries from the .fs file.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load .fs file: {e}")
            self.status_label.config(text="Failed to load .fs file.")

    def save_zip_file(self):
        if not self.files_to_process:
            messagebox.showerror("Error", "No data loaded. Please load a .fs file first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".zip", filetypes=[("ZIP Files", "*.zip"), ("All Files", "*.*")]
        )
        if not save_path:
            return

        try:
            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_name, file_content in self.files_to_process:
                    temp_path = os.path.basename(file_name.strip())
                    zipf.writestr(temp_path, file_content)

            messagebox.showinfo("Success", f"ZIP file saved at {save_path}")
            self.status_label.config(text="ZIP file created successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create ZIP file: {e}")
            self.status_label.config(text="Failed to create ZIP file.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FSProcessorApp(root)
    root.mainloop()

