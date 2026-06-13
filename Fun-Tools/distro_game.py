# ==========================================
# LINUX DISTRO GUESSING GAME — DELUXE EDITION
# Only standard library (tkinter) required
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
import time

# ==========================================
# DISTRO DATABASE
# Each distro has: name, aliases, hint(s), family, year, difficulty
# ==========================================

DISTROS = [
    {"name": "ubuntu",       "aliases": [],                       "family": "Debian",  "year": 2004, "difficulty": 1,
     "hints": ["Orange logo. Very popular for beginners.", "Made by Canonical.", "Default desktop is GNOME."]},
    {"name": "debian",       "aliases": [],                       "family": "Debian",  "year": 1993, "difficulty": 1,
     "hints": ["Very stable distro. Ubuntu is based on it.", "Logo is a red swirl.", "Named after creator + his girlfriend."]},
    {"name": "arch",         "aliases": ["archlinux"],            "family": "Arch",    "year": 2002, "difficulty": 1,
     "hints": ["People say: 'I use this distro btw.'", "Rolling release, install from scratch.", "Uses the pacman package manager."]},
    {"name": "fedora",       "aliases": [],                       "family": "RPM",     "year": 2003, "difficulty": 1,
     "hints": ["Blue logo. Sponsored by Red Hat.", "Cutting-edge upstream of RHEL.", "Uses DNF as package manager."]},
    {"name": "mint",         "aliases": ["linuxmint"],            "family": "Debian",  "year": 2006, "difficulty": 1,
     "hints": ["Green distro based on Ubuntu.", "Ships with Cinnamon desktop.", "Very newcomer friendly."]},
    {"name": "kali",         "aliases": ["kalilinux"],            "family": "Debian",  "year": 2013, "difficulty": 1,
     "hints": ["Used for hacking and penetration testing.", "Dragon logo.", "Made by Offensive Security."]},
    {"name": "manjaro",      "aliases": [],                       "family": "Arch",    "year": 2011, "difficulty": 1,
     "hints": ["Easy version of Arch Linux.", "Green logo.", "Has its own stable repos."]},
    {"name": "opensuse",     "aliases": ["suse"],                 "family": "RPM",     "year": 2005, "difficulty": 2,
     "hints": ["Green chameleon mascot named Geeko.", "Uses zypper package manager.", "Comes in Leap and Tumbleweed."]},
    {"name": "popos",        "aliases": ["pop", "pop_os"],        "family": "Debian",  "year": 2017, "difficulty": 2,
     "hints": ["Made by System76.", "Ships on their laptops.", "Has its own COSMIC desktop."]},
    {"name": "gentoo",       "aliases": [],                       "family": "Source",  "year": 2002, "difficulty": 2,
     "hints": ["You compile almost everything yourself.", "Uses the Portage package manager.", "Mascot is a purple creature called Larry."]},
    {"name": "slackware",    "aliases": [],                       "family": "Other",   "year": 1993, "difficulty": 3,
     "hints": ["One of the oldest Linux distros.", "Created by Patrick Volkerding.", "Known for simplicity and minimal automation."]},
    {"name": "alpine",       "aliases": [],                       "family": "Other",   "year": 2005, "difficulty": 2,
     "hints": ["Very small distro often used in Docker.", "Built on musl and BusyBox.", "Uses the apk package manager."]},
    {"name": "mxlinux",      "aliases": ["mx"],                   "family": "Debian",  "year": 2014, "difficulty": 3,
     "hints": ["Lightweight distro based on Debian.", "Top of DistroWatch for years.", "Default desktop is Xfce."]},
    {"name": "endeavouros",  "aliases": ["endeavour"],            "family": "Arch",    "year": 2019, "difficulty": 2,
     "hints": ["Arch-based distro with easy installer.", "Spiritual successor to Antergos.", "Purple rocket logo."]},
    {"name": "garuda",       "aliases": [],                       "family": "Arch",    "year": 2020, "difficulty": 2,
     "hints": ["Gaming-focused Arch distro.", "Flashy themes, often dragon themed.", "Uses BTRFS by default."]},
    {"name": "void",         "aliases": ["voidlinux"],            "family": "Other",   "year": 2008, "difficulty": 3,
     "hints": ["Linux distro without systemd.", "Uses runit as init.", "Has its own XBPS package manager."]},
    {"name": "nixos",        "aliases": ["nix"],                  "family": "Other",   "year": 2003, "difficulty": 2,
     "hints": ["Uses special config files for the whole system.", "Reproducible and declarative.", "Snowflake-style logo."]},
    {"name": "qubes",        "aliases": ["qubesos"],              "family": "Other",   "year": 2012, "difficulty": 2,
     "hints": ["Security-focused distro using virtual machines.", "Edward Snowden recommends it.", "Each app runs in its own qube."]},
    {"name": "tails",        "aliases": [],                       "family": "Debian",  "year": 2009, "difficulty": 2,
     "hints": ["Privacy distro that routes traffic through Tor.", "Runs as a live USB.", "Leaves no trace on the host machine."]},
    {"name": "parrot",       "aliases": ["parrotos"],             "family": "Debian",  "year": 2013, "difficulty": 2,
     "hints": ["Security distro similar to Kali.", "Bird-themed logo.", "Made by Parrot Security."]},
    {"name": "elementary",   "aliases": ["elementaryos"],         "family": "Debian",  "year": 2011, "difficulty": 2,
     "hints": ["Looks similar to macOS.", "Uses the Pantheon desktop.", "Pay-what-you-want model."]},
    {"name": "zorin",        "aliases": ["zorinos"],              "family": "Debian",  "year": 2009, "difficulty": 2,
     "hints": ["Ubuntu-based distro that mimics Windows for newcomers.", "Made in Ireland.", "Comes in Core and Pro editions."]},
    {"name": "centos",       "aliases": [],                       "family": "RPM",     "year": 2004, "difficulty": 2,
     "hints": ["Free rebuild of Red Hat Enterprise Linux.", "Now lives on as CentOS Stream.", "Long used on servers."]},
    {"name": "rocky",        "aliases": ["rockylinux"],           "family": "RPM",     "year": 2021, "difficulty": 3,
     "hints": ["RHEL-compatible distro created after CentOS pivot.", "Named after a CentOS co-founder.", "Run by the RESF foundation."]},
    {"name": "almalinux",    "aliases": ["alma"],                 "family": "RPM",     "year": 2021, "difficulty": 3,
     "hints": ["Another RHEL-compatible distro from 2021.", "Backed by CloudLinux.", "Logo features a star."]},
    {"name": "raspbian",     "aliases": ["raspberrypios"],        "family": "Debian",  "year": 2012, "difficulty": 2,
     "hints": ["Default OS for the Raspberry Pi.", "Based on Debian.", "Renamed to Raspberry Pi OS."]},
    {"name": "puppy",        "aliases": ["puppylinux"],           "family": "Other",   "year": 2003, "difficulty": 3,
     "hints": ["Tiny distro that runs entirely in RAM.", "Named after a small animal.", "Great for reviving old PCs."]},
    {"name": "deepin",       "aliases": [],                       "family": "Debian",  "year": 2008, "difficulty": 3,
     "hints": ["Chinese distro with a very polished desktop.", "Has its own DDE desktop environment.", "Known for slick aesthetics."]},
    {"name": "solus",        "aliases": [],                       "family": "Other",   "year": 2015, "difficulty": 3,
     "hints": ["Independent rolling distro.", "Created the Budgie desktop.", "Uses the eopkg package manager."]},
    {"name": "bodhi",        "aliases": ["bodhilinux"],           "family": "Debian",  "year": 2011, "difficulty": 3,
     "hints": ["Lightweight Ubuntu-based distro.", "Uses the Moksha desktop (Enlightenment fork).", "Name comes from Buddhism."]},
]

FAMILIES = sorted({d["family"] for d in DISTROS})

# ==========================================
# PERSISTENT HIGH SCORES
# ==========================================

SCORE_FILE = os.path.join(os.path.expanduser("~"), ".distro_game_scores.json")

def load_scores():
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_scores(scores):
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except Exception:
        pass

# ==========================================
# THEME
# ==========================================

BG       = "#0f1115"
PANEL    = "#181b22"
ACCENT   = "#7CFC00"   # lime
ACCENT2  = "#00BFFF"   # cyan
WARN     = "#ff5555"
TEXT     = "#f5f5f5"
MUTED    = "#9aa0a6"
GOLD     = "#ffd166"

FONT_TITLE = ("Helvetica", 22, "bold")
FONT_H2    = ("Helvetica", 14, "bold")
FONT_BODY  = ("Helvetica", 13)
FONT_MONO  = ("Courier", 12)

# ==========================================
# GAME LOGIC
# ==========================================

GAMEMODES = {
    "classic":      "10 rounds. One hint per distro.",
    "hardcore":     "10 rounds. Only the first (hardest) hint. No extra hints.",
    "progressive":  "10 rounds. Start with subtle hint, reveal more as time passes. Faster = more points.",
    "multichoice":  "10 rounds. Pick the distro from 4 options.",
    "family":       "10 rounds. Guess the distro family (Debian, Arch, RPM, …).",
    "timeattack":   "60 seconds. Answer as many as you can.",
    "survival":     "Infinite rounds. One wrong answer ends the game.",
}

DIFFICULTY_LABELS = {1: "Easy", 2: "Medium", 3: "Hard"}


class DistroGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐧 Linux Distro Game — Deluxe")
        self.root.geometry("720x560")
        self.root.configure(bg=BG)
        self.root.minsize(680, 540)

        self.scores = load_scores()

        self.mode = tk.StringVar(value="classic")
        self.difficulty = tk.StringVar(value="all")

        self.build_menu()

    # ---------- helpers ----------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def label(self, parent, text, font=FONT_BODY, fg=TEXT, **kw):
        return tk.Label(parent, text=text, font=font, fg=fg, bg=parent["bg"], **kw)

    def button(self, parent, text, command, bg=ACCENT, fg="black", **kw):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         font=FONT_H2, activebackground=ACCENT2, relief="flat",
                         padx=14, pady=6, cursor="hand2", **kw)

    def normalize(self, s):
        return s.strip().lower().replace(" ", "").replace("-", "").replace("_", "")

    def is_correct(self, guess, distro):
        g = self.normalize(guess)
        if not g:
            return False
        candidates = [distro["name"]] + distro.get("aliases", [])
        return g in {self.normalize(c) for c in candidates}

    def filtered_pool(self):
        if self.difficulty.get() == "all":
            return DISTROS[:]
        target = int(self.difficulty.get())
        return [d for d in DISTROS if d["difficulty"] == target]

    # ---------- main menu ----------
    def build_menu(self):
        self.clear()
        self.root.configure(bg=BG)

        self.label(self.root, "🐧 Linux Distro Game", font=FONT_TITLE, fg=ACCENT).pack(pady=(20, 4))
        self.label(self.root, "Deluxe Edition", font=FONT_BODY, fg=MUTED).pack()

        box = tk.Frame(self.root, bg=PANEL, padx=20, pady=18)
        box.pack(padx=20, pady=18, fill="x")

        self.label(box, "Game Mode", font=FONT_H2, fg=ACCENT2).pack(anchor="w")
        for key, desc in GAMEMODES.items():
            row = tk.Frame(box, bg=PANEL)
            row.pack(anchor="w", fill="x", pady=2)
            tk.Radiobutton(row, text=key.capitalize(), variable=self.mode, value=key,
                           bg=PANEL, fg=TEXT, selectcolor=BG, activebackground=PANEL,
                           font=FONT_H2, anchor="w").pack(side="left")
            self.label(row, f"— {desc}", fg=MUTED).pack(side="left", padx=8)

        self.label(box, "Difficulty", font=FONT_H2, fg=ACCENT2).pack(anchor="w", pady=(12, 2))
        diff_row = tk.Frame(box, bg=PANEL)
        diff_row.pack(anchor="w")
        for val, lbl in [("all", "All"), ("1", "Easy"), ("2", "Medium"), ("3", "Hard")]:
            tk.Radiobutton(diff_row, text=lbl, variable=self.difficulty, value=val,
                           bg=PANEL, fg=TEXT, selectcolor=BG, activebackground=PANEL,
                           font=FONT_BODY).pack(side="left", padx=6)

        btns = tk.Frame(self.root, bg=BG)
        btns.pack(pady=6)
        self.button(btns, "▶  Start Game", self.start_game).pack(side="left", padx=6)
        self.button(btns, "🏆 High Scores", self.show_scores, bg=GOLD).pack(side="left", padx=6)
        self.button(btns, "❌ Quit", self.root.quit, bg=WARN, fg="white").pack(side="left", padx=6)

        self.label(self.root, f"{len(DISTROS)} distros loaded", fg=MUTED).pack(pady=(10, 0))

    # ---------- high scores ----------
    def show_scores(self):
        self.clear()
        self.label(self.root, "🏆 High Scores", font=FONT_TITLE, fg=GOLD).pack(pady=18)
        frame = tk.Frame(self.root, bg=PANEL, padx=24, pady=16)
        frame.pack(padx=24, pady=10, fill="both", expand=True)
        if not self.scores:
            self.label(frame, "No scores yet — play a round!", fg=MUTED).pack(pady=20)
        else:
            for mode, entry in sorted(self.scores.items()):
                self.label(frame, f"{mode.capitalize():<14}  best: {entry['best']}   last: {entry['last']}",
                           font=FONT_MONO).pack(anchor="w", pady=2)
        self.button(self.root, "← Back", self.build_menu).pack(pady=14)

    def record_score(self, mode, score):
        prev = self.scores.get(mode, {"best": 0, "last": 0})
        prev["last"] = score
        if score > prev["best"]:
            prev["best"] = score
        self.scores[mode] = prev
        save_scores(self.scores)

    # ---------- start game ----------
    def start_game(self):
        pool = self.filtered_pool()
        if len(pool) < 4:
            messagebox.showerror("Not enough distros", "Pick a wider difficulty.")
            return
        mode = self.mode.get()
        if mode == "timeattack":
            GameSession(self, pool, mode, time_limit=60).start()
        elif mode == "survival":
            GameSession(self, pool, mode, survival=True).start()
        else:
            GameSession(self, pool, mode, total_rounds=10).start()


# ==========================================
# GAME SESSION
# ==========================================

class GameSession:
    def __init__(self, app, pool, mode, total_rounds=None, time_limit=None, survival=False):
        self.app = app
        self.root = app.root
        self.pool = pool
        self.mode = mode
        self.total_rounds = total_rounds
        self.time_limit = time_limit
        self.survival = survival

        self.score = 0
        self.round = 0
        self.streak = 0
        self.start_time = None
        self.timer_job = None

        self.current = None
        self.hints_shown = 1
        self.q_start = 0

    # ---------- UI ----------
    def start(self):
        self.app.clear()
        self.root.configure(bg=BG)

        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=16, pady=10)
        tk.Button(top, text="← Quit", command=self.app.build_menu,
                  bg=PANEL, fg=TEXT, relief="flat", font=FONT_BODY,
                  activebackground=WARN, cursor="hand2").pack(side="left")
        self.status_label = tk.Label(top, text="", font=FONT_H2, fg=ACCENT2, bg=BG)
        self.status_label.pack(side="right")

        tk.Label(self.root, text=f"Mode: {self.mode.capitalize()}",
                 font=FONT_H2, fg=GOLD, bg=BG).pack()

        self.hint_frame = tk.Frame(self.root, bg=PANEL)
        self.hint_frame.pack(padx=20, pady=12, fill="x")
        self.hint_label = tk.Label(self.hint_frame, text="", font=FONT_BODY,
                                   fg=TEXT, bg=PANEL, wraplength=620, justify="left")
        self.hint_label.pack(padx=16, pady=14)

        self.answer_area = tk.Frame(self.root, bg=BG)
        self.answer_area.pack(pady=8, fill="x")

        self.result_label = tk.Label(self.root, text="", font=FONT_H2, bg=BG, fg=TEXT)
        self.result_label.pack(pady=6)

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(side="bottom", fill="x", pady=8)
        self.score_label = tk.Label(bottom, text="Score: 0", font=FONT_H2, fg=GOLD, bg=BG)
        self.score_label.pack(side="left", padx=16)
        self.streak_label = tk.Label(bottom, text="Streak: 0", font=FONT_BODY, fg=ACCENT, bg=BG)
        self.streak_label.pack(side="left")
        self.timer_label = tk.Label(bottom, text="", font=FONT_BODY, fg=ACCENT2, bg=BG)
        self.timer_label.pack(side="right", padx=16)

        if self.time_limit:
            self.start_time = time.time()
            self.tick_timer()

        self.next_question()

    def tick_timer(self):
        if not self.time_limit:
            return
        remaining = int(self.time_limit - (time.time() - self.start_time))
        if remaining <= 0:
            self.timer_label.config(text="Time: 0s")
            self.end_game()
            return
        self.timer_label.config(text=f"Time: {remaining}s")
        self.timer_job = self.root.after(250, self.tick_timer)

    # ---------- question setup ----------
    def next_question(self):
        # Total-round modes: stop when limit reached
        if self.total_rounds and self.round >= self.total_rounds:
            self.end_game()
            return

        self.round += 1
        self.current = random.choice(self.pool)
        self.hints_shown = 1
        self.q_start = time.time()
        self.result_label.config(text="")

        for w in self.answer_area.winfo_children():
            w.destroy()

        self.update_status()

        if self.mode == "family":
            self.show_family_question()
        elif self.mode == "multichoice":
            self.show_multichoice_question()
        else:
            self.show_text_question()

    def update_status(self):
        if self.survival:
            self.status_label.config(text=f"Round {self.round} • Lives: 1")
        elif self.total_rounds:
            self.status_label.config(text=f"Round {self.round}/{self.total_rounds}")
        else:
            self.status_label.config(text=f"Round {self.round}")

    # ---------- modes ----------
    def show_text_question(self):
        hints = self.current["hints"]
        if self.mode == "hardcore":
            text = f"Hint: {hints[0]}"
        elif self.mode == "progressive":
            text = "Hint: " + hints[0]
            self.schedule_progressive_hints()
        else:
            text = "Hint: " + random.choice(hints)
        self.hint_label.config(text=text)

        entry = tk.Entry(self.answer_area, font=("Helvetica", 16), width=28, justify="center",
                         bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat")
        entry.pack(pady=6)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self.submit_text(entry.get()))

        btn_row = tk.Frame(self.answer_area, bg=BG)
        btn_row.pack(pady=4)
        self.app.button(btn_row, "Submit", lambda: self.submit_text(entry.get())).pack(side="left", padx=4)
        if self.mode != "hardcore":
            self.app.button(btn_row, "Skip (-1)", self.skip, bg=WARN, fg="white").pack(side="left", padx=4)

    def schedule_progressive_hints(self):
        def reveal(idx):
            if self.current is None or idx >= len(self.current["hints"]):
                return
            if self.hints_shown != idx:
                return
            self.hints_shown = idx + 1
            shown = self.current["hints"][:self.hints_shown]
            self.hint_label.config(text="Hints:\n• " + "\n• ".join(shown))
            if idx + 1 < len(self.current["hints"]):
                self.root.after(4000, lambda: reveal(idx + 1))
        self.root.after(4000, lambda: reveal(1))

    def show_multichoice_question(self):
        self.hint_label.config(text="Hint: " + random.choice(self.current["hints"]))
        options = [self.current]
        others = [d for d in self.pool if d["name"] != self.current["name"]]
        options += random.sample(others, min(3, len(others)))
        random.shuffle(options)
        grid = tk.Frame(self.answer_area, bg=BG)
        grid.pack(pady=6)
        for i, opt in enumerate(options):
            b = tk.Button(grid, text=opt["name"], font=FONT_H2, width=14,
                          bg=PANEL, fg=TEXT, relief="flat", cursor="hand2",
                          activebackground=ACCENT,
                          command=lambda o=opt: self.submit_text(o["name"]))
            b.grid(row=i // 2, column=i % 2, padx=8, pady=6)

    def show_family_question(self):
        self.hint_label.config(text=f"Which family does '{self.current['name']}' belong to?")
        grid = tk.Frame(self.answer_area, bg=BG)
        grid.pack(pady=6)
        for i, fam in enumerate(FAMILIES):
            b = tk.Button(grid, text=fam, font=FONT_H2, width=14,
                          bg=PANEL, fg=TEXT, relief="flat", cursor="hand2",
                          activebackground=ACCENT,
                          command=lambda f=fam: self.submit_family(f))
            b.grid(row=i // 3, column=i % 3, padx=6, pady=6)

    # ---------- submission ----------
    def submit_text(self, guess):
        if self.mode == "family":
            return
        correct = self.app.is_correct(guess, self.current)
        self.resolve(correct, expected=self.current["name"])

    def submit_family(self, fam):
        correct = (fam == self.current["family"])
        self.resolve(correct, expected=f"{self.current['name']} → {self.current['family']}")

    def skip(self):
        self.score = max(0, self.score - 1)
        self.streak = 0
        self.result_label.config(text=f"⏭  Skipped. Answer was: {self.current['name']}", fg=MUTED)
        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text="Streak: 0")
        self.root.after(900, self.next_question)

    def resolve(self, correct, expected):
        if correct:
            self.streak += 1
            pts = 1
            if self.mode == "progressive":
                pts = max(1, 4 - self.hints_shown)  # fewer hints = more points
            if self.mode == "hardcore":
                pts = 2
            if self.streak >= 3:
                pts += 1  # streak bonus
            self.score += pts
            self.result_label.config(text=f"✅ Correct!  (+{pts})", fg=ACCENT)
        else:
            self.result_label.config(text=f"❌ Wrong! Answer: {expected}", fg=WARN)
            self.streak = 0
            if self.survival:
                self.score_label.config(text=f"Score: {self.score}")
                self.root.after(1400, self.end_game)
                return

        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text=f"Streak: {self.streak}")
        self.root.after(800, self.next_question)

    # ---------- end ----------
    def end_game(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.current = None
        self.app.record_score(self.mode, self.score)

        self.app.clear()
        self.root.configure(bg=BG)
        tk.Label(self.root, text="🎉 Game Over", font=FONT_TITLE, fg=ACCENT, bg=BG).pack(pady=30)
        tk.Label(self.root, text=f"Mode: {self.mode.capitalize()}", font=FONT_H2, fg=GOLD, bg=BG).pack()
        tk.Label(self.root, text=f"Final score: {self.score}", font=FONT_H2, fg=ACCENT2, bg=BG).pack(pady=8)

        best = self.app.scores.get(self.mode, {}).get("best", 0)
        tk.Label(self.root, text=f"Best ever: {best}", font=FONT_BODY, fg=MUTED, bg=BG).pack()

        btns = tk.Frame(self.root, bg=BG)
        btns.pack(pady=20)
        tk.Button(btns, text="🔁 Play Again", command=lambda: self.app.start_game(),
                  bg=ACCENT, fg="black", font=FONT_H2, relief="flat",
                  padx=14, pady=6, cursor="hand2").pack(side="left", padx=6)
        tk.Button(btns, text="🏠 Menu", command=self.app.build_menu,
                  bg=PANEL, fg=TEXT, font=FONT_H2, relief="flat",
                  padx=14, pady=6, cursor="hand2").pack(side="left", padx=6)


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    DistroGame(root)
    root.mainloop()
