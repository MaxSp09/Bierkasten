import tkinter as tk
from tkinter import ttk, messagebox

class WährungsumrechnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Währungsumrechner - Feature Edition")
        self.root.geometry("600x450") 
        self.root.configure(bg="#f0f0f0")
        
        # Wechselkurse (relativ zu Euro)
        # HINZUGEFÜGT: SCHWEIZER FRANKEN für den Pull Request
        self.wechselkurse = {
            "EURO": 1.0,
            "YEN": 182.0,
            "SCHWEDISCHE KRONEN": 10.63,
            "SCHILLING": 13.76,
            "SCHWEIZER FRANKEN": 0.95 
        }
        
        # Haupttitel
        titel = tk.Label(root, text="Währungsumrechner", font=("Arial", 18, "bold"), bg="#f0f0f0")
        titel.pack(pady=15)

        # --- Such-Bereich ---
        such_frame = tk.Frame(root, bg="#f0f0f0")
        such_frame.pack(pady=5, padx=20, fill="x")
        tk.Label(such_frame, text="Währung suchen:", font=("Arial", 10), bg="#f0f0f0").pack(side="left", padx=5)
        self.suche_var = tk.StringVar()
        self.suche_var.trace_add("write", self.filter_waehrungen)
        self.suche_input = tk.Entry(such_frame, textvariable=self.suche_var, width=20, font=("Arial", 10))
        self.suche_input.pack(side="left", padx=5)
        
        # Eingabe-Frame
        eingabe_frame = tk.Frame(root, bg="#f0f0f0")
        eingabe_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(eingabe_frame, text="Betrag:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
        self.betrag_input = tk.Entry(eingabe_frame, width=15, font=("Arial", 12))
        self.betrag_input.pack(side="left", padx=5)
        self.betrag_input.bind("<Return>", lambda e: self.umrechnen())
        
        # Umrechnung-Frame
        umrechnung_frame = tk.Frame(root, bg="#f0f0f0")
        umrechnung_frame.pack(pady=15, padx=20, fill="x")
        
        tk.Label(umrechnung_frame, text="Von:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
        self.von_currency = ttk.Combobox(umrechnung_frame, values=list(self.wechselkurse.keys()), 
                                         state="readonly", width=15, font=("Arial", 12))
        self.von_currency.set("EURO")
        self.von_currency.pack(side="left", padx=5)
        
        tk.Label(umrechnung_frame, text="→", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(side="left", padx=10)
        
        tk.Label(umrechnung_frame, text="Zu:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
        self.zu_currency = ttk.Combobox(umrechnung_frame, values=list(self.wechselkurse.keys()), 
                                        state="readonly", width=15, font=("Arial", 12))
        self.zu_currency.set("YEN")
        self.zu_currency.pack(side="left", padx=5)
        
        # Button Frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=15)
        
        umrechnen_btn = tk.Button(button_frame, text="Umrechnen", command=self.umrechnen, 
                                  font=("Arial", 12), bg="#4CAF50", fg="white", padx=20)
        umrechnen_btn.pack(side="left", padx=5)
        
        löschen_btn = tk.Button(button_frame, text="Löschen", command=self.löschen,
                               font=("Arial", 12), bg="#f44336", fg="white", padx=20)
        löschen_btn.pack(side="left", padx=5)
        
        # Ergebnis-Frame
        ergebnis_frame = tk.LabelFrame(root, text="Ergebnis", font=("Arial", 12, "bold"), 
                                      bg="#f0f0f0", padx=15, pady=15)
        ergebnis_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        self.ergebnis_label = tk.Label(ergebnis_frame, text="Geben Sie einen Betrag ein",
                                       font=("Arial", 14), bg="white", fg="#333333", 
                                       justify="center", wraplength=400, relief="sunken", padx=10, pady=20)
        self.ergebnis_label.pack(fill="both", expand=True)

    def filter_waehrungen(self, *args):
        """Filtert die Combobox-Einträge basierend auf der Sucheingabe."""
        suchbegriff = self.suche_var.get().upper()
        alle_waehrungen = list(self.wechselkurse.keys())
        gefiltert = [w for w in alle_waehrungen if suchbegriff in w]
        
        self.von_currency['values'] = gefiltert
        self.zu_currency['values'] = gefiltert
        
        if len(gefiltert) == 1:
            self.von_currency.set(gefiltert[0])
            self.zu_currency.set(gefiltert[0])

    def umrechnen(self):
        try:
            betrag_text = self.betrag_input.get().replace(",", ".").strip()
            if not betrag_text:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen Betrag ein!")
                return
            
            betrag = float(betrag_text)
            if betrag < 0:
                messagebox.showwarning("Warnung", "Der Betrag muss positiv sein!")
                return
            
            von = self.von_currency.get()
            zu = self.zu_currency.get()
            
            if von not in self.wechselkurse or zu not in self.wechselkurse:
                messagebox.showerror("Fehler", "Bitte wählen Sie gültige Währungen aus!")
                return
            
            betrag_in_eur = betrag / self.wechselkurse[von]
            ergebnis = betrag_in_eur * self.wechselkurse[zu]
            
            ergebnis_text = f"{betrag:.2f} {von}\n=\n{ergebnis:.2f} {zu}"
            self.ergebnis_label.config(text=ergebnis_text, fg="#27ae60")
            
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl ein!")

    def löschen(self):
        self.betrag_input.delete(0, tk.END)
        self.suche_var.set("") 
        self.filter_waehrungen() 
        self.ergebnis_label.config(text="Geben Sie einen Betrag ein", fg="#333333")
        self.betrag_input.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = WährungsumrechnerApp(root)
    root.mainloop()
