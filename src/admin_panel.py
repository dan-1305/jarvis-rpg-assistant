import tkinter as tk
from tkinter import ttk, messagebox
import logging
import sys
import os

# --- SETUP PATH ĐỂ IMPORT MODULE JARVIS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jarvis_core.database import get_database

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class JarvisAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" JARVIS SYSTEM DASHBOARD (Admin Mode)")
        self.root.geometry("800x600")
        self.db = get_database()

        # Style
        style = ttk.Style()
        style.theme_use('clam')  # Theme nhìn cho đỡ "cổ"

        # --- MAIN TABS ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tab 1: User Profile
        self.tab_profile = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_profile, text=' User Profile')
        self.setup_profile_tab()

        # Tab 2: Vocabulary Manager
        self.tab_vocab = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vocab, text=' Vocabulary DB')
        self.setup_vocab_tab()

    # ==========================================
    # TAB 1: USER PROFILE LOGIC
    # ==========================================
    def setup_profile_tab(self):
        frame = ttk.LabelFrame(self.tab_profile, text="Core Stats (ID: 1)", padding=20)
        frame.pack(padx=20, pady=20, fill="x")

        # Variables
        self.var_level = tk.IntVar()
        self.var_xp = tk.IntVar()
        self.var_hp = tk.IntVar()
        self.var_status = tk.StringVar()

        # UI Layout
        grid_opts = {'padx': 5, 'pady': 10, 'sticky': 'w'}

        ttk.Label(frame, text="Level:").grid(row=0, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_level, width=10).grid(row=0, column=1, **grid_opts)

        ttk.Label(frame, text="XP:").grid(row=0, column=2, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_xp, width=15).grid(row=0, column=3, **grid_opts)

        ttk.Label(frame, text="HP:").grid(row=1, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_hp, width=10).grid(row=1, column=1, **grid_opts)

        ttk.Label(frame, text="Status:").grid(row=1, column=2, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_status, width=30).grid(row=1, column=3, **grid_opts)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=20)

        ttk.Button(btn_frame, text=" Refresh Data", command=self.load_profile).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=" Save Changes (Force Update)", command=self.save_profile).pack(side='left', padx=5)

        # Load data immediately
        self.load_profile()

    def load_profile(self):
        try:
            profile = self.db.get_user_profile()
            self.var_level.set(profile.get('level', 1))
            self.var_xp.set(profile.get('xp', 0))
            self.var_hp.set(profile.get('hp', 100))
            self.var_status.set(profile.get('status', 'active'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profile: {e}")

    def save_profile(self):
        # Admin tool dùng quyền ghi đè trực tiếp (Direct Execute)
        try:
            query = """
                    UPDATE user_profile
                    SET level  = ?, \
                        xp     = ?, \
                        hp     = ?, \
                        status = ?
                    WHERE id = 1 \
                    """
            params = (
                self.var_level.get(),
                self.var_xp.get(),
                self.var_hp.get(),
                self.var_status.get()
            )
            # Truy cập hàm _execute của DatabaseManager (Dù là protected nhưng Admin có quyền)
            self.db._execute(query, params)
            messagebox.showinfo("Success", "Profile Updated Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    # ==========================================
    # TAB 2: VOCABULARY MANAGER LOGIC
    # ==========================================
    def setup_vocab_tab(self):
        # Left Panel: List
        list_frame = ttk.Frame(self.tab_vocab)
        list_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        # Search Bar
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=5)
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_vocab)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side='left', fill='x', expand=True, padx=5)

        # Treeview (Table)
        cols = ('ID', 'Word', 'Level', 'Next Review')
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')

        self.tree.heading('ID', text='ID')
        self.tree.column('ID', width=30)
        self.tree.heading('Word', text='Word')
        self.tree.column('Word', width=120)
        self.tree.heading('Level', text='Lv')
        self.tree.column('Level', width=40)
        self.tree.heading('Next Review', text='Next Review')
        self.tree.column('Next Review', width=100)

        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select_vocab)

        # Right Panel: Edit Form
        form_frame = ttk.LabelFrame(self.tab_vocab, text="Word Editor", padding=10)
        form_frame.pack(side='right', fill='y', padx=10, pady=10)

        self.vocab_id = tk.StringVar()
        self.vocab_word = tk.StringVar()
        self.vocab_meaning = tk.StringVar()
        self.vocab_level = tk.IntVar()

        ttk.Label(form_frame, text="Word:").pack(anchor='w')
        ttk.Entry(form_frame, textvariable=self.vocab_word, width=30).pack(anchor='w', pady=2)

        ttk.Label(form_frame, text="Meaning:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(form_frame, textvariable=self.vocab_meaning, width=30).pack(anchor='w', pady=2)

        ttk.Label(form_frame, text="Learning Level (0-10):").pack(anchor='w', pady=(10, 0))
        ttk.Entry(form_frame, textvariable=self.vocab_level, width=10).pack(anchor='w', pady=2)

        # Buttons
        ttk.Separator(form_frame, orient='horizontal').pack(fill='x', pady=20)

        ttk.Button(form_frame, text=" Add New", command=self.add_vocab).pack(fill='x', pady=5)
        ttk.Button(form_frame, text=" Update Selected", command=self.update_vocab).pack(fill='x', pady=5)
        ttk.Button(form_frame, text=" Delete Selected", command=self.delete_vocab).pack(fill='x', pady=5)
        ttk.Button(form_frame, text=" Clear Form", command=self.clear_form).pack(fill='x', pady=20)

        # Initial Load
        self.load_vocab_list()

    def load_vocab_list(self, query=None):
        # Clear list
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            if query:
                sql = "SELECT * FROM vocab WHERE word LIKE ? OR meaning LIKE ?"
                params = (f'%{query}%', f'%{query}%')
                rows = self.db._fetch_all(sql, params)
            else:
                rows = self.db._fetch_all("SELECT * FROM vocab ORDER BY id DESC")

            for row in rows:
                self.tree.insert('', 'end', values=(row['id'], row['word'], row['learning_level'], row['next_review']))
        except Exception as e:
            print(f"Error loading vocab: {e}")

    def filter_vocab(self, *args):
        self.load_vocab_list(self.search_var.get())

    def on_select_vocab(self, event):
        selected = self.tree.selection()
        if not selected: return
        item = self.tree.item(selected[0])
        pk = item['values'][0]

        # Load full details
        row = self.db._fetch_one("SELECT * FROM vocab WHERE id = ?", (pk,))
        if row:
            self.vocab_id.set(row['id'])
            self.vocab_word.set(row['word'])
            self.vocab_meaning.set(row['meaning'])
            self.vocab_level.set(row['learning_level'])

    def clear_form(self):
        self.vocab_id.set('')
        self.vocab_word.set('')
        self.vocab_meaning.set('')
        self.vocab_level.set(0)
        self.tree.selection_remove(self.tree.selection())

    def add_vocab(self):
        word = self.vocab_word.get().strip()
        meaning = self.vocab_meaning.get().strip()
        if not word: return

        try:
            self.db.add_vocab(word, meaning)
            self.load_vocab_list()
            self.clear_form()
            messagebox.showinfo("Success", "Word added!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_vocab(self):
        pk = self.vocab_id.get()
        if not pk: return

        try:
            query = "UPDATE vocab SET word=?, meaning=?, learning_level=? WHERE id=?"
            self.db._execute(query, (self.vocab_word.get(), self.vocab_meaning.get(), self.vocab_level.get(), pk))
            self.load_vocab_list()
            messagebox.showinfo("Success", "Word updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_vocab(self):
        pk = self.vocab_id.get()
        word = self.vocab_word.get()
        if not pk: return

        if messagebox.askyesno("Confirm", f"Delete word '{word}'?"):
            try:
                self.db._execute("DELETE FROM vocab WHERE id=?", (pk,))
                self.load_vocab_list()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisAdminApp(root)
    root.mainloop()