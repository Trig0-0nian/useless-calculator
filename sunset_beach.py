import tkinter as tk
from tkinter import ttk, messagebox
import math
import re
import random
from datetime import datetime

class UltraCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Useless Calculator Pro Max Ultra")
        self.root.geometry("480x750")
        self.root.resizable(False, False)
        
        # Variables
        self.expression = ""
        self.result_var = tk.StringVar(value="0")
        self.history = []
        self.memory = 0
        self.is_scientific = False
        self.is_degree = True
        self.current_theme = "dark"
        self.current_mode = "calculator"  # calculator, converter, game
        self.game_score = 0
        self.game_question = None
        self.game_answer = None
        
        # Themes
        self.themes = {
            'dark': {
                'bg': '#0a0e27',
                'display_bg': '#151b2e',
                'text': '#ffffff',
                'subtext': '#5a6a8a',
                'accent': '#00d9ff',
                'button_bg': '#1e2838',
                'button_hover': '#2a3648',
                'operator_bg': '#2a4a6f',
                'operator_hover': '#3a5a8f',
                'function_bg': '#4a148c',
                'function_hover': '#6a1b9a',
                'equals_bg': '#00d9ff',
                'equals_fg': '#0a0e27',
                'clear_bg': '#d32f2f',
                'special_bg': '#37474f'
            },
            'light': {
                'bg': '#f5f7fa',
                'display_bg': '#ffffff',
                'text': '#1a202c',
                'subtext': '#718096',
                'accent': '#3182ce',
                'button_bg': '#e2e8f0',
                'button_hover': '#cbd5e0',
                'operator_bg': '#4299e1',
                'operator_hover': '#3182ce',
                'function_bg': '#9f7aea',
                'function_hover': '#805ad5',
                'equals_bg': '#48bb78',
                'equals_fg': '#ffffff',
                'clear_bg': '#f56565',
                'special_bg': '#718096'
            },
            'neon': {
                'bg': '#000000',
                'display_bg': '#0d0d0d',
                'text': '#00ff00',
                'subtext': '#00aa00',
                'accent': '#ff00ff',
                'button_bg': '#1a1a1a',
                'button_hover': '#2a2a2a',
                'operator_bg': '#330033',
                'operator_hover': '#550055',
                'function_bg': '#003300',
                'function_hover': '#005500',
                'equals_bg': '#ff00ff',
                'equals_fg': '#000000',
                'clear_bg': '#ff0000',
                'special_bg': '#333333'
            }
        }
        
        self.apply_theme()
        self.create_widgets()
        self.root.bind('<Key>', self.key_press)
        
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme['bg'])
        
    def create_widgets(self):
        # ============ TOP NAVIGATION BAR ============
        nav_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]['bg'], height=60)
        nav_frame.pack(fill='x', padx=15, pady=(15, 0))
        
        # App title with emoji
        title_label = tk.Label(nav_frame, text="🧮 USELESS CALCULATOR", 
                              font=('Segoe UI', 13, 'bold'),
                              bg=self.themes[self.current_theme]['bg'], 
                              fg=self.themes[self.current_theme]['accent'])
        title_label.pack(side='left')
        
        # Navigation buttons container
        nav_buttons = tk.Frame(nav_frame, bg=self.themes[self.current_theme]['bg'])
        nav_buttons.pack(side='right')
        
        # Theme button
        self.theme_btn = tk.Button(nav_buttons, text="🌙", 
                                   font=('Segoe UI', 14),
                                   bg=self.themes[self.current_theme]['special_bg'],
                                   fg=self.themes[self.current_theme]['text'],
                                   command=self.cycle_theme,
                                   relief='flat', cursor='hand2',
                                   bd=0, padx=10, pady=5)
        self.theme_btn.pack(side='left', padx=2)
        
        # Mode buttons
        modes = [
            ('🧮', 'calculator', 'Calculator'),
            ('🔄', 'converter', 'Converter'),
            ('🎮', 'game', 'Math Game')
        ]
        
        self.mode_buttons = {}
        for icon, mode, tooltip in modes:
            btn = tk.Button(nav_buttons, text=icon, 
                          font=('Segoe UI', 14),
                          bg=self.themes[self.current_theme]['special_bg'],
                          fg=self.themes[self.current_theme]['text'],
                          command=lambda m=mode: self.switch_mode(m),
                          relief='flat', cursor='hand2',
                          bd=0, padx=10, pady=5)
            btn.pack(side='left', padx=2)
            self.mode_buttons[mode] = btn
            
        # ============ STATUS BAR ============
        status_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]['bg'], height=35)
        status_frame.pack(fill='x', padx=15, pady=(8, 0))
        
        # Time display
        self.time_label = tk.Label(status_frame, text=datetime.now().strftime("%H:%M"),
                                   font=('Segoe UI', 9),
                                   bg=self.themes[self.current_theme]['bg'],
                                   fg=self.themes[self.current_theme]['subtext'])
        self.time_label.pack(side='left', padx=(0, 8))
        self.update_time()
        
        # Memory indicator
        self.memory_label = tk.Label(status_frame, text="M", 
                                     font=('Segoe UI', 9),
                                     bg=self.themes[self.current_theme]['special_bg'],
                                     fg='#666',
                                     padx=8, pady=3, relief='flat')
        self.memory_label.pack(side='left', padx=(0, 8))
        
        # DEG/RAD toggle
        self.deg_rad_btn = tk.Button(status_frame, text="DEG", 
                                    font=('Segoe UI', 9, 'bold'),
                                    bg=self.themes[self.current_theme]['accent'],
                                    fg=self.themes[self.current_theme]['bg'],
                                    command=self.toggle_deg_rad,
                                    relief='flat', cursor='hand2',
                                    bd=0, padx=10, pady=3)
        self.deg_rad_btn.pack(side='left')
        
        # Scientific mode toggle
        self.sci_btn = tk.Button(status_frame, text="⚙ SCI", 
                                font=('Segoe UI', 9, 'bold'),
                                bg=self.themes[self.current_theme]['special_bg'],
                                fg=self.themes[self.current_theme]['accent'],
                                command=self.toggle_scientific,
                                relief='flat', cursor='hand2',
                                bd=0, padx=10, pady=3)
        self.sci_btn.pack(side='right')
        
        # ============ DISPLAY AREA ============
        self.display_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]['display_bg'])
        self.display_frame.pack(fill='x', padx=15, pady=(15, 0))
        
        inner_display = tk.Frame(self.display_frame, bg=self.themes[self.current_theme]['display_bg'])
        inner_display.pack(fill='both', padx=15, pady=15)
        
        # Expression label
        self.expr_label = tk.Label(inner_display, text="", 
                                   font=('Segoe UI', 11), 
                                   bg=self.themes[self.current_theme]['display_bg'],
                                   fg=self.themes[self.current_theme]['subtext'],
                                   anchor='e', height=1)
        self.expr_label.pack(fill='x')
        
        # Result label
        self.result_label = tk.Label(inner_display, textvariable=self.result_var,
                                     font=('Segoe UI', 42, 'bold'),
                                     bg=self.themes[self.current_theme]['display_bg'],
                                     fg=self.themes[self.current_theme]['text'],
                                     anchor='e', height=1)
        self.result_label.pack(fill='x', pady=(5, 0))
        
        # ============ CONTENT AREA (Switchable) ============
        self.content_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]['bg'])
        self.content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create calculator interface
        self.create_calculator_interface()
        
    def create_calculator_interface(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.buttons_frame = tk.Frame(self.content_frame, bg=self.themes[self.current_theme]['bg'])
        self.buttons_frame.pack(fill='both', expand=True)
        
        if not self.is_scientific:
            buttons = [
                ['C', '⌫', '%', '÷'],
                ['7', '8', '9', '×'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['MC', '0', '.', '=']
            ]
        else:
            buttons = [
                ['C', '⌫', 'MC', 'MR', 'M+', 'M-'],
                ['sin', 'cos', 'tan', '(', ')', '÷'],
                ['asin', 'acos', 'atan', '7', '8', '9'],
                ['x²', '√', 'x^y', '4', '5', '6'],
                ['log', 'ln', 'n!', '1', '2', '3'],
                ['π', 'e', '1/x', '0', '.', '×'],
                ['abs', 'mod', '%', '+', '-', '=']
            ]
        
        theme = self.themes[self.current_theme]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                # Determine style
                if btn_text == 'C':
                    bg, fg, hover = theme['clear_bg'], '#ffffff', '#e53935'
                elif btn_text == '⌫':
                    bg, fg, hover = theme['special_bg'], '#ffffff', '#546e7a'
                elif btn_text == '=':
                    bg, fg, hover = theme['equals_bg'], theme['equals_fg'], theme['accent']
                elif btn_text in ['÷', '×', '-', '+']:
                    bg, fg, hover = theme['operator_bg'], theme['accent'], theme['operator_hover']
                elif btn_text in ['%', 'MC', 'MR', 'M+', 'M-', 'mod']:
                    bg, fg, hover = theme['special_bg'], theme['accent'], '#546e7a'
                elif btn_text in ['0','1','2','3','4','5','6','7','8','9','.','(',')']:
                    bg, fg, hover = theme['button_bg'], theme['text'], theme['button_hover']
                else:
                    bg, fg, hover = theme['function_bg'], theme['accent'], theme['function_hover']
                
                font_size = 18 if not self.is_scientific else 11
                btn = tk.Button(self.buttons_frame, text=btn_text,
                               font=('Segoe UI', font_size, 'bold'),
                               bg=bg, fg=fg,
                               activebackground=hover,
                               activeforeground=fg,
                               relief='flat', cursor='hand2', bd=0,
                               command=lambda x=btn_text: self.button_click(x))
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
                
                # Hover effects
                btn.bind('<Enter>', lambda e, b=btn, c=hover: b.config(bg=c))
                btn.bind('<Leave>', lambda e, b=btn, c=bg: b.config(bg=c))
        
        # Configure grid
        for i in range(len(buttons)):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(buttons[0])):
            self.buttons_frame.grid_columnconfigure(j, weight=1)
    
    def create_converter_interface(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        theme = self.themes[self.current_theme]
        
        conv_frame = tk.Frame(self.content_frame, bg=theme['bg'])
        conv_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(conv_frame, text="🔄 Unit Converter", 
                font=('Segoe UI', 16, 'bold'),
                bg=theme['bg'], fg=theme['accent']).pack(pady=10)
        
        # Conversion type
        tk.Label(conv_frame, text="Select Conversion:", 
                font=('Segoe UI', 10),
                bg=theme['bg'], fg=theme['text']).pack(pady=5)
        
        self.conv_type = tk.StringVar(value="length")
        conv_types = [
            ("📏 Length", "length"),
            ("⚖️ Weight", "weight"),
            ("🌡️ Temperature", "temperature"),
            ("💾 Data", "data")
        ]
        
        type_frame = tk.Frame(conv_frame, bg=theme['bg'])
        type_frame.pack(pady=10)
        
        for text, value in conv_types:
            tk.Radiobutton(type_frame, text=text, variable=self.conv_type,
                          value=value, bg=theme['bg'], fg=theme['text'],
                          selectcolor=theme['button_bg'],
                          activebackground=theme['bg'],
                          activeforeground=theme['accent'],
                          font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        # Input
        input_frame = tk.Frame(conv_frame, bg=theme['display_bg'])
        input_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(input_frame, text="From:", 
                font=('Segoe UI', 10),
                bg=theme['display_bg'], fg=theme['text']).pack(pady=5)
        
        self.conv_input = tk.Entry(input_frame, font=('Segoe UI', 14),
                                   bg=theme['button_bg'], fg=theme['text'],
                                   justify='center', bd=0)
        self.conv_input.pack(fill='x', padx=20, pady=5, ipady=8)
        
        self.from_unit = ttk.Combobox(input_frame, values=['meter', 'kilometer', 'mile', 'foot'],
                                      font=('Segoe UI', 10), state='readonly')
        self.from_unit.set('meter')
        self.from_unit.pack(pady=5)
        
        # Arrow
        tk.Label(conv_frame, text="⬇️", font=('Segoe UI', 20),
                bg=theme['bg'], fg=theme['accent']).pack(pady=5)
        
        # Output
        output_frame = tk.Frame(conv_frame, bg=theme['display_bg'])
        output_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(output_frame, text="To:", 
                font=('Segoe UI', 10),
                bg=theme['display_bg'], fg=theme['text']).pack(pady=5)
        
        self.conv_output = tk.Label(output_frame, text="0", 
                                    font=('Segoe UI', 18, 'bold'),
                                    bg=theme['button_bg'], fg=theme['accent'])
        self.conv_output.pack(fill='x', padx=20, pady=10, ipady=8)
        
        self.to_unit = ttk.Combobox(output_frame, values=['meter', 'kilometer', 'mile', 'foot'],
                                    font=('Segoe UI', 10), state='readonly')
        self.to_unit.set('kilometer')
        self.to_unit.pack(pady=5)
        
        # Convert button
        tk.Button(conv_frame, text="Convert", font=('Segoe UI', 12, 'bold'),
                 bg=theme['equals_bg'], fg=theme['equals_fg'],
                 command=self.convert_units,
                 relief='flat', cursor='hand2',
                 bd=0, padx=30, pady=10).pack(pady=15)
    
    def create_game_interface(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        theme = self.themes[self.current_theme]
        
        game_frame = tk.Frame(self.content_frame, bg=theme['bg'])
        game_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(game_frame, text="🎮 Math Challenge", 
                font=('Segoe UI', 18, 'bold'),
                bg=theme['bg'], fg=theme['accent']).pack(pady=10)
        
        # Score
        self.score_label = tk.Label(game_frame, text=f"Score: {self.game_score}", 
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=theme['bg'], fg=theme['text'])
        self.score_label.pack(pady=5)
        
        # Question display
        self.question_frame = tk.Frame(game_frame, bg=theme['display_bg'])
        self.question_frame.pack(fill='x', pady=20, padx=30)
        
        self.question_label = tk.Label(self.question_frame, text="Press Start!", 
                                       font=('Segoe UI', 24, 'bold'),
                                       bg=theme['display_bg'], fg=theme['text'],
                                       height=3)
        self.question_label.pack(fill='both', padx=20, pady=20)
        
        # Answer input
        self.answer_entry = tk.Entry(game_frame, font=('Segoe UI', 18),
                                     bg=theme['button_bg'], fg=theme['text'],
                                     justify='center', bd=0)
        self.answer_entry.pack(pady=10, padx=50, ipady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        # Buttons
        button_frame = tk.Frame(game_frame, bg=theme['bg'])
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🎯 Check Answer", 
                 font=('Segoe UI', 11, 'bold'),
                 bg=theme['equals_bg'], fg=theme['equals_fg'],
                 command=self.check_answer,
                 relief='flat', cursor='hand2',
                 bd=0, padx=20, pady=8).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="▶️ New Question", 
                 font=('Segoe UI', 11, 'bold'),
                 bg=theme['operator_bg'], fg=theme['accent'],
                 command=self.generate_question,
                 relief='flat', cursor='hand2',
                 bd=0, padx=20, pady=8).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="🔄 Reset Score", 
                 font=('Segoe UI', 11, 'bold'),
                 bg=theme['clear_bg'], fg='#ffffff',
                 command=self.reset_game,
                 relief='flat', cursor='hand2',
                 bd=0, padx=20, pady=8).pack(side='left', padx=5)
        
        # Feedback label
        self.feedback_label = tk.Label(game_frame, text="", 
                                       font=('Segoe UI', 12, 'bold'),
                                       bg=theme['bg'])
        self.feedback_label.pack(pady=10)
    
    def generate_question(self):
        operators = ['+', '-', '×', '÷']
        op = random.choice(operators)
        
        if op == '+':
            a, b = random.randint(10, 100), random.randint(10, 100)
            self.game_question = f"{a} + {b}"
            self.game_answer = a + b
        elif op == '-':
            a, b = random.randint(50, 100), random.randint(10, 49)
            self.game_question = f"{a} - {b}"
            self.game_answer = a - b
        elif op == '×':
            a, b = random.randint(2, 15), random.randint(2, 15)
            self.game_question = f"{a} × {b}"
            self.game_answer = a * b
        else:  # ÷
            b = random.randint(2, 12)
            self.game_answer = random.randint(2, 20)
            a = b * self.game_answer
            self.game_question = f"{a} ÷ {b}"
        
        self.question_label.config(text=self.game_question)
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
    
    def check_answer(self):
        try:
            user_answer = float(self.answer_entry.get())
            if abs(user_answer - self.game_answer) < 0.01:
                self.game_score += 10
                self.feedback_label.config(text="✅ Correct! +10 points", 
                                          fg='#48bb78')
                self.score_label.config(text=f"Score: {self.game_score}")
                self.root.after(1000, self.generate_question)
            else:
                self.game_score = max(0, self.game_score - 5)
                self.feedback_label.config(text=f"❌ Wrong! Answer: {self.game_answer}", 
                                          fg='#f56565')
                self.score_label.config(text=f"Score: {self.game_score}")
        except:
            self.feedback_label.config(text="Please enter a valid number!", 
                                      fg='#ed8936')
    
    def reset_game(self):
        self.game_score = 0
        self.score_label.config(text=f"Score: {self.game_score}")
        self.question_label.config(text="Press 'New Question' to start!")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
    
    def convert_units(self):
        try:
            value = float(self.conv_input.get())
            from_u = self.from_unit.get()
            to_u = self.to_unit.get()
            conv_type = self.conv_type.get()
            
            # Length conversions
            if conv_type == "length":
                conversions = {
                    'meter': 1,
                    'kilometer': 0.001,
                    'mile': 0.000621371,
                    'foot': 3.28084
                }
            # Add more conversion types...
            
            if from_u in conversions and to_u in conversions:
                meters = value / conversions[from_u]
                result = meters * conversions[to_u]
                self.conv_output.config(text=f"{result:.4f}")
        except:
            self.conv_output.config(text="Error")
    
    def switch_mode(self, mode):
        self.current_mode = mode
        theme = self.themes[self.current_theme]
        
        # Reset all button colors
        for m, btn in self.mode_buttons.items():
            btn.config(bg=theme['special_bg'])
        
        # Highlight selected
        self.mode_buttons[mode].config(bg=theme['accent'])
        
        if mode == "calculator":
            self.create_calculator_interface()
        elif mode == "converter":
            self.create_converter_interface()
        elif mode == "game":
            self.create_game_interface()
    
    def cycle_theme(self):
        themes = list(self.themes.keys())
        current_index = themes.index(self.current_theme)
        self.current_theme = themes[(current_index + 1) % len(themes)]
        
        # Update theme button emoji
        theme_emojis = {'dark': '🌙', 'light': '☀️', 'neon': '⚡'}
        self.theme_btn.config(text=theme_emojis[self.current_theme])
        
        # Recreate UI with new theme
        self.apply_theme()
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.switch_mode(self.current_mode)
    
    def toggle_scientific(self):
        self.is_scientific = not self.is_scientific
        if self.is_scientific:
            self.root.geometry("480x870")
            self.sci_btn.config(text="⚙ STD")
        else:
            self.root.geometry("480x750")
            self.sci_btn.config(text="⚙ SCI")
        
        if self.current_mode == "calculator":
            self.create_calculator_interface()
    
    def toggle_deg_rad(self):
        self.is_degree = not self.is_degree
        theme = self.themes[self.current_theme]
        if self.is_degree:
            self.deg_rad_btn.config(text="DEG", bg=theme['accent'], fg=theme['bg'])
        else:
            self.deg_rad_btn.config(text="RAD", bg='#ff6b35', fg='#ffffff')
    
    def update_time(self):
        self.time_label.config(text=datetime.now().strftime("%H:%M"))
        self.root.after(60000, self.update_time)
    
    def button_click(self, value):
        try:
            if value == 'C':
                self.clear()
            elif value == '⌫':
                self.backspace()
            elif value == '=':
                self.calculate()
            elif value == 'MC':
                self.memory = 0
                self.memory_label.config(fg='#666')
            elif value == 'MR':
                self.expression += str(self.memory)
                self.update_display()
            elif value == 'M+':
                try:
                    current = float(self.result_var.get())
                    self.memory += current
                    self.memory_label.config(fg=self.themes[self.current_theme]['accent'])
                except:
                    pass
            elif value == 'M-':
                try:
                    current = float(self.result_var.get())
                    self.memory -= current
                    self.memory_label.config(fg=self.themes[self.current_theme]['accent'])
                except:
                    pass
            elif value == '√':
                self.expression += 'sqrt('
                self.update_display()
            elif value == 'x²':
                self.expression += '**2'
                self.update_display()
            elif value == 'x^y':
                self.expression += '**'
                self.update_display()
            elif value == 'π':
                self.expression += str(math.pi)
                self.update_display()
            elif value == 'e':
                self.expression += str(math.e)
                self.update_display()
            elif value == '1/x':
                self.expression = f'1/({self.expression})'
                self.update_display()
            elif value in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln', 'abs']:
                func_map = {'ln': 'log', 'log': 'log10'}
                func_name = func_map.get(value, value)
                self.expression += f'{func_name}('
                self.update_display()
            elif value == 'n!':
                self.expression += 'factorial('
                self.update_display()
            elif value == 'mod':
                self.expression += '%'
                self.update_display()
            elif value == '÷':
                self.expression += '/'
                self.update_display()
            elif value == '×':
                self.expression += '*'
                self.update_display()
            elif value == '%':
                self.expression += '/100'
                self.update_display()
            else:
                self.expression += value
                self.update_display()
        except Exception as e:
            self.show_error(str(e))
    
    def calculate(self):
        try:
            expr = self.expression
            open_count = expr.count('(')
            close_count = expr.count(')')
            if open_count > close_count:
                expr += ')' * (open_count - close_count)
                self.expression = expr
            
            if self.is_degree:
                expr = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expr)
                expr = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expr)
                expr = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expr)
                expr = re.sub(r'asin\(([^)]+)\)', r'math.degrees(math.asin(\1))', expr)
                expr = re.sub(r'acos\(([^)]+)\)', r'math.degrees(math.acos(\1))', expr)
                expr = re.sub(r'atan\(([^)]+)\)', r'math.degrees(math.atan(\1))', expr)
            else:
                expr = expr.replace('sin', 'math.sin')
                expr = expr.replace('cos', 'math.cos')
                expr = expr.replace('tan', 'math.tan')
                expr = expr.replace('asin', 'math.asin')
                expr = expr.replace('acos', 'math.acos')
                expr = expr.replace('atan', 'math.atan')
            
            expr = expr.replace('sqrt', 'math.sqrt')
            expr = expr.replace('log10', 'math.log10')
            expr = expr.replace('log', 'math.log')
            expr = expr.replace('factorial', 'math.factorial')
            
            result = eval(expr)
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.history.append(f"{self.expression} = {result}")
            self.expr_label.config(text=self.expression)
            self.result_var.set(str(result))
            self.expression = str(result)
            
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
        except Exception as e:
            self.show_error("Invalid expression")
    
    def show_error(self, message):
        self.result_var.set("Error")
        self.result_label.config(fg='#ff6b6b')
        self.root.after(1500, lambda: self.result_label.config(fg=self.themes[self.current_theme]['text']))
        self.root.after(1500, self.clear)
    
    def clear(self):
        self.expression = ""
        self.result_var.set("0")
        self.expr_label.config(text="")
    
    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display()
    
    def update_display(self):
        display_text = self.expression if self.expression else "0"
        self.result_var.set(display_text)
    
    def key_press(self, event):
        if self.current_mode != "calculator":
            return
        key = event.char
        if key.isdigit() or key in ['+', '-', '*', '/', '.', '(', ')']:
            self.button_click(key if key != '*' else '×')
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.clear()

# ============ MAIN ============
if __name__ == "__main__":
    root = tk.Tk()
    calculator = UltraCalculator(root)
    
    # Menu
    menubar = tk.Menu(root, bg='#1a2332', fg='white')
    root.config(menu=menubar)
    
    history_menu = tk.Menu(menubar, tearoff=0, bg='#1a2332', fg='white')
    menubar.add_cascade(label="📜 History", menu=history_menu)
    history_menu.add_command(label="View History", 
                            command=lambda: messagebox.showinfo("History", 
                            "\n".join(calculator.history[-10:]) if calculator.history else "No history"))
    history_menu.add_command(label="Clear History", 
                            command=lambda: calculator.history.clear())
    
    help_menu = tk.Menu(menubar, tearoff=0, bg='#1a2332', fg='white')
    menubar.add_cascade(label="❓ Help", menu=help_menu)
    help_menu.add_command(label="About", 
                         command=lambda: messagebox.showinfo("Useless Calculator Pro Max Ultra", 
                         "🧮 Useless Calculator Pro Max Ultra v3.0\n\n✨ Features:\n• 3 Themes (Dark/Light/Neon)\n• Scientific Calculator\n• Unit Converter\n• Math Challenge Game\n• Real-time Clock\n• Memory Functions\n• Keyboard Support\n• Auto-close Parentheses\n\n🎮 Absolutely useless but fun!\n\nMade with Python & Tkinter"))
    
    root.mainloop()
