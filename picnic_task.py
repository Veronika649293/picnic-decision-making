import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PicnicApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Вихідні дані для прийняття рішення в "Задачі про пікнік"')
        self.root.geometry('950x550')
        self.root.configure(bg='#f0f4f8')

        style = ttk.Style()
        style.theme_use('clam')
        
        # Загальні кольори
        bg_color = '#f0f4f8'
        card_bg = '#ffffff'
        
        style.configure('.', background=bg_color, font=('Segoe UI', 10))
        style.configure('Card.TFrame', background=card_bg, relief='solid', borderwidth=1)
        style.configure('TLabel', background=card_bg, font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#1a252f')
        style.configure('Result.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#27ae60')

        main_container = ttk.Frame(root, padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ліва панель 
        left_card = ttk.Frame(main_container, style='Card.TFrame', padding=15)
        left_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        ttk.Label(left_card, text="Імовірність дощу", style='Title.TLabel').grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.rain_prob_var = tk.DoubleVar(value=0.64)
        self.rain_label = ttk.Label(left_card, text="0.64", font=('Segoe UI', 11, 'bold'), foreground='#e74c3c')
        self.rain_label.grid(row=0, column=1, sticky='e', pady=(0, 5))

        self.slider = ttk.Scale(
            left_card, 
            from_=0.0, 
            to=1.0, 
            value=0.64, 
            variable=self.rain_prob_var, 
            command=self.update_all
        )
        self.slider.grid(row=1, column=0, columnspan=2, sticky='we', pady=(0, 15))

        ttk.Separator(left_card, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='we', pady=5)

        ttk.Label(left_card, text="Результат", style='Title.TLabel').grid(row=3, column=0, sticky='w', pady=(10, 5))
        ttk.Label(left_card, text="Корисність", style='Title.TLabel').grid(row=3, column=1, sticky='e', pady=(10, 5))

        self.utility_vars = {
            'вкрай погано': tk.DoubleVar(value=0),
            'погано': tk.DoubleVar(value=2),
            'посередньо': tk.DoubleVar(value=5),
            'чудово': tk.DoubleVar(value=8)
        }

        row_idx = 4
        for outcome, var in self.utility_vars.items():
            ttk.Label(left_card, text=outcome, foreground='#555555').grid(row=row_idx, column=0, sticky='w', pady=3)
            
            entry = tk.Entry(
                left_card, 
                textvariable=var, 
                width=6, 
                font=('Segoe UI', 10), 
                justify='center',
                bd=1,
                relief='solid'
            )
            entry.grid(row=row_idx, column=1, sticky='e', pady=3)
            entry.bind("<KeyRelease>", lambda e: self.update_all())
            row_idx += 1

        
        ttk.Separator(left_card, orient='horizontal').grid(row=row_idx, column=0, columnspan=2, sticky='we', pady=10)
        row_idx += 1

        ttk.Label(left_card, text="Очікувана корисність", style='Title.TLabel').grid(row=row_idx, column=0, columnspan=2, sticky='w', pady=(5, 5))
        row_idx += 1

        ttk.Label(left_card, text="ліс", foreground='#555555').grid(row=row_idx, column=0, sticky='w', padx=(10, 0), pady=2)
        self.u_forest_label = ttk.Label(left_card, text="0.00", font=('Segoe UI', 10, 'bold'))
        self.u_forest_label.grid(row=row_idx, column=1, sticky='e', pady=2)
        row_idx += 1

        ttk.Label(left_card, text="дім", foreground='#555555').grid(row=row_idx, column=0, sticky='w', padx=(10, 0), pady=2)
        self.u_home_label = ttk.Label(left_card, text="0.00", font=('Segoe UI', 10, 'bold'))
        self.u_home_label.grid(row=row_idx, column=1, sticky='e', pady=2)
        row_idx += 1
        
        decision_box = tk.Frame(left_card, bg='#e8f8f5', bd=1, relief='solid', highlightbackground='#27ae60')
        decision_box.grid(row=row_idx, column=0, columnspan=2, sticky='we', pady=(15, 0), ipadx=5, ipady=8)

        ttk.Label(decision_box, text="Рішення:", font=('Segoe UI', 9, 'bold'), background='#e8f8f5', foreground='#16a085').pack(anchor='w', padx=5)
        self.decision_label = ttk.Label(decision_box, text="", font=('Segoe UI', 10, 'bold'), background='#e8f8f5', foreground='#27ae60')
        self.decision_label.pack(anchor='w', padx=5)

        # права панель
        right_card = ttk.Frame(main_container, style='Card.TFrame', padding=15)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_card, text="Рішення про пікнік", style='Header.TLabel').pack(anchor='center', pady=(0, 10))

        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        self.fig, self.ax = plt.subplots(figsize=(6, 4.5), dpi=100)
        self.fig.patch.set_facecolor('#ffffff')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_card)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_all()

    def get_utilities(self):
        try:
            return {
                'вкрай погано': float(self.utility_vars['вкрай погано'].get()),
                'погано': float(self.utility_vars['погано'].get()),
                'посередньо': float(self.utility_vars['посередньо'].get()),
                'чудово': float(self.utility_vars['чудово'].get()),
            }
        except ValueError:
            return {'вкрай погано': 0, 'погано': 2, 'посередньо': 5, 'чудово': 8}

    def update_all(self, *args):
        p_rain = round(self.rain_prob_var.get(), 2)
        self.rain_label.config(text=f"{p_rain:.2f}")

        u = self.get_utilities()

        u_home = p_rain * u['погано'] + (1 - p_rain) * u['посередньо']
        u_forest = p_rain * u['вкрай погано'] + (1 - p_rain) * u['чудово']

        self.u_home_label.config(text=f"{u_home:.2f}")
        self.u_forest_label.config(text=f"{u_forest:.2f}")

        if u_forest > u_home:
            decision_text = "Їдемо в ліс! :)"
        elif u_home > u_forest:
            decision_text = "Сидимо вдома! :("
        else:
            decision_text = "Рішення байдуже :|"

        self.decision_label.config(text=decision_text)

        self.plot_graph(u, p_rain, u_forest, u_home)

    def plot_graph(self, u, current_p, u_forest, u_home):
        self.ax.clear()

        p_values = np.linspace(0, 1, 100)
        u_forest_line = p_values * u['вкрай погано'] + (1 - p_values) * u['чудово']
        u_home_line = p_values * u['погано'] + (1 - p_values) * u['посередньо']

        self.ax.plot(p_values, u_forest_line, label='ліс', color="#77e3cf", linewidth=2.5)
        self.ax.plot(p_values, u_home_line, label='дім', color="#b41f24", linewidth=2.5)

        self.ax.axvline(x=current_p, color='#7f7f7f', linestyle='--', alpha=0.7, linewidth=1.5)

        self.ax.scatter([current_p], [u_forest], color='#77e3cf', s=40, zorder=5)
        self.ax.scatter([current_p], [u_home], color="#b41f24", s=40, zorder=5)

        self.ax.set_xlabel("імовірність дощу", fontsize=10, color='#333333', labelpad=8)
        self.ax.set_ylabel("корисність", fontsize=10, color='#333333', labelpad=8)
        self.ax.set_xlim(0, 1)
        self.ax.set_xticks(np.arange(0, 1.1, 0.1))
        
        self.ax.grid(True, linestyle=':', alpha=0.6, color='#cccccc')
        
        self.ax.legend(
            loc='upper left', 
            bbox_to_anchor=(1.02, 1), 
            borderaxespad=0, 
            frameon=True, 
            facecolor='#ffffff', 
            edgecolor='#cccccc',
            fontsize=10
        )

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = PicnicApp(root)
    root.mainloop()