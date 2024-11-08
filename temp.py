import tkinter as tk
from tkinter import ttk


def on_item_double_click(event):
    # Récupérer l'élément sélectionné
    selected_item = tree.focus()
    item_value = tree.item(selected_item, "values")

    if item_value:
        print(f"Vous avez double-cliqué sur : {item_value}")


# Créer la fenêtre principale
root = tk.Tk()
root.title("Exemple de Treeview avec double-clic")

# Créer un Treeview avec des colonnes
tree = ttk.Treeview(root, columns=("Nom", "Âge"), show="headings")
tree.heading("Nom", text="Nom")
tree.heading("Âge", text="Âge")
tree.pack(padx=20, pady=20)

# Ajouter des données au Treeview
data = [
    ("Alice", 25),
    ("Bob", 30),
    ("Charlie", 22)
]

for item in data:
    tree.insert("", "end", values=item)

# Associer l'événement de double-clic au Treeview
tree.bind("<Double-1>", on_item_double_click)

# Lancer la boucle principale
root.mainloop()