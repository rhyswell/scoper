import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

from scoper_engine import ScoperEngine


class ScoperGUI:
    def __init__(self):
        self.engine = ScoperEngine()

        self.root = tk.Tk()
        self.root.title("Scoper - Scientific Argument Explorer")
        self.root.geometry("1000x700")

        self._build_layout()

    def _build_layout(self):
        # Claim input
        self.claim_label = tk.Label(self.root, text="Enter Scientific Claim:")
        self.claim_label.pack(pady=5)

        self.claim_entry = tk.Entry(self.root, width=120)
        self.claim_entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.analyze_button = tk.Button(
            button_frame, text="Analyze", command=self._analyze_thread
        )
        self.analyze_button.pack(side=tk.LEFT, padx=10)

        self.reindex_button = tk.Button(
            button_frame, text="Re-index Literature", command=self._reindex_thread
        )
        self.reindex_button.pack(side=tk.LEFT, padx=10)

        # Output frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Supporting arguments
        support_label = tk.Label(output_frame, text="Supporting Arguments")
        support_label.grid(row=0, column=0, pady=5)

        self.support_text = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD
        )
        self.support_text.grid(row=1, column=0, sticky="nsew", padx=5)

        # Opposing arguments
        oppose_label = tk.Label(output_frame, text="Opposing Arguments")
        oppose_label.grid(row=0, column=1, pady=5)

        self.oppose_text = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD
        )
        self.oppose_text.grid(row=1, column=1, sticky="nsew", padx=5)

        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_columnconfigure(1, weight=1)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready.")

        self.status_bar = tk.Label(
            self.root, textvariable=self.status_var, anchor="w"
        )
        self.status_bar.pack(fill=tk.X)

    def _set_status(self, message: str):
        self.status_var.set(message)
        self.root.update_idletasks()

    def _analyze_thread(self):
        thread = threading.Thread(target=self._analyze)
        thread.start()

    def _reindex_thread(self):
        thread = threading.Thread(target=self._reindex)
        thread.start()

    def _analyze(self):
        claim = self.claim_entry.get()

        self._set_status("Analyzing claim...")
        self.support_text.delete(1.0, tk.END)
        self.oppose_text.delete(1.0, tk.END)

        try:
            results = self.engine.analyze_claim(claim)

            self.support_text.insert(tk.END, results["support"])
            self.oppose_text.insert(tk.END, results["oppose"])

            self._set_status("Analysis complete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self._set_status("Error occurred.")

    def _reindex(self):
        self._set_status("Re-indexing literature...")

        try:
            self.engine.reindex_literature()
            self._set_status("Re-index complete.")
            messagebox.showinfo("Success", "Literature successfully re-indexed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self._set_status("Error during re-indexing.")

    def run(self):
        self.root.mainloop()
