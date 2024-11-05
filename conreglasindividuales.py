# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:12:03 2024

@author: itzel
"""

import re
import json
import matplotlib.pyplot as plt
from itertools import product
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

LETRAS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

# Funciones para manejo de lógica y reglas
def convertir_a_formula(oracion):
    proposiciones = re.split(r'\s+y\s+|\s+o\s+', oracion)
    formula = oracion.replace(" y ", " ∧ ").replace(" o ", " ∨ ")
    mapeo = {proposiciones[i]: LETRAS[i] for i in range(len(proposiciones))}
    
    for proposicion, letra in mapeo.items():
        formula = formula.replace(proposicion, letra)
    
    return formula, mapeo

def detectar_palabras_clave(oracion):
    palabras_clave = re.findall(r'\b(y|o|no)\b', oracion)
    return palabras_clave

def generar_tabla_verdad(formula, mapeo):
    proposiciones = list(mapeo.values())
    n = len(proposiciones)
    combinaciones = list(product([True, False], repeat=n))
    tabla = []

    for combinacion in combinaciones:
        valores = dict(zip(proposiciones, combinacion))
        evaluacion = eval(formula.replace("∧", " and ").replace("∨", " or "), {}, valores)
        tabla.append((combinacion, evaluacion))
    
    return tabla

def imprimir_tabla_verdad(tabla, mapeo):
    proposiciones = list(mapeo.values())
    header = " | ".join(proposiciones) + " | Resultado"
    output = header + "\n" + "-" * len(header) + "\n"
    
    for fila in tabla:
        valores = ["V" if v else "F" for v in fila[0]]
        resultado = "V" if fila[1] else "F"
        output += " | ".join(valores) + " | " + resultado + "\n"
    
    return output

def dibujar_arbol_decision(tabla, mapeo):
    proposiciones = list(mapeo.values())
    fig, ax = plt.subplots(figsize=(10, 8))
    
    def construir_arbol(ax, combinacion, resultado, nivel=0, pos=0):
        if nivel == len(proposiciones):
            ax.text(pos, -nivel, 'V' if resultado else 'F', ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen" if resultado else "lightcoral"))
            return
        prop = proposiciones[nivel]
        true_pos = pos - 0.5 / (2 ** (nivel + 1))
        false_pos = pos + 0.5 / (2 ** (nivel + 1))
        
        ax.text(pos, -nivel, f"{prop}", ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        construir_arbol(ax, combinacion, resultado, nivel + 1, true_pos)
        construir_arbol(ax, combinacion, resultado, nivel + 1, false_pos)
        ax.plot([pos, true_pos], [-nivel, -(nivel + 1)], color="gray")
        ax.plot([pos, false_pos], [-nivel, -(nivel + 1)], color="gray")

    for i, (combinacion, resultado) in enumerate(tabla):
        construir_arbol(ax, combinacion, resultado)

    ax.set_title("Árbol de Decisión")
    ax.axis("off")
    plt.show()

def ingresar_regla():
    oracion = simpledialog.askstring("Ingresar nueva regla", "Ingrese una proposición compuesta:")
    if oracion:
        palabras_clave = detectar_palabras_clave(oracion)
        formula, mapeo = convertir_a_formula(oracion)
        reglas.append({"oracion_original": oracion, "formula": formula, "mapeo": mapeo, "palabras_clave": palabras_clave})
        messagebox.showinfo("Información", f"Regla añadida: \"{oracion}\" con palabras clave: {', '.join(palabras_clave)}.")

def mostrar_reglas():
    for idx, regla in enumerate(reglas, 1):
        oracion_original = regla["oracion_original"]
        formula = regla["formula"]
        mapeo = regla["mapeo"]
        palabras_clave = regla.get("palabras_clave", [])
        tabla = generar_tabla_verdad(formula, mapeo)
        
        info = (
            f"Regla {idx}:\n"
            f"Texto original: {oracion_original}\n"
            f"Fórmula lógica: {formula}\n"
            f"Palabras clave: {', '.join(palabras_clave)}\n\n"
            f"Tabla de verdad:\n{imprimir_tabla_verdad(tabla, mapeo)}"
        )
        
        messagebox.showinfo("Reglas", info)
        dibujar_arbol_decision(tabla, mapeo)

def guardar_reglas():
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(reglas, file)
    messagebox.showinfo("Guardar reglas", f"Reglas guardadas en {archivo}.")

def cargar_reglas():
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reglas.extend(json.load(file))
        messagebox.showinfo("Cargar reglas", f"Reglas cargadas desde {archivo}.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado.")

def evaluar_proposicion_atomica():
    if reglas:
        formula, mapeo = reglas[0]["formula"], reglas[0]["mapeo"]
        respuestas = {letra: (simpledialog.askstring(f"Evaluar {proposicion}", f"¿{proposicion} es Verdadero (V) o Falso (F)?").lower() == 'v')
                      for proposicion, letra in mapeo.items()}
        evaluacion = eval(formula.replace("∧", " and ").replace("∨", " or "), {}, respuestas)
        messagebox.showinfo("Evaluación de proposición", f"Resultado: {'V' if evaluacion else 'F'}")
    else:
        messagebox.showerror("Error", "No hay reglas cargadas para evaluar.")

def mostrar_tabla_atomos():
    if reglas:
        for idx, regla in enumerate(reglas, 1):
            mapeo = regla["mapeo"]
            combinaciones = list(product([True, False], repeat=len(mapeo)))
            atoms_table = "\n".join([" | ".join("V" if v else "F" for v in combo) for combo in combinaciones])
            messagebox.showinfo(f"Tabla de átomos para Regla {idx}", atoms_table)
    else:
        messagebox.showerror("Error", "No hay reglas cargadas para mostrar la tabla de átomos.")

def mostrar_clausulas_horn():
    if reglas:
        output = ""
        for regla in reglas:
            formula, mapeo = regla["formula"], regla["mapeo"]
            tabla = generar_tabla_verdad(formula, mapeo)
            for combinacion, resultado in tabla:
                antecedente = [f"¬{letra}" if not v else letra for letra, v in zip(mapeo.values(), combinacion)]
                consecuente = "V" if resultado else "F"
                output += f"{' ∧ '.join(antecedente)} → {consecuente}\n"
        messagebox.showinfo("Cláusulas de Horn", output)
    else:
        messagebox.showerror("Error", "No hay reglas cargadas para mostrar cláusulas de Horn.")

def mostrar_tabla_elementos_clausulas():
    if reglas:
        output = ""
        for idx, regla in enumerate(reglas, 1):
            mapeo = regla["mapeo"]
            output += f"\nTabla de elementos para Regla {idx}:\n" + "\n".join(f"{key} = {value}" for key, value in mapeo.items())
        messagebox.showinfo("Tabla de elementos de cláusulas de Horn", output)
    else:
        messagebox.showerror("Error", "No hay reglas cargadas para mostrar la tabla de elementos.")

def guardar_clausulas_horn():
    archivo_txt = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar cláusulas de Horn")
    if archivo_txt:
        with open(archivo_txt, 'w', encoding='utf-8') as file:
            for i, regla in enumerate(reglas, 1):
                formula, mapeo = regla["formula"], regla["mapeo"]
                tabla = generar_tabla_verdad(formula, mapeo)
                clausulas = mostrar_clausulas_horn(tabla, mapeo)
                file.write(f"Regla {i}:\n{clausulas}\n")
        messagebox.showinfo("Guardado", f"Cláusulas de Horn guardadas en {archivo_txt}.")

def cargar_oraciones_desde_txt():
    archivo_txt = filedialog.askopenfilename(title="Seleccione el archivo de oraciones", filetypes=[("Archivos de texto", "*.txt")])
    if archivo_txt:
        with open(archivo_txt, 'r', encoding='utf-8') as file:
            for line in file:
                oracion = line.strip()
                if oracion:
                    palabras_clave = detectar_palabras_clave(oracion)
                    formula, mapeo = convertir_a_formula(oracion)
                    reglas.append({"oracion_original": oracion, "formula": formula, "mapeo": mapeo, "palabras_clave": palabras_clave})
        messagebox.showinfo("Cargado", f"Oraciones cargadas desde {archivo_txt}.")

# Interfaz gráfica
archivo = "reglas.json"
reglas = []

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Gestor de Reglas Lógicas")

    tk.Button(root, text="Ingresar nueva regla", command=ingresar_regla).pack()
    tk.Button(root, text="Mostrar reglas", command=mostrar_reglas).pack()
    tk.Button(root, text="Guardar reglas", command=guardar_reglas).pack()
    tk.Button(root, text="Cargar reglas", command=cargar_reglas).pack()
    tk.Button(root, text="Evaluar proposición atómica", command=evaluar_proposicion_atomica).pack()
    tk.Button(root, text="Mostrar tabla de átomos", command=mostrar_tabla_atomos).pack()
    tk.Button(root, text="Mostrar cláusulas de Horn", command=mostrar_clausulas_horn).pack()
    tk.Button(root, text="Mostrar tabla de elementos de cláusulas de Horn", command=mostrar_tabla_elementos_clausulas).pack()
    tk.Button(root, text="Guardar cláusulas de Horn", command=guardar_clausulas_horn).pack()
    tk.Button(root, text="Cargar oraciones desde archivo TXT", command=cargar_oraciones_desde_txt).pack()

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()

