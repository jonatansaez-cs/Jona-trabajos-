import tkinter as tk
from math import sqrt

def click(b):
    actual = entry.get()
    if b == "=":
        try:
            resultado = eval(actual)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(resultado))
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif b == "C":
        entry.delete(0, tk.END)
    elif b == "√":
        try:
            valor = float(actual)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(sqrt(valor)))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif b == "x²":
        try:
            valor = float(actual)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(valor**2))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    else:
        entry.insert(tk.END, b)

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("300x400")
ventana.resizable(False, False)

entry = tk.Entry(ventana, font=("Arial", 20), justify="right", bd=8, relief="sunken")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

botones = [
    ("7",1,0),("8",1,1),("9",1,2),("/",1,3),
    ("4",2,0),("5",2,1),("6",2,2),("*",2,3),
    ("1",3,0),("2",3,1),("3",3,2),("-",3,3),
    ("0",4,0),(".",4,1),("=",4,2),("+",4,3),
    ("C",5,0),("√",5,1),("x²",5,2)
]

for (text, row, col) in botones:
    tk.Button(ventana, text=text, width=5, height=2, font=("Arial", 14),
              command=lambda b=text: click(b)).grid(row=row, column=col, padx=5, pady=5)

ventana.mainloop()
