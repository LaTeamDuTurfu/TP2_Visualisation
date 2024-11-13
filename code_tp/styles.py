from tkinter import ttk

style_rouge = ttk.Style()
style_rouge.configure("Custom.Rouge",
                      foreground="black",  # Text color
                      background="red")    # Background color

style_rouge.map("Custom.Rouge",
          background=[('active', '#2980b9'), ('pressed', '#1f618d')])
