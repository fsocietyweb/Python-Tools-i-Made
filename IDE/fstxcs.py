import os
import sys
import subprocess
import threading
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

# System-Wide Version Control & Brand Identifiers
APP_VERSION = "v2.2.0 (Stable Beta)"
APP_TITLE = f"FSTX Code Studio {APP_VERSION}"
FONT_FAMILY = "Consolas" if os.name == "nt" else "Monospace"
CODE_NAME = "BEYOND10"

DEFAULT_FONT_SIZE = 12
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 28

# Extended 15-Format Production Matrix Table
SUPPORTED_FORMATS = [
    ("FSTX Studio Format", "*.fstx"),
    ("Python Architecture", "*.py"),
    ("JavaScript Blueprint", "*.js"),
    ("TypeScript Component", "*.ts"),
    ("HTML5 Document", "*.html"),
    ("Cascading Style Sheet", "*.css"),
    ("JSON Configuration", "*.json"),
    ("Markdown Technical Spec", "*.md"),
    ("C++ Engine Source", "*.cpp;*.hpp;*.h"),
    ("C# Core Assembly", "*.cs"),
    ("Java Enterprise Source", "*.java"),
    ("Rust Systems Code", "*.rs"),
    ("Go Microservices Code", "*.go"),
    ("Unix Shell Script", "*.sh"),
    ("Windows Batch File", "*.bat"),
    ("All Legacy Assets", "*.*")
]

# Comprehensive 10-Language Localization Dictionary Matrix
LOCALIZATION = {
    "English": {
        "new": "New File", "open": "Open File", "save": "Save", "save_as": "Save As", "close_tab": "Close Tab",
        "run": "Run Code", "settings": "Settings", "theme": "UI Theme", "lang": "Language", "about": "About FSTX",
        "adv_on": "Telemetry: ON", "adv_off": "Telemetry: OFF", "status_ready": "Status: Ready", "status_idle": "Status: Idle",
        "console_title": "Execution Console Output (ECO)", "clear_console": "Clear", "empty_state": "No open buffers.\nCreate or import a file to initialize workspace.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nNext-gen lightweight structural development environment.\n\nCreated in 2026.",
        "adv_metrics": "File Metrics", "sys_telemetry": "System Telemetry", "lines": "Lines", "chars": "Characters", "size": "Disk Size", "path": "File Path",
        "opt_font": "Editor Font Size", "close_set": "✕ Close Panels", "toggle_console": "👁 Toggle Console", "explorer": "Workspace Explorer",
        "rename": "Refactor"
    },
    "German": {
        "new": "Neue Datei", "open": "Datei Öffnen", "save": "Speichern", "save_as": "Speichern unter", "close_tab": "Schließen",
        "run": "Ausführen", "settings": "Optionen", "theme": "Design-Modus", "lang": "Sprache", "about": "Über FSTX",
        "adv_on": "Telemetrie: AN", "adv_off": "Telemetrie: AUS", "status_ready": "Status: Bereit", "status_idle": "Status: Leerlauf",
        "console_title": "Ausgabe-Konsole (ECO)", "clear_console": "Leeren", "empty_state": "Keine Dokumente geöffnet.\nErstellen Sie eine Datei, um zu beginnen.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nLeichte Entwicklungsumgebung für strukturierte Programmierung.\n\nErstellt im Jahr 2026.",
        "adv_metrics": "Datei-Metriken", "sys_telemetry": "System-Telemetrie", "lines": "Zeilen", "chars": "Zeichen", "size": "Größe", "path": "Dateipfad",
        "opt_font": "Schriftgröße", "close_set": "✕ Schließen", "toggle_console": "👁 Konsole Umschalten", "explorer": "Arbeitsbereich",
        "rename": "Refaktorieren"
    },
    "French": {
        "new": "Nouveau", "open": "Ouvrir", "save": "Enregistrer", "save_as": "Enregistrer sous", "close_tab": "Fermer",
        "run": "Exécuter", "settings": "Options", "theme": "Thème UI", "lang": "Langue", "about": "À propos",
        "adv_on": "Télémétrie: ON", "adv_off": "Télémétrie: OFF", "status_ready": "Statut: Prêt", "status_idle": "Statut: Inactif",
        "console_title": "Console d'exécution (ECO)", "clear_console": "Effacer", "empty_state": "Aucun document ouvert.\nCréez ou ouvrez un fichier pour commencer.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nEnvironnement de développement léger et moderne.\n\nCréé en 2026.",
        "adv_metrics": "Métriques", "sys_telemetry": "Télémétrie Système", "lines": "Lignes", "chars": "Caractères", "size": "Taille", "path": "Chemin",
        "opt_font": "Taille Police", "close_set": "✕ Fermer", "toggle_console": "👁 Afficher Console", "explorer": "Explorateur",
        "rename": "Refactoriser"
    },
    "Spanish": {
        "new": "Nuevo Archivo", "open": "Abrir", "save": "Guardar", "save_as": "Guardar como", "close_tab": "Cerrar Pestaña",
        "run": "Ejecutar", "settings": "Ajustes", "theme": "Tema UI", "lang": "Idioma", "about": "Acerca de",
        "adv_on": "Telemetría: ON", "adv_off": "Telemetría: OFF", "status_ready": "Estado: Listo", "status_idle": "Estado: Inactivo",
        "console_title": "Consola de Ejecución (ECO)", "clear_console": "Limpiar", "empty_state": "No hay documentos abiertos.\nCree o abra un archivo para comenzar.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nEntorno de desarrollo ligero y estructurado.\n\nCreado en 2026.",
        "adv_metrics": "Métricas de Archivo", "sys_telemetry": "Telemetría de Sistema", "lines": "Líneas", "chars": "Caracteres", "size": "Tamaño", "path": "Ruta",
        "opt_font": "Tamaño de Fuente", "close_set": "✕ Cerrar", "toggle_console": "👁 Alternar Consola", "explorer": "Explorador",
        "rename": "Refactorizar"
    },
    "Hungarian": {
        "new": "Új fájl", "open": "Megnyitás", "save": "Mentés", "save_as": "Mentés másként", "close_tab": "Lap bezárása",
        "run": "Futtatás", "settings": "Beállítások", "theme": "UI Téma", "lang": "Nyelv", "about": "FSTX névjegye",
        "adv_on": "Telemetria: BE", "adv_off": "Telemetria: KI", "status_ready": "Állapot: Kész", "status_idle": "Állapot: Üresjárat",
        "console_title": "Konzol kimenet (ECO)", "clear_console": "Törlés", "empty_state": "Nincs nyitott dokumentum.\nHozzon létre vagy nyisson meg egy fájlt.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nTiszta, könnyűsúlyú IDE struktúra.\n\nKészült 2026-ban.",
        "adv_metrics": "Fájl statisztika", "sys_telemetry": "Rendszer telemetria", "lines": "Sorok", "chars": "Karakterek", "size": "Méret", "path": "Elérési út",
        "opt_font": "Betűméret", "close_set": "✕ Bezárás", "toggle_console": "👁 Konsole Ki/Be", "explorer": "Fájlkezelő",
        "rename": "Refaktorálás"
    },
    "Italian": {
        "new": "Nuovo File", "open": "Apri File", "save": "Salva", "save_as": "Salva Come", "close_tab": "Chiudi Tab",
        "run": "Esegui", "settings": "Impostazioni", "theme": "Tema UI", "lang": "Lingua", "about": "Informazioni",
        "adv_on": "Telemetria: ON", "adv_off": "Telemetria: OFF", "status_ready": "Stato: Pronto", "status_idle": "Stato: Inattivo",
        "console_title": "Console di Esecuzione (ECO)", "clear_console": "Cancella", "empty_state": "Nessun buffer aperto.\nCrea o importa un file per iniziare.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nAmbiente di sviluppo leggero di nuova generazione.\n\nCreato nel 2026.",
        "adv_metrics": "Metriche File", "sys_telemetry": "Telemetria Sistema", "lines": "Linee", "chars": "Caratteri", "size": "Dimensione", "path": "Percorso",
        "opt_font": "Dimensione Font", "close_set": "✕ Chiudi Pannelli", "toggle_console": "👁 Alterna Console", "explorer": "Esploratore",
        "rename": "Refactoring"
    },
    "Polish": {
        "new": "Nowy Plik", "open": "Otwórz Plik", "save": "Zapisz", "save_as": "Zapisz Jako", "close_tab": "Zamknij Kartę",
        "run": "Uruchom", "settings": "Ustawienia", "theme": "Motyw UI", "lang": "Język", "about": "O Programie",
        "adv_on": "Telemetria: WŁ", "adv_off": "Telemetria: WYŁ", "status_ready": "Status: Gotowy", "status_idle": "Status: Bezczynny",
        "console_title": "Konsola Wyjściowa (ECO)", "clear_console": "Wyczyść", "empty_state": "Brak otwartych plików.\nUtwórz lub zaimportuj plik, aby zacząć.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nNowoczesne, lekkie środowisko programistyczne.\n\nUtworzono w 2026 roku.",
        "adv_metrics": "Metryki Pliku", "sys_telemetry": "Telemetria Systemu", "lines": "Linie", "chars": "Znaki", "size": "Rozmiar", "path": "Ścieżka",
        "opt_font": "Rozmiar Czcionki", "close_set": "✕ Zamknij Panele", "toggle_console": "👁 Przełącz Konsolę", "explorer": "Eksplorator",
        "rename": "Refaktoryzuj"
    },
    "Portuguese": {
        "new": "Novo Arquivo", "open": "Abrir Arquivo", "save": "Salvar", "save_as": "Salvar Como", "close_tab": "Fechar Aba",
        "run": "Executar", "settings": "Configurações", "theme": "Tema UI", "lang": "Idioma", "about": "Sobre o FSTX",
        "adv_on": "Telemetria: LIGADO", "adv_off": "Telemetria: DESLIGADO", "status_ready": "Status: Pronto", "status_idle": "Status: Ocioso",
        "console_title": "Console de Execução (ECO)", "clear_console": "Limpar", "empty_state": "Nenhum arquivo aberto.\nCrie ou importe um arquivo para iniciar.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nAmbiente de desenvolvimento estruturado e leve.\n\nCriado em 2026.",
        "adv_metrics": "Métricas do Arquivo", "sys_telemetry": "Telemetria do Sistema", "lines": "Linhas", "chars": "Caracteres", "size": "Tamanho", "path": "Caminho",
        "opt_font": "Tamanho da Fonte", "close_set": "✕ Fechar Painéis", "toggle_console": "👁 Alternar Console", "explorer": "Explorador",
        "rename": "Refatorar"
    },
    "Dutch": {
        "new": "Nieuw Bestand", "open": "Bestand Openen", "save": "Opslaan", "save_as": "Opslaan Als", "close_tab": "Tab Sluiten",
        "run": "Uitvoeren", "settings": "Instellingen", "theme": "UI Thema", "lang": "Taal", "about": "Over FSTX",
        "adv_on": "Telemetrie: AAN", "adv_off": "Telemetrie: UIT", "status_ready": "Status: Gereed", "status_idle": "Status: Standby",
        "console_title": "Uitvoerconsole (ECO)", "clear_console": "Wissen", "empty_state": "Geen geopende documenten.\nMaak of open een bestand om te beginnen.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nVolgende generatie lichtgewicht ontwikkelomgeving.\n\nGemaakt in 2026.",
        "adv_metrics": "Bestandsstatistieken", "sys_telemetry": "Systeemtelemetrie", "lines": "Regels", "chars": "Tekens", "size": "Grootte", "path": "Pad",
        "opt_font": "Lettergrootte", "close_set": "✕ Sluiten", "toggle_console": "👁 Console Schakelen", "explorer": "Verkenner",
        "rename": "Refactoring"
    },
    "Swedish": {
        "new": "Ny Fil", "open": "Öppna Fil", "save": "Spara", "save_as": "Spara Som", "close_tab": "Stäng Flik",
        "run": "Kör Kod", "settings": "Inställningar", "theme": "UI Thema", "lang": "Språk", "about": "Om FSTX",
        "adv_on": "Telemetri: PÅ", "adv_off": "Telemetri: AV", "status_ready": "Status: Redo", "status_idle": "Status: Viloläge",
        "console_title": "Exekveringskonsol (ECO)", "clear_console": "Rensa", "empty_state": "Inga öppna filer.\nSkapa eller importera en fil för att starta.",
        "about_text": f"FSTX Code Studio {APP_VERSION}\nNästa generations lätta utvecklingsmiljö.\n\nSkapad 2026.",
        "adv_metrics": "Filmetrik", "sys_telemetry": "Systemtelemetri", "lines": "Rader", "chars": "Tecken", "size": "Storlek", "path": "Sökväg",
        "opt_font": "Textstorlek", "close_set": "✕ Stäng Paneler", "toggle_console": "👁 Växla Konsol", "explorer": "Utforskare",
        "rename": "Refaktorera"
    }
}

# Core Comprehensive Styling Engine Configurations
THEME_PRESETS = {
    "Dark Modern": {
        "bg_main": "#1e1e24", "bg_ribbon": "#16161a", "bg_widget": "#2a2a32", "fg_text": "#f1f1f5",
        "accent": "#007acc", "accent_hover": "#0098ff", "editor_bg": "#1e1e1e", "editor_fg": "#d4d4d4",
        "console_bg": "#121214", "console_fg": "#4af626", "border": "#2d2d34"
    },
    "Light Modern": {
        "bg_main": "#f3f3f7", "bg_ribbon": "#e9e9f0", "bg_widget": "#ffffff", "fg_text": "#232329",
        "accent": "#007acc", "accent_hover": "#005999", "editor_bg": "#ffffff", "editor_fg": "#232329",
        "console_bg": "#f3f3f3", "console_fg": "#1e1e1e", "border": "#cccccc"
    },
    "Windows 9X": {
        "bg_main": "#d4d0c8", "bg_ribbon": "#d4d0c8", "bg_widget": "#d4d0c8", "fg_text": "#000000",
        "accent": "#000080", "accent_hover": "#0a0a95", "editor_bg": "#ffffff", "editor_fg": "#000000",
        "console_bg": "#ffffff", "console_fg": "#000000", "border": "#808080"
    },
    "Windows XP": {
        "bg_main": "#ece9d8", "bg_ribbon": "#739ed5", "bg_widget": "#fbfafd", "fg_text": "#000000",
        "accent": "#245edb", "accent_hover": "#316ac5", "editor_bg": "#ffffff", "editor_fg": "#000000",
        "console_bg": "#ffffff", "console_fg": "#000080", "border": "#919b9c"
    },
    "Windows Vista": {
        "bg_main": "#cfdceb", "bg_ribbon": "#a2bad6", "bg_widget": "#dbe5f0", "fg_text": "#1e2d3d",
        "accent": "#2b567d", "accent_hover": "#3d7ab0", "editor_bg": "#f9fbfd", "editor_fg": "#0a111a",
        "console_bg": "#1a222a", "console_fg": "#aed2f2", "border": "#7897b8"
    },
    "Matrix Digital Rain": {
        "bg_main": "#000000", "bg_ribbon": "#0d0d0d", "bg_widget": "#141414", "fg_text": "#00ff00",
        "accent": "#00ff00", "accent_hover": "#33ff33", "editor_bg": "#000000", "editor_fg": "#00ff00",
        "console_bg": "#000000", "console_fg": "#ffffff", "border": "#00ff00"
    },
    "Cyberpunk Neon": {
        "bg_main": "#0f051d", "bg_ribbon": "#1a0b2e", "bg_widget": "#2c124d", "fg_text": "#00ffff",
        "accent": "#ff007f", "accent_hover": "#ff00aa", "editor_bg": "#0f051d", "editor_fg": "#ffff00",
        "console_bg": "#1a0b2e", "console_fg": "#00ffff", "border": "#ff007f"
    }
}


class LineNumberCanvas(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, highlightthickness=0, borderwidth=0, **kwargs)
        self.text_widget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = i.split(".")[0]
            self.create_text(
                self.winfo_width() - 6, y, anchor="ne", text=linenum,
                font=(FONT_FAMILY, self.text_widget["font"].actual("size")), fill="#71717a"
            )
            i = self.text_widget.index(f"{i}+1line")


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(*cmd)
        except Exception:
            return None
        if args[0] in ("insert", "delete", "replace") or args[0] in "yview" or (len(args) > 1 and args[1] in ("moveto", "scroll")):
            self.event_generate("<<TextModified>>", when="tail")
        return result


class EditorTab(tk.Frame):
    def __init__(self, master, app_reference, file_path=None):
        super().__init__(master)
        self.app = app_reference
        self.file_path = file_path
        self.is_modified = False
        self.font_size = DEFAULT_FONT_SIZE

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text_area = CustomText(
            self, wrap="none", undo=True, font=(FONT_FAMILY, self.font_size),
            borderwidth=0, highlightthickness=0
        )
        self.line_canvas = LineNumberCanvas(self, self.text_area, width=42)
        self.line_canvas.grid(row=0, column=0, sticky="ns")
        self.text_area.grid(row=0, column=1, sticky="nsew", padx=4, pady=2)

        self.v_scroll = ttk.Scrollbar(self, orient="vertical", command=self.text_area.yview)
        self.v_scroll.grid(row=0, column=2, sticky="ns")
        self.h_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.text_area.xview)
        self.h_scroll.grid(row=1, column=1, sticky="ew")
        
        self.text_area.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.text_area.bind("<<TextModified>>", self.on_text_modified)
        self.text_area.bind("<Configure>", lambda e: self.line_canvas.redraw())

        if self.file_path:
            self.load_file()
        else:
            self.display_name = "Untitled"

    def load_file(self):
        try:
            if self.file_path.lower().endswith(".fstx"):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                content = data.get("source_payload", "")
            else:
                with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.text_area.edit_reset()
            self.text_area.edit_modified(False)
            self.display_name = os.path.basename(self.file_path)
            self.is_modified = False
        except Exception as e:
            messagebox.showerror("IO Read Error", f"Failed to open resource:\n{str(e)}")

    def on_text_modified(self, event=None):
        if self.text_area.edit_modified():
            if not self.is_modified:
                self.is_modified = True
                self.app.mark_tab_modified(self)
        self.line_canvas.redraw()
        self.app.update_advanced_data()

    def update_font_size(self, size):
        self.font_size = max(MIN_FONT_SIZE, min(size, MAX_FONT_SIZE))
        self.text_area.configure(font=(FONT_FAMILY, self.font_size))
        self.line_canvas.redraw()


class FSTXCodeStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1300x820")
        
        # INTERCEPT AND BIND SAFELY TO PREVENT THREAD FREEZING
        self.protocol("WM_DELETE_WINDOW", self.on_close_application)

        self.current_lang = "English"
        self.current_theme = "Dark Modern"
        self.is_advanced_mode = False
        self.console_visible = False
        self.tabs_list = []
        self.active_tab = None

        # Build Master UI Grid Layout Hierarchy System
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- TOP RIBBON CONTROLS INTERFACE ---
        self.ribbon = tk.Frame(self, height=45, bd=1, relief="raised")
        self.ribbon.grid(row=0, column=0, sticky="ew")
        self.ribbon.grid_propagate(False)

        self.brand_lbl = tk.Label(self.ribbon, text="FSTX Core 2.2", font=(FONT_FAMILY, 12, "bold"))
        self.brand_lbl.pack(side="left", padx=12, pady=8)

        self.btn_new = tk.Button(self.ribbon, text="New File", font=(FONT_FAMILY, 10), command=self.create_new_tab, padx=6)
        self.btn_new.pack(side="left", padx=4, pady=6)

        self.btn_open = tk.Button(self.ribbon, text="Open File", font=(FONT_FAMILY, 10), command=self.trigger_open_file, padx=6)
        self.btn_open.pack(side="left", padx=4, pady=6)

        self.btn_save = tk.Button(self.ribbon, text="Save", font=(FONT_FAMILY, 10), command=self.trigger_save_file, padx=6)
        self.btn_save.pack(side="left", padx=4, pady=6)

        self.btn_rename = tk.Button(self.ribbon, text="Refactor", font=(FONT_FAMILY, 10), command=self.trigger_rename_active_file, padx=6)
        self.btn_rename.pack(side="left", padx=4, pady=6)

        self.btn_run = tk.Button(self.ribbon, text="▶ Run Code", font=(FONT_FAMILY, 10, "bold"), fg="#ffffff", bg="#107c41", command=self.run_active_code, padx=10)
        self.btn_run.pack(side="left", padx=12, pady=6)

        self.btn_toggle_eco = tk.Button(self.ribbon, text="👁 Toggle Console", font=(FONT_FAMILY, 10), command=self.toggle_console_visibility, padx=6)
        self.btn_toggle_eco.pack(side="left", padx=4, pady=6)

        self.btn_telemetry = tk.Button(self.ribbon, text="Telemetry", font=(FONT_FAMILY, 10), command=self.toggle_advanced_ui, padx=6)
        self.btn_telemetry.pack(side="left", padx=4, pady=6)

        self.btn_settings = tk.Button(self.ribbon, text="⚙ Settings", font=(FONT_FAMILY, 10), command=self.show_settings_modal, padx=8)
        self.btn_settings.pack(side="right", padx=15, pady=6)

        # --- CENTRAL INTEGRATED WORKSPACE DESKTOP ---
        self.workspace = tk.Frame(self)
        self.workspace.grid(row=1, column=0, sticky="nsew", padx=4, pady=2)
        self.workspace.grid_columnconfigure(1, weight=1)
        self.workspace.grid_rowconfigure(0, weight=1)

        # Workspace Left Tree Explorer Layout Pane Component
        self.explorer_pane = tk.Frame(self.workspace, width=180, bd=1, relief="sunken")
        self.explorer_pane.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.explorer_pane.grid_propagate(False)
        self.explorer_pane.grid_columnconfigure(0, weight=1)
        self.explorer_pane.grid_rowconfigure(1, weight=1)

        self.explorer_title = tk.Label(self.explorer_pane, text="Workspace Explorer", font=(FONT_FAMILY, 9, "bold"))
        self.explorer_title.grid(row=0, column=0, sticky="w", padx=4, pady=4)

        self.explorer_box = tk.Listbox(self.explorer_pane, font=(FONT_FAMILY, 9), borderwidth=0, highlightthickness=0)
        self.explorer_box.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        self.explorer_box.bind("<<ListboxSelect>>", self.on_explorer_select)

        # Central Editor Core Viewport Grid Mapping Container Matrix
        self.center_split = tk.Frame(self.workspace)
        self.center_split.grid(row=0, column=1, sticky="nsew")
        self.center_split.grid_columnconfigure(0, weight=1)
        self.center_split.grid_rowconfigure(1, weight=1)

        # Tab bar element array manager interface
        self.tab_strip = tk.Frame(self.center_split, height=28)
        self.tab_strip.grid(row=0, column=0, sticky="ew")
        self.tab_strip.grid_rowconfigure(0, weight=1)

        self.btn_close_tab = tk.Button(self.tab_strip, text="✕ Close Tab", font=(FONT_FAMILY, 9), command=self.close_active_tab_context_pipeline, bg="#802424", fg="#ffffff")
        self.btn_close_tab.grid(row=0, column=0, padx=2, pady=2)

        self.tab_header_container = tk.Frame(self.tab_strip)
        self.tab_header_container.grid(row=0, column=1, sticky="nsew", padx=4)

        self.editor_viewport = tk.Frame(self.center_split, bd=1, relief="sunken")
        self.editor_viewport.grid(row=1, column=0, sticky="nsew")
        self.editor_viewport.grid_columnconfigure(0, weight=1)
        self.editor_viewport.grid_rowconfigure(0, weight=1)

        self.empty_state = tk.Label(self.editor_viewport, text="No active documents initialization pipeline loaded.")
        self.empty_state.grid(row=0, column=0)

        # ECO Frame Split Architecture (Strictly Controlled Height Constraints)
        self.sash = tk.Frame(self.center_split, height=5, cursor="sb_v_double_arrow", bg="#444444")
        self.sash.bind("<B1-Motion>", self.on_sash_drag_calculation)

        self.terminal_panel = tk.Frame(self.center_split, height=140)
        self.terminal_panel.grid_columnconfigure(0, weight=1)
        self.terminal_panel.grid_rowconfigure(1, weight=1)
        self.terminal_panel.grid_propagate(False)

        self.term_header = tk.Frame(self.terminal_panel, height=22)
        self.term_header.grid(row=0, column=0, sticky="ew")
        self.term_header.grid_columnconfigure(0, weight=1)

        self.term_title = tk.Label(self.term_header, text="ECO Output Engine", font=(FONT_FAMILY, 9, "bold"))
        self.term_title.grid(row=0, column=0, sticky="w", padx=6)

        self.btn_term_clear = tk.Button(self.term_header, text="Clear Engine", font=(FONT_FAMILY, 8), command=self.clear_console_buffer)
        self.btn_term_clear.grid(row=0, column=1, padx=4, pady=1)

        self.console_widget = tk.Text(self.terminal_panel, font=(FONT_FAMILY, 10), wrap="word", state="disabled")
        self.console_widget.grid(row=1, column=0, sticky="nsew", padx=4, pady=2)
        
        self.term_scroll = ttk.Scrollbar(self.terminal_panel, orient="vertical", command=self.console_widget.yview)
        self.term_scroll.grid(row=1, column=1, sticky="ns")
        self.console_widget.configure(yscrollcommand=self.term_scroll.set)

        # --- RIGHT TELEMETRY PANELS ---
        self.advanced_panel = tk.Frame(self.workspace, width=240, bd=1, relief="groove")
        self.advanced_panel.grid_columnconfigure(0, weight=1)
        self.advanced_panel.grid_propagate(False)

        # --- MODAL SETTINGS PREFERENCES FRAME SYSTEM (FIXED ADHESION) ---
        self.settings_modal = tk.Frame(self, bd=2, relief="groove", width=300, height=400)
        self.settings_modal.grid_columnconfigure(0, weight=1)
        self.settings_modal.grid_propagate(False)

        # --- FOOTER TRACE BAR ---
        self.footer = tk.Frame(self, height=22, bd=1, relief="sunken")
        self.footer.grid(row=2, column=0, sticky="ew")
        self.footer_lbl = tk.Label(self.footer, text="Status: Pipeline System Standby", font=(FONT_FAMILY, 9))
        self.footer_lbl.pack(side="left", padx=8, pady=2)

        self.current_process = None
        self.wire_universal_subsystems()
        self.apply_theme_engine_layer()
        self.apply_localization_matrix()
        self.create_new_tab()

    def wire_universal_subsystems(self):
        self.bind("<Control-n>", lambda e: self.create_new_tab())
        self.bind("<Control-o>", lambda e: self.trigger_open_file())
        self.bind("<Control-s>", lambda e: self.trigger_save_file())
        self.bind("<Control-w>", lambda e: self.close_active_tab_context_pipeline())
        self.bind("<KeyPress-F5>", lambda e: self.run_active_code())
        self.bind("<Control-MouseWheel>", self.handle_mouse_wheel_zoom)

    def apply_theme_engine_layer(self):
        st = THEME_PRESETS[self.current_theme]
        
        # Map Base Windows Layout Structures Colors
        self.configure(bg=st["bg_main"])
        self.ribbon.configure(bg=st["bg_ribbon"])
        self.workspace.configure(bg=st["bg_main"])
        self.explorer_pane.configure(bg=st["bg_ribbon"])
        self.center_split.configure(bg=st["bg_main"])
        self.tab_strip.configure(bg=st["bg_ribbon"])
        self.tab_header_container.configure(bg=st["bg_ribbon"])
        self.editor_viewport.configure(bg=st["editor_bg"])
        self.terminal_panel.configure(bg=st["bg_ribbon"])
        self.term_header.configure(bg=st["bg_ribbon"])
        self.advanced_panel.configure(bg=st["bg_ribbon"])
        self.settings_modal.configure(bg=st["bg_ribbon"])
        self.footer.configure(bg=st["bg_ribbon"])

        # Map System Components Text Colors Nodes
        self.brand_lbl.configure(bg=st["bg_ribbon"], fg=st["accent"])
        self.explorer_title.configure(bg=st["bg_ribbon"], fg=st["fg_text"])
        self.explorer_box.configure(bg=st["editor_bg"], fg=st["editor_fg"])
        self.term_title.configure(bg=st["bg_ribbon"], fg=st["fg_text"])
        self.footer_lbl.configure(bg=st["bg_ribbon"], fg=st["fg_text"])
        self.empty_state.configure(bg=st["editor_bg"], fg=st["fg_text"])

        # Map UI Action Elements Styles Loop
        buttons = [self.btn_new, self.btn_open, self.btn_save, self.btn_rename, self.btn_toggle_eco, self.btn_telemetry, self.btn_settings, self.btn_term_clear]
        for btn in buttons:
            btn.configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff", bd=1, relief="raised")

        self.console_widget.configure(bg=st["console_bg"], fg=st["console_fg"], insertbackground=st["console_fg"])

        # Map Dynamic Active Editing Buffer Layout Framework Components
        for tab in self.tabs_list:
            tab.configure(bg=st["bg_main"])
            tab.text_area.configure(bg=st["editor_bg"], fg=st["editor_fg"], insertbackground=st["editor_fg"])
            tab.line_canvas.configure(bg=st["editor_bg"])
            tab.line_canvas.redraw()

        self.refresh_tab_headers_ui()

    def apply_localization_matrix(self):
        tr = LOCALIZATION[self.current_lang]
        self.btn_new.configure(text=tr["new"])
        self.btn_open.configure(text=tr["open"])
        self.btn_save.configure(text=tr["save"])
        self.btn_rename.configure(text=tr["rename"])
        self.btn_run.configure(text=tr["run"])
        self.btn_toggle_eco.configure(text=tr["toggle_console"])
        self.btn_telemetry.configure(text=tr["adv_on"] if self.is_advanced_mode else tr["adv_off"])
        self.btn_settings.configure(text=tr["settings"])
        self.explorer_title.configure(text=tr["explorer"])
        self.term_title.configure(text=tr["console_title"])
        self.btn_term_clear.configure(text=tr["clear_console"])
        self.empty_state.configure(text=tr["empty_state"])
        self.update_footer_telemetry_track()
        self.update_advanced_data()

    def toggle_console_visibility(self):
        self.console_visible = not self.console_visible
        if self.console_visible:
            self.sash.grid(row=2, column=0, sticky="ew")
            self.terminal_panel.grid(row=3, column=0, sticky="nsew")
        else:
            self.sash.grid_forget()
            self.terminal_panel.grid_forget()

    def toggle_advanced_ui(self):
        self.is_advanced_mode = not self.is_advanced_mode
        if self.is_advanced_mode:
            self.advanced_panel.grid(row=0, column=2, sticky="nsew", padx=(2, 0))
            self.update_advanced_data()
        else:
            self.advanced_panel.grid_forget()
        self.apply_localization_matrix()

    def update_advanced_data(self):
        if not self.is_advanced_mode: return
        for child in self.advanced_panel.winfo_children(): child.destroy()
        tr = LOCALIZATION[self.current_lang]
        st = THEME_PRESETS[self.current_theme]

        header = tk.Label(self.advanced_panel, text=tr["adv_metrics"], font=(FONT_FAMILY, 10, "bold"), bg=st["bg_ribbon"], fg=st["accent"])
        header.grid(row=0, column=0, sticky="w", padx=6, pady=6)

        lines, chars, size, path = "0", "0", "0 B", "Transient Workspace"
        if self.active_tab:
            raw_text = self.active_tab.text_area.get("1.0", tk.END + "-1c")
            lines = str(len(raw_text.splitlines()))
            chars = str(len(raw_text))
            if self.active_tab.file_path and os.path.exists(self.active_tab.file_path):
                path = self.active_tab.file_path
                size = f"{os.path.getsize(path)} Bytes"
            else:
                size = f"{len(raw_text.encode('utf-8'))} Bytes (RAM)"

        metrics_array = [(tr["lines"], lines), (tr["chars"], chars), (tr["size"], size), (tr["path"], path)]
        for idx, (k, v) in enumerate(metrics_array):
            m_lbl = tk.Label(self.advanced_panel, text=f"{k}: {v}", font=(FONT_FAMILY, 9), bg=st["bg_ribbon"], fg=st["fg_text"], justify="left", wraplength=220)
            m_lbl.grid(row=idx+1, column=0, sticky="w", padx=12, pady=2)

        sys_header = tk.Label(self.advanced_panel, text=tr["sys_telemetry"], font=(FONT_FAMILY, 10, "bold"), bg=st["bg_ribbon"], fg="#107c41")
        sys_header.grid(row=5, column=0, sticky="w", padx=6, pady=(15, 6))

        sys_metrics = [("OS Platform", sys.platform), ("Interpreter", sys.version.split()[0]), ("Active Worker Threads", str(threading.active_count()))]
        for idx, (k, v) in enumerate(sys_metrics):
            s_lbl = tk.Label(self.advanced_panel, text=f"{k}: {v}", font=(FONT_FAMILY, 9), bg=st["bg_ribbon"], fg=st["fg_text"])
            s_lbl.grid(row=6+idx, column=0, sticky="w", padx=12, pady=2)

    def show_settings_modal(self):
        """Builds and firmly positions the persistent settings panel configuration overlay."""
        for child in self.settings_modal.winfo_children(): child.destroy()
        tr = LOCALIZATION[self.current_lang]
        st = THEME_PRESETS[self.current_theme]

        title = tk.Label(self.settings_modal, text=tr["settings"], font=(FONT_FAMILY, 12, "bold"), bg=st["bg_ribbon"], fg=st["accent"])
        title.pack(anchor="w", padx=12, pady=10)

        # Language Selection Section Block (Using native tk.OptionMenu for robust cross-platform Linux formatting compatibility)
        lang_lbl = tk.Label(self.settings_modal, text=tr["lang"], font=(FONT_FAMILY, 9), bg=st["bg_ribbon"], fg=st["fg_text"])
        lang_lbl.pack(anchor="w", padx=12, pady=(4, 0))
        lang_var = tk.StringVar(value=self.current_lang)
        lang_dropdown = tk.OptionMenu(self.settings_modal, lang_var, *list(LOCALIZATION.keys()), command=lambda l: self.change_language_runtime(l))
        lang_dropdown.configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff", highlightthickness=0, bd=1, relief="raised")
        lang_dropdown["menu"].configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff")
        lang_dropdown.pack(fill="x", padx=12, pady=4)

        # Theme Configuration Section Block
        theme_lbl = tk.Label(self.settings_modal, text=tr["theme"], font=(FONT_FAMILY, 9), bg=st["bg_ribbon"], fg=st["fg_text"])
        theme_lbl.pack(anchor="w", padx=12, pady=(8, 0))
        theme_var = tk.StringVar(value=self.current_theme)
        theme_dropdown = tk.OptionMenu(self.settings_modal, theme_var, *list(THEME_PRESETS.keys()), command=lambda t: self.change_theme_runtime(t))
        theme_dropdown.configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff", highlightthickness=0, bd=1, relief="raised")
        theme_dropdown["menu"].configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff")
        theme_dropdown.pack(fill="x", padx=12, pady=4)

        # Text Core Scaling Parameters Block
        font_lbl = tk.Label(self.settings_modal, text=tr["opt_font"], font=(FONT_FAMILY, 9), bg=st["bg_ribbon"], fg=st["fg_text"])
        font_lbl.pack(anchor="w", padx=12, pady=(8, 0))
        font_size_var = tk.StringVar(value=str(self.active_tab.font_size if self.active_tab else DEFAULT_FONT_SIZE))
        font_dropdown = tk.OptionMenu(self.settings_modal, font_size_var, *[str(x) for x in range(10, 30, 2)], command=lambda s: self.update_active_font_interface(int(s)))
        font_dropdown.configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff", highlightthickness=0, bd=1, relief="raised")
        font_dropdown["menu"].configure(bg=st["bg_widget"], fg=st["fg_text"], activebackground=st["accent_hover"], activeforeground="#ffffff")
        font_dropdown.pack(fill="x", padx=12, pady=4)

        # About Metadata Textbox Block
        about_box = tk.Text(self.settings_modal, height=4, font=(FONT_FAMILY, 9), bg=st["bg_main"], fg=st["fg_text"], bd=1, relief="solid")
        about_box.insert("1.0", tr["about_text"])
        about_box.configure(state="disabled")
        about_box.pack(fill="x", padx=12, pady=12)

        # Dismiss Actions Control Block
        btn_close = tk.Button(self.settings_modal, text=tr["close_set"], font=(FONT_FAMILY, 9), command=self.settings_modal.place_forget, bg=st["bg_widget"], fg=st["fg_text"])
        btn_close.pack(fill="x", padx=12, pady=8)

        # Snap Position Interface Overlay Anchor
        self.settings_modal.place(relx=0.99, rely=0.06, anchor="ne")

    def change_theme_runtime(self, selected_theme):
        self.current_theme = selected_theme
        self.apply_theme_engine_layer()
        self.show_settings_modal()

    def change_language_runtime(self, selected_lang):
        self.current_lang = selected_lang
        self.apply_localization_matrix()
        self.show_settings_modal()

    def update_active_font_interface(self, size):
        if self.active_tab: self.active_tab.update_font_size(size)

    def on_sash_drag_calculation(self, event):
        total_height = self.center_split.winfo_height()
        sash_y = self.sash.winfo_y() + event.y
        if (sash_y > 100) and (total_height - sash_y - 5 > 25):
            self.terminal_panel.configure(height=total_height - sash_y - 5)

    def create_new_tab(self, file_path=None):
        if self.empty_state: self.empty_state.grid_forget()
        tab = EditorTab(self.editor_viewport, self, file_path=file_path)
        self.tabs_list.append(tab)

        st = THEME_PRESETS[self.current_theme]
        btn = tk.Button(
            self.tab_header_container, text=tab.display_name, font=(FONT_FAMILY, 9),
            command=lambda t=tab: self.switch_active_tab(t), bd=1, relief="groove"
        )
        tab.handle_button = btn
        self.switch_active_tab(tab)
        self.sync_explorer_view()

    def switch_active_tab(self, target_tab):
        if self.active_tab: self.active_tab.grid_forget()
        self.active_tab = target_tab
        if self.active_tab:
            self.active_tab.grid(row=0, column=0, sticky="nsew")
            self.active_tab.text_area.focus_set()
        else:
            self.empty_state.grid(row=0, column=0)
        self.refresh_tab_headers_ui()
        self.apply_localization_matrix()

    def refresh_tab_headers_ui(self):
        st = THEME_PRESETS[self.current_theme]
        for child in self.tab_header_container.winfo_children(): child.pack_forget()
        for idx, tab in enumerate(self.tabs_list):
            tab.handle_button.pack(side="left", padx=1, pady=1)
            if tab == self.active_tab:
                tab.handle_button.configure(bg=st["accent"], fg="#ffffff")
            else:
                tab.handle_button.configure(bg=st["bg_widget"], fg=st["fg_text"])

    def sync_explorer_view(self):
        self.explorer_box.delete(0, tk.END)
        for tab in self.tabs_list:
            self.explorer_box.insert(tk.END, tab.display_name)

    def on_explorer_select(self, event):
        selection = self.explorer_box.curselection()
        if selection:
            self.switch_active_tab(self.tabs_list[selection[0]])

    def mark_tab_modified(self, tab):
        if tab.is_modified and not tab.display_name.endswith("*"):
            tab.display_name += "*"
            tab.handle_button.configure(text=tab.display_name)
            self.sync_explorer_view()

    def trigger_open_file(self):
        """Natively opens file pickers securely within OS scope."""
        paths = filedialog.askopenfilenames(filetypes=SUPPORTED_FORMATS)
        if paths:
            for path in paths:
                already_open = False
                for tab in self.tabs_list:
                    if tab.file_path == path:
                        self.switch_active_tab(tab)
                        already_open = True
                        break
                if not already_open:
                    self.create_new_tab(file_path=path)

    def trigger_save_file(self):
        """Writes the active document content to disk with explicit typed extension enforcement."""
        if not self.active_tab: 
            return False
            
        if self.active_tab.file_path:
            try:
                text_content = self.active_tab.text_area.get("1.0", tk.END + "-1c")
                
                # Check extension case-insensitively
                if self.active_tab.file_path.lower().endswith(".fstx"):
                    packaged_payload = {
                        "editor_context": "FSTX Structural Map Asset Container",
                        "app_build_version": APP_VERSION,
                        "source_payload": text_content
                    }
                    with open(self.active_tab.file_path, "w", encoding="utf-8") as f:
                        json.dump(packaged_payload, f, indent=4)
                else:
                    # Write exact raw formatting typed by user
                    with open(self.active_tab.file_path, "w", encoding="utf-8") as f:
                        f.write(text_content)
                
                self.active_tab.is_modified = False
                self.active_tab.text_area.edit_modified(False)
                self.active_tab.display_name = os.path.basename(self.active_tab.file_path)
                self.switch_active_tab(self.active_tab)
                self.sync_explorer_view()
                return True
            except Exception as e:
                messagebox.showerror("Disk Write Exception", f"Could not perform save action:\n{str(e)}")
                return False
                
        return self.trigger_save_as_file()

    def trigger_save_as_file(self):
        if not self.active_tab: 
            return False
            
        # Dialog opens without hardcoded default filters forcing .fstx
        dest_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save As Custom Production Format...",
            filetypes=SUPPORTED_FORMATS
        )
        
        if dest_path:
            self.active_tab.file_path = dest_path
            return self.trigger_save_file()
        return False

    def trigger_rename_active_file(self):
        """Changes the name of the file on disk instantly without losing tab state data."""
        if not self.active_tab:
            messagebox.showwarning("Refactor Action Boundary", "No active file open to refactor.")
            return

        if not self.active_tab.file_path or not os.path.exists(self.active_tab.file_path):
            messagebox.showwarning("Refactor Action Boundary", "Please save this workspace file locally before refactoring.")
            return

        old_path = self.active_tab.file_path
        old_dir = os.path.dirname(old_path)
        old_name = os.path.basename(old_path)

        new_name = simpledialog.askstring("Refactor File Pipeline", f"Enter a new name for '{old_name}':", initialvalue=old_name)
        
        if not new_name or new_name.strip() == old_name:
            return

        new_path = os.path.join(old_dir, new_name.strip())

        try:
            if os.path.exists(new_path):
                if not messagebox.askyesno("Overwrite Alert", f"A file named '{new_name}' already exists. Overwrite?"):
                    return
            
            # Save any unsaved text changes first before moving
            self.trigger_save_file()
            
            # Execute filesystem rename operation
            os.rename(old_path, new_path)
            
            # Update workspace memory states
            self.active_tab.file_path = new_path
            self.active_tab.display_name = new_name
            self.active_tab.handle_button.configure(text=new_name)
            self.sync_explorer_view()
            self.apply_localization_matrix()
            
        except Exception as e:
            messagebox.showerror("File IO Refactor Error", f"Could not update filename on disk:\n{str(e)}")

    def close_active_tab_context_pipeline(self):
        if not self.active_tab: return
        t = self.active_tab
        if t.is_modified:
            ans = messagebox.askyesnocancel("Unsaved Modifications Detected", f"Save modifications to {t.display_name.strip('*')}?")
            if ans is True:
                if not self.trigger_save_file(): return
            elif ans is None:
                return
        idx = self.tabs_list.index(t)
        t.handle_button.destroy()
        t.destroy()
        self.tabs_list.remove(t)
        self.switch_active_tab(self.tabs_list[idx-1] if self.tabs_list else None)
        self.sync_explorer_view()

    def run_active_code(self):
        if not self.active_tab: return
        if self.active_tab.is_modified or not self.active_tab.file_path:
            if messagebox.askyesno("Save Action Boundary Required", "Changes must be written to disk before runtime execution. Save now?"):
                if not self.trigger_save_file(): return
            else: return

        if not self.console_visible: self.toggle_console_visibility()
        self.execute_script_pipeline(self.active_tab.file_path)

    def execute_script_pipeline(self, target_path):
        if self.current_process and self.current_process.poll() is None: return
        self.clear_console_buffer()
        
        if not target_path.lower().endswith(".py"):
            self.write_to_console_output("[ECO System Core Alert]: Native code compilation requires a standalone .py environment script.\n")
            return

        self.write_to_console_output(f">> Spawning Execution Thread Pipeline For: {os.path.basename(target_path)}\n")
        threading.Thread(target=self._async_subprocess_execution, args=(target_path,), daemon=True).start()

    def _async_subprocess_execution(self, target_path):
        try:
            self.current_process = subprocess.Popen(
                [sys.executable, "-u", target_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, bufsize=1, creationflags=(subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            )
            def read_out():
                for line in self.current_process.stdout: self.write_to_console_output(line)
            def read_err():
                for line in self.current_process.stderr: self.write_to_console_output(line)
            
            t1 = threading.Thread(target=read_out, daemon=True)
            t2 = threading.Thread(target=read_err, daemon=True)
            t1.start(); t2.start(); t1.join(); t2.join()
            self.current_process.wait()
            self.write_to_console_output(f"\n>> Pipeline Disposed. Exit Code: {self.current_process.returncode}\n")
        except Exception as e:
            self.write_to_console_output(f"\n>> Pipeline Execution Fault: {str(e)}\n")

    def write_to_console_output(self, msg):
        self.console_widget.configure(state="normal")
        self.console_widget.insert(tk.END, msg)
        self.console_widget.see(tk.END)
        self.console_widget.configure(state="disabled")

    def clear_console_buffer(self):
        self.console_widget.configure(state="normal")
        self.console_widget.delete("1.0", tk.END)
        self.console_widget.configure(state="disabled")

    def handle_mouse_wheel_zoom(self, event):
        if not self.active_tab: return
        self.active_tab.update_font_size(self.active_tab.font_size + (1 if event.delta > 0 else -1))

    def update_footer_telemetry_track(self):
        tr = LOCALIZATION[self.current_lang]
        if self.active_tab:
            p = self.active_tab.file_path if self.active_tab.file_path else "Unbound RAM Buffer"
            self.footer_lbl.configure(text=f"{tr['status_ready']} | Target Context Asset: {p}")
        else:
            self.footer_lbl.configure(text=tr["status_idle"])

    def on_close_application(self):
        """Safely disposes of active resources and worker threads during shutdown."""
        while self.tabs_list:
            self.switch_active_tab(self.tabs_list[-1])
            count_before = len(self.tabs_list)
            self.close_active_tab_context_pipeline()
            if len(self.tabs_list) == count_before: return
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = FSTXCodeStudio()
    app.mainloop()