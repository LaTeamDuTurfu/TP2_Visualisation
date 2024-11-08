import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
from models.stock import Stock
from code_tp.alphaAPI import StockAPI


class ClientTK(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Stock Manager", "park", "dark")

        self.root.geometry("1280x720")

        # PanedWindow
        self.paned_window = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Deux divisions
        self.left_frame = ttk.Frame(self.paned_window)
        self.right_frame = ttk.Frame(self.paned_window)

        self.paned_window.add(self.left_frame, weight=1)
        self.paned_window.add(self.right_frame, weight=1)

        # Champ de recherche
        self.search_var = tk.StringVar()
        self.search_results = []
        self.search_entry = tk.Entry(self.left_frame, textvariable=self.search_var)
        self.search_entry.pack()
        # self.search_entry.bind("<KeyRelease>", lambda event: self.search_stock())

        # Bouton recherche
        self.search_button = tk.Button(self.left_frame, text="Search", command=self.search_stock)
        self.search_button.pack()

        # Treeview
        self.tree = ttk.Treeview(self.left_frame, columns=("Symbol", "Name"), show="headings")
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Name", text="Name")
        self.tree.pack()

        # StockAPI
        self.stock_api = StockAPI()

    def update_tree_view(self):
        # Clear the Treeview
        self.tree.delete(*self.tree.get_children())

        # Populate Treeview with updated search results
        for result in self.search_results:
            self.tree.insert('', 'end', values=(result[0], result[1]))

    def search_stock(self):
        keyword = self.search_var.get()
        json_result = None
        if keyword != "":
            json_result = self.stock_api.recherche_stock(keyword)
        if json_result is None:
            return
        try:
            self.search_results.clear()
            for result in json_result["bestMatches"]:
                self.search_results.append([result["1. symbol"], result["2. name"]])
            self.update_tree_view()
        except KeyError:
            print("Pas de résultats :(")



if __name__ == '__main__':
    client = ClientTK()
    client.run()
