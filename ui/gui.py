import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import datetime
import os
from settings.config import load_settings
import math

class RodentRefreshmentGUI:
    def __init__(self, run_program, stop_program, update_all_settings):
        self.run_program = run_program
        self.stop_program = stop_program
        self.update_all_settings = update_all_settings

        self.root = tk.Tk()
        self.root.title("Rodent Refreshment Regulator")

        self.settings = load_settings()
        self.selected_relays = self.settings['selected_relays']
        self.num_triggers = self.settings['num_triggers']

        self.create_widgets()

    def create_widgets(self):
        MIN_WIDTH = 1800
        MIN_HEIGHT = 1000

        def enforce_min_size(event):
            if self.root.winfo_width() < MIN_WIDTH:
                self.root.geometry(f"{MIN_WIDTH}x{self.root.winfo_height()}")
            if self.root.winfo_height() < MIN_HEIGHT:
                self.root.geometry(f"{self.root.winfo_width()}x{MIN_HEIGHT}")
        self.root.bind("<Configure>", enforce_min_size)

        terminal_frame = tk.Frame(self.root)
        terminal_frame.pack(side="bottom", fill="x")

        self.terminal_output = tk.Text(terminal_frame, height=14)
        self.terminal_output.pack(side="bottom", fill="x")
        self.terminal_output.insert("end", "System Messages will appear here.\n")

        terminal_scrollbar = tk.Scrollbar(terminal_frame, command=self.terminal_output.yview)
        terminal_scrollbar.pack(side='right', fill='y', before=self.terminal_output)
        self.terminal_output.config(yscrollcommand=terminal_scrollbar.set)

        self.print_to_terminal("Welcome to the Rodent Refreshment Regulator!")

        canvas = tk.Canvas(self.root)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas)
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        left_content_frame = tk.Frame(scrollable_frame)
        left_content_frame.pack(side='left', fill='both', expand=True)

        right_content_frame = tk.Frame(scrollable_frame)
        right_content_frame.pack(side='right', fill='both')

        welcome_label = tk.Label(left_content_frame, text="Welcome to the Rodent Refreshment Regulator Wizard", font=("Arial", 24, "bold"))
        welcome_label.pack(fill='x', padx=20, pady=(5, 3))

        subheaders_text = """
        Step 1: Answer the questions on the right side of the screen to suit your needs.
        Step 2: Press the 'Suggest Settings' button to receive setting recommendations in the terminal below.
        Step 3: Press the 'Push Settings' button to submit and save these setting recommendations.
        Step 4: (OPTIONAL) Adjust settings manually in the 'Advanced Settings' menu below if desired.\n               * Remember to save these changes using the 'Update Settings' button at the bottom of the Advanced Settings menu.
        Step 5: See the notes section below for additional information, and run the program when ready.
        Notes:
         * Questions pertaining to water volume are for EACH relay.
         * Water volume suggestions will always round UP based on the volume increments that your pumps are capable of outputting per trigger.\n      * The amount of water released defaults to 10uL/trigger.
         * Closing this window will stop the program. Please leave this window open for it to continue running.
         * An email can optionally be sent to you upon each successful pump trigger. See the ReadMe for setup instructions if desired.
         * CTRL+C is set to force close the program if required.
         * "Stagger" is the time that elapses between triggers of the same relay pair (if applicable). Changing this value is not recommended.\n      * This parameter is set based on the maximum electrical output of a Raspberry Pi-4. Only change if your hardware needs differ.
        """

        self.add_styled_text_single(left_content_frame, subheaders_text, scrollbar)

        questions_frame = tk.LabelFrame(right_content_frame, text="Answer These For Setting Suggestions", font=("Arial", 12, "bold"))
        questions_frame.pack(fill='x', padx=15, pady=(50, 30))

        questions = [
            "Water volume for relays 1 & 2 (uL):",
            "Water volume for relays 3 & 4 (uL):",
            "Water volume for relays 5 & 6 (uL):",
            "Water volume for relays 7 & 8 (uL):",
            "Water volume for relays 9 & 10 (uL):",
            "Water volume for relays 11 & 12 (uL):",
            "Water volume for relays 13 & 14 (uL):",
            "Water volume for relays 15 & 16 (uL):",
            "How often should each cage receive water? \n  (Seconds)",
            "Water window start (hour, 24-hour format):",
            "Water window end (hour, 24-hour format):"
        ]
        self.entries = {}

        for i, question in enumerate(questions):
            label = tk.Label(questions_frame, text=question)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(questions_frame, width=20)
            entry.insert(0, "0")
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.entries[question] = entry

        buttons_frame = tk.Frame(right_content_frame)
        buttons_frame.pack(fill='x', padx=5, pady=(1, 1))

        suggest_button = tk.Button(buttons_frame, text="Suggest Settings", command=self.suggest_settings)
        push_button = tk.Button(buttons_frame, text="Push Settings", command=self.push_settings)
        run_button = tk.Button(buttons_frame, text="Run Program", command=self.run_program)
        stop_button = tk.Button(buttons_frame, text="Stop Program", command=self.stop_program)

        suggest_button.grid(row=0, column=0, padx=5, pady=0, sticky="w")
        push_button.grid(row=0, column=1, padx=5, pady=0, sticky="w")
        run_button.grid(row=0, column=2, padx=5, pady=0, sticky="w")
        stop_button.grid(row=0, column=3, padx=5, pady=0, sticky="w")

        suggest_button.config(height=3)
        push_button.config(height=3)
        run_button.config(height=3)
        stop_button.config(height=3)

        advanced_settings_frame = tk.LabelFrame(left_content_frame, text="Advanced Settings", font=("Arial", 12, "bold"))
        advanced_settings_frame.pack(fill='x', padx=10, pady=(30, 30))

        toggle_frame = tk.Frame(advanced_settings_frame)
        toggle_frame.grid(row=7, column=0, padx=10, pady=10)

        self.relay_checkboxes = {}
        self.trigger_entries = {}

        for i, relay_pair in enumerate(self.settings['relay_pairs']):
            frame = tk.Frame(toggle_frame)
            frame.grid(row=i//4, column=i%4, padx=10, pady=(0, 10), sticky="w")

            relay_pair_tuple = tuple(relay_pair)  # Convert list to tuple

            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(frame, text=f"Enable Relays {relay_pair[0]} & {relay_pair[1]}", variable=var, command=lambda rp=relay_pair_tuple, v=var: self.toggle_relay(rp, v))
            chk.pack(side='top', anchor='w')
            if var.get():
                chk.select()
            self.relay_checkboxes[relay_pair_tuple] = (chk, var)

            label = tk.Label(frame, text="Triggers:")
            label.pack(side='left', pady=(2, 0))
            trigger_entry = tk.Entry(frame, width=5)
            trigger_entry.insert(0, "0")
            trigger_entry.pack(side='left')
            self.trigger_entries[relay_pair_tuple] = trigger_entry

        interval_frame = tk.Frame(advanced_settings_frame)
        interval_frame.grid(row=10, column=0, padx=0, pady=(5, 0))
        tk.Label(interval_frame, text="Interval (seconds):").grid(row=0, column=0, sticky="w")
        self.interval_entry = tk.Entry(interval_frame)
        self.interval_entry.insert(0, self.settings['interval'])
        self.interval_entry.grid(row=0, column=1, sticky="w")

        stagger_frame = tk.Frame(advanced_settings_frame)
        stagger_frame.grid(row=11, column=0, padx=10, pady=(5, 0))
        tk.Label(stagger_frame, text="Stagger (seconds):").grid(row=0, column=0, sticky="w")
        self.stagger_entry = tk.Entry(stagger_frame)
        self.stagger_entry.insert(0, self.settings['stagger'])
        self.stagger_entry.grid(row=0, column=1, sticky="w")

        window_frame = tk.Frame(advanced_settings_frame)
        window_frame.grid(row=12, column=0, padx=10, pady=(5, 0))
        tk.Label(window_frame, text="Water Window Start (24-hour format):").grid(row=0, column=0, sticky="w")
        self.window_start_entry = tk.Entry(window_frame)
        self.window_start_entry.insert(0, self.settings['window_start'])
        self.window_start_entry.grid(row=0, column=1, sticky="w")
        tk.Label(window_frame, text="Water Window End (24-hour format):").grid(row=1, column=0, sticky="w")
        self.window_end_entry = tk.Entry(window_frame)
        self.window_end_entry.insert(0, self.settings['window_end'])
        self.window_end_entry.grid(row=1, column=1, sticky="w")

        update_settings_button = tk.Button(advanced_settings_frame, text="Update Settings", command=self.update_all_settings)
        update_settings_button.grid(row=13, column=0, sticky="w", padx=(230, 5), pady=10)
        update_settings_button.config(height=3)

        # Dynamic path construction for the image file
        image1_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'Lab_logo_white.png')
        image1 = Image.open(image1_path)
        tk_image1 = ImageTk.PhotoImage(image1)

        self.root.tk_image1 = ImageTk.PhotoImage(Image.open(image1_path))

        image_frame = tk.Frame(right_content_frame)
        image_frame.pack(fill='x', padx=(50, 10), pady=1)

        left_image_label = tk.Label(image_frame, image=tk_image1)
        left_image_label.grid(row=0, column=0, padx=(50, 10), pady=(15, 5), sticky="w")

        canvas.configure(scrollregion=canvas.bbox("all"))

    def add_styled_text_single(self, frame, text, scrollbar):
        text_frame = tk.Frame(frame)
        text_frame.pack(fill='x', padx=(25, 25), pady=(1, 1))

        text_widget = tk.Text(text_frame, wrap='word', height=18, font=("Arial", 12),
                              bg=frame.cget("bg"), bd=0, highlightthickness=0)
        text_widget.pack(side='left', fill='x', expand=True)

        text_widget.config(width=120)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.insert("1.0", text)

        text_widget.tag_configure("bold", font=("Arial", 12, "bold"))

        bold_patterns = [
            r"Step \d+:",
            r"Notes:",
            r"EACH",
            r"UP",
            r"\*",
            r"1",
            r"2",
            r"3",
            r"4",
            r"5",
            r":",
            r"\bC\b",
            r"\b+\b",
        ]

        for pattern in bold_patterns:
            start_index = "1.0"
            while True:
                start_index = text_widget.search(pattern, start_index, stopindex=tk.END, regexp=True)
                if not start_index:
                    break
                length_of_match = len(text_widget.get(start_index, f"{start_index} wordend"))
                end_index = f"{start_index} + {length_of_match}c"
                text_widget.tag_add("bold", start_index, end_index)
                start_index = end_index

        text_widget.config(state="disabled")

    def print_to_terminal(self, message):
        self.terminal_output.insert("end", message + "\n")
        self.terminal_output.see("end")

    def toggle_relay(self, relay_pair, var):
        if var.get():
            if relay_pair not in self.selected_relays:
                self.selected_relays.append(relay_pair)
            print(f"Relay pair {relay_pair} enabled")
        else:
            if relay_pair in self.selected_relays:
                self.selected_relays.remove(relay_pair)
            print(f"Relay pair {relay_pair} disabled")

    def suggest_settings(self):
        try:
            frequency = int(self.entries["How often should each cage receive water? \n  (Seconds)"].get())
            window_start = int(self.entries["Water window start (hour, 24-hour format):"].get())
            window_end = int(self.entries["Water window end (hour, 24-hour format):"].get())

            suggestion_text = (
                f"Suggested Settings:\n"
                f"- Interval: {frequency} seconds\n"
                f"- Stagger: {'1'} seconds (Assumed)\n"
                f"- Water Window: {window_start}:00 to {window_end}:00\n"
            )

            for relay_pair in self.settings['relay_pairs']:
                question = f"Water volume for relays {relay_pair[0]} & {relay_pair[1]} (uL):"
                if question in self.entries:
                    volume_per_relay = int(self.entries[question].get())
                    triggers = self.calculate_triggers(volume_per_relay)
                    suggestion_text += f"- Relays {relay_pair[0]} & {relay_pair[1]} should trigger {triggers} times to dispense {volume_per_relay} micro-liters each.\n"

            self.print_to_terminal(suggestion_text)
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numbers for all settings.")

    def calculate_triggers(self, volume_needed):
        return math.ceil(volume_needed / 10)

    def push_settings(self):
        try:
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.insert(0, self.entries["How often should each cage receive water? \n  (Seconds)"].get())

            self.stagger_entry.delete(0, tk.END)
            self.stagger_entry.insert(0, "1")

            self.window_start_entry.delete(0, tk.END)
            self.window_start_entry.insert(0, self.entries["Water window start (hour, 24-hour format):"].get())
            self.window_end_entry.delete(0, tk.END)
            self.window_end_entry.insert(0, self.entries["Water window end (hour, 24-hour format):"].get())

            for relay_pair, (chk, var) in self.relay_checkboxes.items():
                question = f"Water volume for relays {relay_pair[0]} & {relay_pair[1]} (uL):"
                if question in self.entries:
                    volume_per_relay = int(self.entries[question].get())
                    triggers = self.calculate_triggers(volume_per_relay)
                    self.trigger_entries[relay_pair].delete(0, tk.END)
                    self.trigger_entries[relay_pair].insert(0, str(triggers))

                    if volume_per_relay == 0:
                        var.set(False)
                    else:
                        var.set(True)

            self.update_all_settings()
            self.print_to_terminal("Settings have been pushed to the control panel and updated.")
        except Exception as e:
            self.print_to_terminal(f"Error pushing settings: {e}")

    def get_settings(self):
        settings = {
            'interval': int(self.interval_entry.get()),
            'stagger': int(self.stagger_entry.get()),
            'window_start': int(self.window_start_entry.get()),
            'window_end': int(self.window_end_entry.get()),
            'selected_relays': [rp for rp, (chk, var) in self.relay_checkboxes.items() if var.get()],
            'num_triggers': {rp: int(self.trigger_entries[rp].get()) for rp in self.relay_checkboxes if self.trigger_entries[rp].get().isdigit()}
        }
        return settings

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.stop_program()
