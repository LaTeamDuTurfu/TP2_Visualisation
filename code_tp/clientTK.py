import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
from models.stock import Stock
from code_tp.alphaAPI import *


class ClientTK(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Gestion de Livres", "park", "dark")

        # Champ de recherche
        self.search_var = tk.StringVar()
        self.search_results = []
        self.search_entry = tk.Entry(textvariable=self.search_var)
        self.search_entry.pack()
        # self.search_entry.bind("<KeyRelease>", lambda event: self.search_stock())

        # Bouton recherche
        self.search_button = tk.Button(text="Search", command=self.search_stock)
        self.search_button.pack()

        # Treeview
        self.tree = ttk.Treeview(columns=("Symbol", "Name"), show="headings")
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Name", text="Name")
        self.tree.pack()

    def update_tree_view(self):
        # Clear the Treeview
        self.tree.delete(*self.tree.get_children())

        # Populate Treeview with updated search results
        for result in self.search_results:
            self.tree.insert('', 'end', values=(result[0], result[1]))

    def search_stock(self):
        keyword = self.search_var.get()
        json_result = recherche_stock(keyword)
        if json_result is None:
            return
        try:
            for result in json_result["bestMatches"]:
                self.search_results.append([result["1. symbol"], result["2. name"]])
            self.update_tree_view()
        except KeyError:
            print("Limite quotidienne de requêtes atteinte :(")


if __name__ == '__main__':
    client = ClientTK()
    client.run()
