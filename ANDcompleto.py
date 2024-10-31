# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:33:56 2024

@author: Departamento
"""

import tkinter as tk
from tkinter import messagebox

# Función para mostrar el árbol de decisión gráfico
def mostrar_arbol_grafico():
    # Crear una nueva ventana para el árbol de decisión gráfico
    ventana_arbol_grafico = tk.Toplevel()
    ventana_arbol_grafico.title("Árbol de Decisión Gráfico")
    ventana_arbol_grafico.geometry("400x400")
    
    # Crear un canvas para dibujar el árbol de decisión
    canvas = tk.Canvas(ventana_arbol_grafico, width=400, height=400)
    canvas.pack()

    # Coordenadas y valores de los nodos
    nodos = {
        "A": (200, 50),
        "B_Si": (100, 150),
        "B_No": (300, 150),
        "C_Si_Si": (50, 250),
        "C_Si_No": (150, 250),
        "Resultado_Si_Si_Si": (50, 350, "Verdadero"),
        "Resultado_Si_Si_No": (150, 350, "Falso"),
        "Resultado_Si_No": (100, 250, "Falso"),
        "Resultado_No": (300, 250, "Falso")
    }
    
    # Dibujar conexiones entre nodos
    canvas.create_line(nodos["A"], nodos["B_Si"], fill="black", arrow=tk.LAST)
    canvas.create_line(nodos["A"], nodos["B_No"], fill="black", arrow=tk.LAST)
    canvas.create_line(nodos["B_Si"], nodos["C_Si_Si"], fill="black", arrow=tk.LAST)
    canvas.create_line(nodos["B_Si"], nodos["C_Si_No"], fill="black", arrow=tk.LAST)
    canvas.create_line(nodos["C_Si_Si"], nodos["Resultado_Si_Si_Si"][:2], fill="black", arrow=tk.LAST)
    canvas.create_line(nodos["C_Si_No"], nodos["Resultado_Si_Si_No"][:2], fill="black", arrow=tk.LAST)
    canvas.create_line(nodos["B_No"], nodos["Resultado_No"][:2], fill="black", arrow=tk.LAST)

    # Dibujar nodos y etiquetas
    canvas.create_text(nodos["A"], text="A")
    canvas.create_text(nodos["B_Si"], text="B (Sí)")
    canvas.create_text(nodos["B_No"], text="B (No)")
    canvas.create_text(nodos["C_Si_Si"], text="C (Sí)")
    canvas.create_text(nodos["C_Si_No"], text="C (No)")
    canvas.create_text(nodos["Resultado_Si_Si_Si"][:2], text=f"Resultado: {nodos['Resultado_Si_Si_Si'][2]}")
    canvas.create_text(nodos["Resultado_Si_Si_No"][:2], text=f"Resultado: {nodos['Resultado_Si_Si_No'][2]}")
    canvas.create_text(nodos["Resultado_Si_No"][:2], text=f"Resultado: {nodos['Resultado_Si_No'][2]}")
    canvas.create_text(nodos["Resultado_No"][:2], text=f"Resultado: {nodos['Resultado_No'][2]}")

# Función para mostrar todas las combinaciones de A, B y C con AND
def mostrar_arbol():
    # Crear una lista para almacenar las combinaciones y resultados
    combinaciones = []
    
    # Generar todas las combinaciones posibles de A, B, y C
    for a in [True, False]:
        for b in [True, False]:
            for c in [True, False]:
                resultado = a and b and c
                combinaciones.append((a, b, c, resultado))
    
    # Crear una cadena con todas las combinaciones y sus resultados
    mensaje = "Combinaciones de A, B, C y resultado de A AND B AND C:\n\n"
    for a, b, c, resultado in combinaciones:
        mensaje += f"A = {'Sí' if a else 'No'}, B = {'Sí' if b else 'No'}, C = {'Sí' if c else 'No'} -> Resultado: {'Verdadero' if resultado else 'Falso'}\n"
    
    # Mostrar el mensaje en un cuadro de diálogo
    messagebox.showinfo("Árbol de Decisión - Compuerta AND", mensaje)

    # Mostrar el árbol de decisión gráfico
    mostrar_arbol_grafico()

# Función para abrir la ventana del árbol de decisión al seleccionar Opción 1
def opcion_1():
    global ventana_arbol
    ventana.destroy()

    # Crear una ventana nueva para mostrar el árbol de decisión
    ventana_arbol = tk.Tk()
    ventana_arbol.title("Árbol de Decisión - Compuerta AND de 3 Variables")
    ventana_arbol.geometry("400x300")

    # Etiqueta y botón para mostrar todas las combinaciones
    tk.Label(ventana_arbol, text="Todas las combinaciones de A AND B AND C:").pack(pady=10)
    tk.Button(ventana_arbol, text="Mostrar Árbol de Decisión", command=mostrar_arbol).pack(pady=20)

    ventana_arbol.mainloop()

# Función para la opción 2
def opcion_2():
    messagebox.showinfo("Elección", "Elegiste la Opción 2")
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Elige una opción")
ventana.geometry("300x150")

tk.Label(ventana, text="Selecciona una opción:").pack(pady=10)

# Botones de opciones
tk.Button(ventana, text="Opción 1 AND", command=opcion_1).pack(pady=5)
tk.Button(ventana, text="Opción 2 OR", command=opcion_2).pack(pady=5)

ventana.mainloop()
