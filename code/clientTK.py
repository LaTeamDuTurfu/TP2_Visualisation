import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
import requests


class ClientTK(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Gestion de Livres", "park", "dark")
    

if __name__ == '__main__':
    client = ClientTK()
    client.run()