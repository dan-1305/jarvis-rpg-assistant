import datetime
import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# --- CẤU HÌNH ĐƯỜNG DẪN DB ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "jarvis.db")


class JarvisAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 JARVIS CORTEX MANAGER (Admin Dashboard)")
        self.root.geometry("900x600")

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=25, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))

        # --- KHUNG NHẬP LIỆU (TOP) ---
        input_frame = ttk.LabelFrame(root, text="Chi tiết Từ vựng", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Word (Từ vựng):").grid(row=0, column=0, padx=5, sticky="w")
        self.entry_word = ttk.Entry(input_frame, width=30)
        self.entry_word.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Meaning (Nghĩa/Context):").grid(row=0, column=2, padx=5, sticky="w")
        self.entry_meaning = ttk.Entry(input_frame, width=50)
        self.entry_meaning.grid(row=0, column=3, padx=5, pady=5)

        # Level & Date (Chỉ hiển thị, không sửa trực tiếp ở đây cho an toàn)
        self.lbl_status = ttk.Label(input_frame, text="Status: Ready", foreground="blue")
        self.lbl_status.grid(row=1, column=0, columnspan=4, pady=5)

        # --- KHUNG NÚT BẤM (MIDDLE) ---
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill="x", padx=10)

        ttk.Button(btn_frame, text="➕ Thêm Mới", command=self.add_word).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✏️ Cập Nhật (Sửa)", command=self.update_word).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Xóa Bỏ", command=self.delete_word).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Làm Mới (Refresh)", command=self.load_data).pack(side="left", padx=5)

        # Nút Hack Time thần thánh
        ttk.Button(btn_frame, text="⚡ HACK TIME (Ôn All)", command=self.hack_time).pack(side="right", padx=5)

        # --- BẢNG DỮ LIỆU (BOTTOM) ---
        tree_frame = ttk.Frame(root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "word", "meaning", "level", "next_review", "created")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Định nghĩa cột
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")

        self.tree.heading("word", text="Word")
        self.tree.column("word", width=150, anchor="w")

        self.tree.heading("meaning", text="Meaning & Context")
        self.tree.column("meaning", width=400, anchor="w")

        self.tree.heading("level", text="Lv")
        self.tree.column("level", width=50, anchor="center")

        self.tree.heading("next_review", text="Next Review")
        self.tree.column("next_review", width=100, anchor="center")

        self.tree.heading("created", text="Created At")
        self.tree.column("created", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Sự kiện click vào dòng
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Load dữ liệu ban đầu
        self.load_data()

    # --- DATABASE FUNCTIONS (ĐÃ FIX LỖI) ---
    def run_query(self, query, params=()):
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            # --- FIX QUAN TRỌNG: Lấy dữ liệu NGAY LẬP TỨC trước khi đóng ---
            # fetchall() sẽ trả về một list các tuples, hoặc list rỗng []
            data = cursor.fetchall()
            return data

        except Exception as e:
            messagebox.showerror("Lỗi Database", str(e))
            return None  # Trả về None nếu lỗi
        finally:
            if conn: conn.close()  # Đóng kết nối an toàn

    def load_data(self):
        # Xóa dữ liệu cũ trên bảng
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Lấy dữ liệu mới
        rows = self.run_query("SELECT * FROM vocab ORDER BY id DESC")

        # Kiểm tra xem có dữ liệu không (rows phải khác None)
        if rows is not None:
            for row in rows:
                self.tree.insert("", "end", values=row)

        self.lbl_status.config(text=f"Đã tải dữ liệu lúc {datetime.datetime.now().strftime('%H:%M:%S')}")

    def on_select(self, event):
        # Khi click vào 1 dòng, điền dữ liệu lên ô nhập
        selected_item = self.tree.selection()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.entry_word.delete(0, tk.END)
            # Kiểm tra xem row có đủ phần tử không để tránh lỗi index
            if len(row) > 1: self.entry_word.insert(0, row[1])
            self.entry_meaning.delete(0, tk.END)
            if len(row) > 2: self.entry_meaning.insert(0, row[2])

    def add_word(self):
        word = self.entry_word.get().strip()
        meaning = self.entry_meaning.get().strip()

        if not word or not meaning:
            messagebox.showwarning("Thiếu tin", "Nhập đủ từ và nghĩa đi bro!")
            return

        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        today = datetime.date.today().isoformat()

        result = self.run_query(
            "INSERT INTO vocab (word, meaning, learning_level, next_review, created_at) VALUES (?, ?, 0, ?, ?)",
            (word, meaning, tomorrow, today)
        )

        if result is not None:
            self.load_data()
            self.entry_word.delete(0, tk.END)
            self.entry_meaning.delete(0, tk.END)
            messagebox.showinfo("Success", f"Đã nạp '{word}' vào não!")

    def update_word(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Chọn dòng", "Chọn từ cần sửa trong bảng trước!")
            return

        row_id = self.tree.item(selected_item)['values'][0]
        word = self.entry_word.get().strip()
        meaning = self.entry_meaning.get().strip()

        result = self.run_query(
            "UPDATE vocab SET word = ?, meaning = ? WHERE id = ?",
            (word, meaning, row_id)
        )
        if result is not None:
            self.load_data()
            messagebox.showinfo("Success", "Đã cập nhật thông tin!")

    def delete_word(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Chọn dòng", "Chọn từ cần xóa!")
            return

        word_to_delete = self.tree.item(selected_item)['values'][1]
        confirm = messagebox.askyesno("Xác nhận", f"Có chắc muốn xóa vĩnh viễn '{word_to_delete}'?")

        if confirm:
            row_id = self.tree.item(selected_item)['values'][0]
            result = self.run_query("DELETE FROM vocab WHERE id = ?", (row_id,))
            if result is not None:
                self.load_data()
                self.entry_word.delete(0, tk.END)
                self.entry_meaning.delete(0, tk.END)

    def hack_time(self):
        confirm = messagebox.askyesno("HACK TIME", "Bạn có muốn ép TOÀN BỘ từ vựng phải ôn tập NGAY HÔM NAY không?")
        if confirm:
            today = datetime.date.today().isoformat()
            result = self.run_query("UPDATE vocab SET next_review = ?", (today,))
            if result is not None:
                self.load_data()
                messagebox.showinfo("Hacker Mode", "🕵️ Đã bẻ cong thời gian thành công!\nChạy bot ngay để ôn bài.")


if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisAdminApp(root)
    root.mainloop()
