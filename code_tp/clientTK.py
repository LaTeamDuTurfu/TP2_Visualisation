import tkinter as tk
from tkinter import ttk, font
import TKinterModernThemes as TKMT
import requests

from code_tp.alphaAPI import StockAPI


class ClientTK(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Stocks Manager", "park", "dark")

        self.root.geometry("1280x720")

        # Styles TTK
        self.close_style = ttk.Style().configure("close_style.TButton", foreground="red", background="black")
        self.subtitle_style = ttk.Style().configure("subtitle_style.TLabel", foreground="grey")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=20)

        # PanedWindow
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="grey", bd=3)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Deux divisions
        self.left_frame = ttk.Frame(self.paned_window)
        self.right_frame = ttk.Frame(self.paned_window)

        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.right_frame)

        # Label Recherche
        self.recherche_label = ttk.Label(self.left_frame, text="Recherche", font=self.title_font)
        self.recherche_label.grid(row=0, column=0, columnspan=2)

        # Champ de recherche
        self.search_var = tk.StringVar()
        self.search_results = []
        self.search_entry = tk.Entry(self.left_frame, textvariable=self.search_var)
        self.search_entry.grid(column=0, row=1, columnspan=1, sticky=tk.EW, padx=10)

        # Bouton recherche
        self.search_button = ttk.Button(self.left_frame, text="Search", command=self.search_stock)
        self.root.bind("<Return>", lambda event: self.search_stock())
        self.search_button.grid(column=1, row=1, columnspan=1, sticky=tk.EW, padx=20)

        # Treeview Recherche
        self.tree_recherche = ttk.Treeview(self.left_frame, columns=("Symbol", "Name"), show="headings")
        self.tree_recherche.heading("Symbol", text="Symbol")
        self.tree_recherche.heading("Name", text="Name")
        self.tree_recherche.bind("<Double-1>", self.ajouter_stock)

        # Close recherche button
        self.close_button = ttk.Button(self.left_frame, text="Fermer Recherche", command=self.fermer_recherche,
                                       style="close_style.TButton")

        # Separator Bar
        self.separator = ttk.Separator(self.left_frame, orient=tk.HORIZONTAL)
        self.separator.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=20)

        # Label Mes symboles
        self.mes_symboles_label = ttk.Label(self.left_frame, text="Mes Symboles", font=self.title_font)
        self.mes_symboles_label.grid(row=5, column=0, columnspan=2)

        # Treeview Mes Symboles
        self.tree_mes_symboles = ttk.Treeview(self.left_frame, columns=("Symbol", "Name"), show="headings")
        self.tree_mes_symboles.heading("Symbol", text="Symbol")
        self.tree_mes_symboles.heading("Name", text="Name")
        self.tree_mes_symboles.grid(column=0, row=6, columnspan=2, pady=10)
        self.tree_mes_symboles.bind("<BackSpace>", self.delete_stock)

        # Symbol, nom et price
        self.symbol_actuel_label = ttk.Label(self.right_frame, text="<Symbol>", font=self.title_font)
        self.symbol_actuel_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.nom_actuel_label = ttk.Label(self.right_frame, text="<Nom>", font=self.subtitle_font, style="subtitle_style.TLabel")
        self.nom_actuel_label.grid(row=0, column=1, sticky=tk.W, pady=10)

        self.price_actuel_label = ttk.Label(self.right_frame, text="<Price>", font=self.subtitle_font, style="subtitle_style.TLabel")
        self.price_actuel_label.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
        self.right_frame.grid_columnconfigure(2, weight=1)

        # Separator Bar
        self.separator = ttk.Separator(self.right_frame, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=3, sticky=tk.EW)

        # StockAPI
        self.stock_api = StockAPI()
        self.update_tree_view()

        # Server Address
        self.addr_srv = "http://127.0.0.1:8100"

    def update_tree_view(self):
        response = requests.get(self.addr_srv + "/my_stocks")

        for i in self.tree_mes_symboles.get_children():
            self.tree_mes_symboles.delete(i)

        if response.status_code == 200:
            stocks = response.json()
            for stock in stocks:
                self.tree_mes_symboles.insert("", tk.END, values=(stock["symbol"], stock["name"]))
        else:
            print(f"Error UPDATE: {response.reason} " + f"{response.status_code}")

    def search_stock(self):
        keyword = self.search_var.get()
        self.search_entry.delete(0, tk.END)
        json_result = None
        if keyword != "":
            json_result = self.stock_api.recherche_stock(keyword)
        if json_result is None:
            return
        try:
            self.search_results.clear()
            for result in json_result["bestMatches"]:
                self.search_results.append([result["1. symbol"], result["2. name"]])
            self.tree_recherche.delete(*self.tree_recherche.get_children())
            for result in self.search_results:
                self.tree_recherche.insert('', 'end', values=(result[0], result[1]))
        except KeyError:
            print("Pas de résultats :(")
        self.tree_recherche.grid(column=0, row=2, columnspan=2, rowspan=1, pady=10)
        self.close_button.grid(column=0, row=3, columnspan=2)

    def fermer_recherche(self):
        self.tree_recherche.grid_forget()
        self.close_button.grid_forget()

    def ajouter_stock(self, event):
        # Récupérer l'élément sélectionné
        selected_item = self.tree_recherche.focus()
        item_value = self.tree_recherche.item(selected_item, "values")

        response = requests.post(
            self.addr_srv + "/my_stocks",
            json={
                "name": item_value[1],
                "symbol": item_value[0],
            }
        )

        if response.status_code == 201:
            self.update_tree_view()
            self.fermer_recherche()
        else:
            print(f"Error ADD: {response.reason} " + f"{response.status_code}")

    def delete_stock(self, event):
        # Récupérer l'élément sélectionné
        selected_item = self.tree_mes_symboles.focus()
        item_value = self.tree_mes_symboles.item(selected_item, "values")

        response = requests.delete(
            self.addr_srv + "/my_stocks/" + item_value[0]
        )

        if response.status_code == 201:
            self.update_tree_view()
            self.fermer_recherche()
        else:
            print(f"Error DELETE: {response.reason} " + f"{response.status_code}")

    def afficher_stock(self):

        selected_item = self.tree_mes_symboles.focus()
        item_value = self.tree_mes_symboles.item(selected_item, "values")

        données_30_jours = StockAPI.get_data_30_days(item_value[0])
        données_monthly = StockAPI.get_data_monthly(item_value[0])



        pass


if __name__ == '__main__':
    client = ClientTK()
    client.run()
