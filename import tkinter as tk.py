import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import date

# Constantes de configuración
YEAR_OPTIONS = [2025, 2026]
# Modalidades de turno: (Días_Trabajo, Días_Descanso)
MODALITIES = {'14x14': (14, 14), '7x7': (7, 7), '4x4': (4, 4)}

class ShiftPlanner(tk.Tk):
    """
    Clase principal para la aplicación Planificador de Turnos.
    Permite visualizar un calendario y marcar días de trabajo/descanso 
    según una modalidad de ciclo (ej: 14x14) y un día de inicio de ciclo.
    Hereda de tk.Tk para crear la ventana principal.
    """
    def __init__(self):
        """Inicializa la ventana, las variables de estado y la interfaz."""
        super().__init__()
        self.title('Planificador de Turnos')
        self.resizable(False, False)
        
        # Variables de control
        self.selected_year = tk.IntVar(value=2025)
        self.selected_month = tk.IntVar(value=1)
        self.selected_modality = tk.StringVar(value='14x14')
        self.cycle_start = None  # Almacena el objeto date del inicio del ciclo (día 1 de trabajo)
        self.selected_day = None # Almacena el objeto date del día seleccionado por el usuario
        self.start_time = tk.StringVar(value='08:00')
        self.end_time = tk.StringVar(value='20:00')
        
        self.create_widgets()
        self.draw_calendar()

    def create_widgets(self):
        """Inicializa y posiciona todos los widgets de la interfaz (controles, tiempos, botones y leyenda)."""
        control_frame = ttk.Frame(self, padding=8)
        control_frame.grid(row=0, column=0, sticky='ew')
        
        # (Widgets de Año, Mes y Modalidad)
        # ... [El código para crear los widgets sigue aquí]
        
        # Frame para el calendario que se redibuja
        self.calendar_frame = ttk.Frame(self, padding=8)
        self.calendar_frame.grid(row=4, column=0)

    def prev_month(self):
        """Retrocede al mes anterior. Si es enero, pasa a diciembre del año anterior (si está permitido)."""
        m, y = self.selected_month.get(), self.selected_year.get()
        if m == 1:
            if y > YEAR_OPTIONS[0]:
                self.selected_year.set(y - 1)
                self.selected_month.set(12)
        else:
            self.selected_month.set(m - 1)
        self.draw_calendar()

    def next_month(self):
        """Avanza al mes siguiente. Si es diciembre, pasa a enero del año siguiente (si está permitido)."""
        m, y = self.selected_month.get(), self.selected_year.get()
        if m == 12:
            if y < YEAR_OPTIONS[-1]:
                self.selected_year.set(y + 1)
                self.selected_month.set(1)
        else:
            self.selected_month.set(m + 1)
        self.draw_calendar()

    def draw_calendar(self):
        """
        Dibuja el calendario mensual.
        Limpia el frame anterior y dibuja nuevos botones/etiquetas de días 
        marcándolos con colores de trabajo o descanso.
        """
        # Elimina widgets anteriores
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        year = self.selected_year.get()
        month = self.selected_month.get()
        
        # (Código para dibujar encabezados de mes y días de la semana)
        
        month_days = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
        for r, week in enumerate(month_days, start=2):
            for c, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text=' ', width=4, height=2).grid(row=r, column=c)
                else:
                    d_date = date(year, month, day)
                    color = 'blue' if self.is_work_day(d_date) else 'white'
                    fg = 'white' if color == 'blue' else 'black'
                    tk.Button(self.calendar_frame, text=str(day), width=4, height=2, bg=color, fg=fg,
                              command=lambda d=d_date: self.select_day(d)).grid(row=r, column=c, padx=2, pady=2)

    def current_modality(self):
        """Retorna la tupla (días_trabajo, días_descanso) de la modalidad seleccionada."""
        return MODALITIES[self.selected_modality.get()]

    def is_work_day(self, d):
        """
        Determina si una fecha dada (d) es un día de trabajo.
        Calcula la posición del día dentro del ciclo (trabajo + descanso) usando el operador módulo (%).
        
        Args:
            d (datetime.date): La fecha a evaluar.
            
        Returns:
            bool: True si es día de trabajo, False si es de descanso o si no hay ciclo fijado.
        """
        if not self.cycle_start:
            return False
        work, rest = self.current_modality()
        cycle_length = work + rest
        diff = (d - self.cycle_start).days % cycle_length
        return diff < work # Si la diferencia cae dentro de los días de trabajo (0 a work-1)

    def select_day(self, d):
        """Almacena el día seleccionado por el usuario y muestra una alerta informativa."""
        self.selected_day = d
        messagebox.showinfo('Día seleccionado', f'Día seleccionado: {d.strftime("%d/%m/%Y")}')

    def set_cycle_start(self):
        """Fija el día seleccionado (`self.selected_day`) como el inicio oficial del ciclo de turnos (`self.cycle_start`)."""
        if not self.selected_day:
            messagebox.showwarning('Atención', 'Seleccione un día primero.')
            return
        self.cycle_start = self.selected_day
        messagebox.showinfo('Inicio fijado', f'Inicio de ciclo: {self.cycle_start.strftime("%d/%m/%Y")}')
        self.draw_calendar()

    def clear_cycle_start(self):
        """Borra la configuración del día de inicio de ciclo (`self.cycle_start = None`)."""
        self.cycle_start = None
        messagebox.showinfo('Borrado', 'Inicio de ciclo eliminado.')
        self.draw_calendar()

if __name__ == '__main__':
    app = ShiftPlanner()
    app.mainloop()