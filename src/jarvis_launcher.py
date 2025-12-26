import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import sys
import os

# --- PATH CONFIGURATION ---
# Xác định thư mục gốc Jarvis từ vị trí file src/jarvis_launcher.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VENV_PYTHON = os.path.join(BASE_DIR, '.venv', 'Scripts', 'python.exe')
MAIN_SCRIPT = os.path.join(BASE_DIR, 'main.py')

class JarvisLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("🚀 JARVIS MISSION CONTROL")
        self.root.geometry("650x650") # Tăng nhẹ chiều cao để thêm Search Bar
        self.root.configure(bg="#1e1e1e")

        self.setup_ui()

    def setup_ui(self) -> None:
        """Thiết lập giao diện tích hợp với main.py."""
        style = ttk.Style()
        style.theme_use('clam')

        # Header
        header = tk.Label(self.root, text="SYSTEM COMMAND CENTER", fg="#00ff00", bg="#1e1e1e",
                          font=("Courier", 16, "bold"))
        header.pack(pady=15)

        # --- SEARCH SECTION (NEW) ---
        search_frame = tk.Frame(self.root, bg="#1e1e1e")
        search_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(search_frame, text="🔍 Search Notes:", fg="#888888", bg="#1e1e1e").pack(side="left")
        self.search_entry = tk.Entry(search_frame, bg="#333333", fg="white", insertbackground="white")
        self.search_entry.pack(side="left", padx=10, fill="x", expand=True)
        # Nhấn Enter để tìm kiếm luôn
        self.search_entry.bind("<Return>", lambda e: self.launch_main_cmd(f"search {self.search_entry.get()}"))
        
        btn_search = tk.Button(search_frame, text="Ask Jarvis", bg="#444444", fg="white",
                               command=lambda: self.launch_main_cmd(f"search {self.search_entry.get()}"))
        btn_search.pack(side="left")

        # --- BUTTON FRAME ---
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        # Định nghĩa các nút lệnh truyền vào main.py
        # Format: (Tên hiển thị, Tham số lệnh cho main.py)
        modules = [
            ("⚡ CORE SYSTEM", ""),           # Chạy main.py mặc định (help/vòng lặp)
            ("☀️ DAILY BRIEF", "daily"),      # python main.py daily
            ("🧬 EVOLUTION", "evolve"),       # python main.py evolve
            ("🕵️ AUTO LEARN", "hunt"),        # python main.py hunt
            ("📖 TEACHER (NEW)", "teach new"),
            ("🎓 TEACHER (REVIEW)", "teach review")
        ]

        for text, cmd_arg in modules:
            # Màu sắc nổi bật cho Core System
            is_core = "CORE" in text
            bg_color = "#d4af37" if is_core else "#333333"
            fg_color = "black" if is_core else "white"
            
            btn = tk.Button(btn_frame, text=text, width=25, height=1,
                            bg=bg_color, fg=fg_color, font=("Arial", 10, "bold"),
                            command=lambda c=cmd_arg: self.launch_main_cmd(c))
            btn.pack(pady=4)

        # Log Window
        tk.Label(self.root, text="SYSTEM LOG:", fg="#888888", bg="#1e1e1e").pack(anchor="w", padx=20)
        self.log_text = tk.Text(self.root, height=12, bg="#000000", fg="#00ff00", font=("Consolas", 9))
        self.log_text.pack(padx=20, pady=5, fill="both", expand=True)

    def log(self, message: str) -> None:
        """Ghi thông tin vào cửa sổ Log."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def launch_main_cmd(self, cmd_args: str) -> None:
        """Chạy main.py thông qua subprocess với tham số."""
        # Chuẩn bị danh sách lệnh
        full_cmd = [VENV_PYTHON, MAIN_SCRIPT]
        if cmd_args.strip():
            # Tách các tham số (ví dụ 'teach new' thành ['teach', 'new'])
            full_cmd.extend(cmd_args.split())

        # Chạy trong thread riêng để không treo giao diện
        thread = threading.Thread(target=self.run_process, args=(full_cmd,))
        thread.start()

    def run_process(self, cmd_list: list) -> None:
        """Thực thi tiến trình và bắt log realtime."""
        display_name = " ".join(cmd_list[1:]) # Bỏ qua đường dẫn python
        self.log(f"--- Executing: {display_name} ---")

        try:
            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )

            if process.stdout:
                for line in process.stdout:
                    self.log(line.strip())

            process.wait()
            self.log(f"✅ Process finished with code {process.returncode}\n")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("System Error", f"Could not execute command: {display_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisLauncher(root)
    root.mainloop()