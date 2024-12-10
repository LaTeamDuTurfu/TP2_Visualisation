import tkinter as tk
from tkinter import ttk, font, PhotoImage, Canvas
from tkinter.ttk import Combobox
import TKinterModernThemes as TKMT
import requests
from alphaAPI import StockAPI
import os


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
        self.tree_mes_symboles.bind("<ButtonRelease-1>", self.générer_graphs)

        # Symbol, nom et price
        self.symbol_actuel_label = ttk.Label(self.right_frame, text="", font=self.title_font)
        self.symbol_actuel_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.nom_actuel_label = ttk.Label(self.right_frame, text="", font=self.subtitle_font,
                                          style="subtitle_style.TLabel")
        self.nom_actuel_label.grid(row=0, column=1, sticky=tk.W, pady=10)

        self.vues = ["30 derniers jours", "Dernière année"]
        self.vue_choisie = Combobox(self.right_frame, values=self.vues, state="readonly")
        self.vue_choisie.current(0)
        self.vue_choisie.bind("<<ComboboxSelected>>", self.afficher_graphique)
        self.vue_choisie.grid(row=0, column=2, pady=10, sticky=tk.NE)
        self.current_graph = None
        self.right_frame.grid_columnconfigure(2, weight=1)

        # Separator Bar
        self.separator = ttk.Separator(self.right_frame, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=3, sticky=tk.EW)

        # test image
        self.canvas = Canvas(self.right_frame, width=1000, height=600)
        self.canvas.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)

        # Server Address
        self.addr_srv = "http://127.0.0.1:8200"

        # StockAPI
        self.stock_api = StockAPI()
        self.update_tree_view()

    @staticmethod
    def remove_all_files_in_folder(folder_path):  # Fonction faite par ChatGPT
        # Vérifier si le chemin existe et s'il s'agit d'un dossier
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Parcourir tous les fichiers dans le dossier
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                # Vérifier si c'est un fichier avant de le supprimer
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Supprimé : {file_path}")
                else:
                    print(f"Ignoré (pas un fichier) : {file_path}")
        else:
            print(f"Le chemin spécifié n'existe pas ou n'est pas un dossier : {folder_path}")

    def afficher_graphique(self, event):
        selected_item = self.tree_mes_symboles.focus()
        item_value = self.tree_mes_symboles.item(selected_item, "values")
        vue_choisie = self.vue_choisie.current()

        self.canvas.delete("all")

        if vue_choisie == 0:
            self.current_graph = PhotoImage(file=f"graphics/{item_value[0]}_30_days.png")
        else:
            self.current_graph = PhotoImage(file=f"graphics/{item_value[0]}_past_year.png")

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_graph)

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

        # Clean la right frame
        self.canvas.delete("all")
        self.nom_actuel_label.configure(text="")
        self.symbol_actuel_label.configure(text="")

        response = requests.delete(
            self.addr_srv + "/my_stocks/" + item_value[0]
        )

        if response.status_code == 201:
            self.update_tree_view()
            self.fermer_recherche()
        else:
            print(f"Error DELETE: {response.reason} " + f"{response.status_code}")

    def fermer_recherche(self):
        self.tree_recherche.grid_forget()
        self.close_button.grid_forget()

    def générer_graphs(self, event):
        selected_item = self.tree_mes_symboles.focus()
        item_value = self.tree_mes_symboles.item(selected_item, "values")

        # Clear le dossier des anciens graphiques
        self.remove_all_files_in_folder("graphics")

        response_past_year = requests.get(self.addr_srv + f"/my_stocks/{item_value[0]}/past_year")
        if response_past_year.status_code == 200:
            with open(f"graphics/{item_value[0]}_past_year.png", "wb") as f:
                f.write(response_past_year.content)

        response_30days = requests.get(self.addr_srv + f"/my_stocks/{item_value[0]}/30_days")
        if response_30days.status_code == 200:
            with open(f"graphics/{item_value[0]}_30_days.png", "wb") as f:
                f.write(response_30days.content)

        # Change le texte des labels
        self.nom_actuel_label.configure(text=item_value[1], font=self.subtitle_font)
        self.symbol_actuel_label.configure(text=item_value[0], font=self.subtitle_font)

        # Affiche le graphique
        self.afficher_graphique(None)

    def search_stock(self):
        # Get le symbole à chercher
        keyword = self.search_var.get()
        self.search_entry.delete(0, tk.END)

        # Fait la recherche avec l'API si l'entry n'est pas vide
        json_result = None
        if keyword != "":
            json_result = self.stock_api.recherche_stock(keyword)
        if json_result is None:
            return

        # Extrait les données pertinentes de la requête API
        try:
            self.search_results.clear()
            for result in json_result["bestMatches"]:
                self.search_results.append([result["1. symbol"], result["2. name"]])
            self.tree_recherche.delete(*self.tree_recherche.get_children())
            for result in self.search_results:
                self.tree_recherche.insert('', 'end', values=(result[0], result[1]))
        except KeyError:
            print("ERREUR: Limite de requête avec la clé API, changez d'IP avec un VPN et relancez le programme.")

        # Affiche le tableau de résultats
        self.tree_recherche.grid(column=0, row=2, columnspan=2, rowspan=1, pady=10)
        self.close_button.grid(column=0, row=3, columnspan=2)

    def update_tree_view(self):
        response = requests.get(self.addr_srv + "/my_stocks")

        # Clear les éléments du treeview
        for i in self.tree_mes_symboles.get_children():
            self.tree_mes_symboles.delete(i)

        # Ajoute le nouveau symbole
        if response.status_code == 200:
            stocks = response.json()
            for stock in stocks:
                self.tree_mes_symboles.insert("", tk.END, values=(stock["symbol"], stock["name"]))
        else:
            print(f"Error UPDATE: {response.reason} " + f"{response.status_code}")


if __name__ == '__main__':
    client = ClientTK()
    client.run()
