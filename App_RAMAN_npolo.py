# Raman Analysis App
# Copyright (c) 2024-2026 Natalia Polo-Moreno
# Licensed under the PolyForm Noncommercial License 1.0.0 (see LICENSE.md)

import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy.signal import find_peaks
import os

# Definir la constante de longitud de onda del láser
laser_wavelength = 532  # nm

# Variables globales para la navegación de gráficos
current_graph_index = 0
all_graphs = []

# Función para procesar un archivo y encontrar las bandas D, G y 2D
def process_raman_spectrum(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        raman_spectrum_df = pd.read_csv(file_path)
    elif ext == ".txt":
        try:
            raman_spectrum_df = pd.read_csv(file_path, sep=None, engine='python')
        except Exception:
            raman_spectrum_df = pd.read_csv(file_path, sep='\t')

    raman_shift = raman_spectrum_df.iloc[:, 0]
    intensity = raman_spectrum_df.iloc[:, 1]

    peaks, _ = find_peaks(intensity, height=0)
    peak_positions = raman_shift.iloc[peaks]
    peak_intensities = intensity.iloc[peaks]

    peaks_df = pd.DataFrame({
        'Raman Shift (cm⁻¹)': peak_positions,
        'Intensity': peak_intensities
    })

    d_band = peaks_df[(peaks_df['Raman Shift (cm⁻¹)'] > 1300) & (peaks_df['Raman Shift (cm⁻¹)'] < 1400)]
    g_band = peaks_df[(peaks_df['Raman Shift (cm⁻¹)'] > 1500) & (peaks_df['Raman Shift (cm⁻¹)'] < 1600)]
    two_d_band = peaks_df[(peaks_df['Raman Shift (cm⁻¹)'] > 2600) & (peaks_df['Raman Shift (cm⁻¹)'] < 2800)]

    id_intensity = d_band['Intensity'].max() if not d_band.empty else None
    ig_intensity = g_band['Intensity'].max() if not g_band.empty else None
    i2d_intensity = two_d_band['Intensity'].max() if not two_d_band.empty else None

    id_position = d_band['Raman Shift (cm⁻¹)'][d_band['Intensity'].idxmax()] if not d_band.empty else None
    ig_position = g_band['Raman Shift (cm⁻¹)'][g_band['Intensity'].idxmax()] if not g_band.empty else None
    i2d_position = two_d_band['Raman Shift (cm⁻¹)'][two_d_band['Intensity'].idxmax()] if not two_d_band.empty else None

    id_ig_ratio = id_intensity / ig_intensity if ig_intensity else None
    i2d_ig_ratio = i2d_intensity / ig_intensity if ig_intensity else None

    la_nm = (2.4e-10) * laser_wavelength**4 * (id_ig_ratio)**-1 if id_ig_ratio else None

    return {
        'File': os.path.basename(file_path),
        'ID': id_intensity,
        'IG': ig_intensity,
        'I2D': i2d_intensity,
        'ID/IG': id_ig_ratio,
        'I2D/IG': i2d_ig_ratio,
        'La (nm)': la_nm,
        'Raman Shift': raman_shift,
        'Intensity': intensity,
        'ID pos': id_position,
        'IG pos': ig_position,
        'I2D pos': i2d_position
    }

# Función para seleccionar archivos CSV o TXT y llenar la lista de archivos
def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(
        title="Seleccionar archivos CSV o TXT",
        filetypes=[("CSV or TXT files", "*.csv *.txt"), ("CSV files", "*.csv"), ("Text files", "*.txt")]
    )
    lista_archivos.delete(0, tk.END)
    for archivo in archivos:
        lista_archivos.insert(tk.END, archivo)

# Función para generar el análisis de los archivos seleccionados
def generar_analisis():
    global all_graphs, current_graph_index
    all_graphs = []  # Reiniciar la lista de gráficos
    current_graph_index = 0  # Reiniciar el índice del gráfico

    all_data = []
    for i in range(lista_archivos.size()):
        archivo = lista_archivos.get(i)
        data = process_raman_spectrum(archivo)
        all_data.append(data)

    # Crear un DataFrame con los resultados
    final_df = pd.DataFrame(all_data)

    # Extraer solo las columnas que necesitamos para la tabla
    summary_df = final_df[['File', 'ID', 'ID pos', 'IG', 'IG pos', 'I2D', 'I2D pos', 'ID/IG', 'I2D/IG', 'La (nm)']]

    # Calcular el promedio y la desviación estándar de cada columna
    average_row = summary_df[['ID', 'ID pos', 'IG', 'IG pos', 'I2D', 'I2D pos', 'ID/IG', 'I2D/IG', 'La (nm)']].mean()
    std_dev_row = summary_df[['ID', 'ID pos', 'IG', 'IG pos', 'I2D', 'I2D pos', 'ID/IG', 'I2D/IG', 'La (nm)']].std()

    # Crear DataFrames para las filas de promedio y desviación estándar
    average_row_df = pd.DataFrame([{
        'File': 'Promedio',
        'ID': average_row['ID'],
        'ID pos': average_row['ID pos'],
        'IG': average_row['IG'],
        'IG pos': average_row['IG pos'],
        'I2D': average_row['I2D'],
        'I2D pos': average_row['I2D pos'],
        'ID/IG': average_row['ID/IG'],
        'I2D/IG': average_row['I2D/IG'],
        'La (nm)': average_row['La (nm)']
    }])

    std_dev_row_df = pd.DataFrame([{
        'File': 'Desviación estándar',
        'ID': std_dev_row['ID'],
        'ID pos': std_dev_row['ID pos'],
        'IG': std_dev_row['IG'],
        'IG pos': std_dev_row['IG pos'],
        'I2D': std_dev_row['I2D'],
        'I2D pos': std_dev_row['I2D pos'],
        'ID/IG': std_dev_row['ID/IG'],
        'I2D/IG': std_dev_row['I2D/IG'],
        'La (nm)': std_dev_row['La (nm)']
    }])

    # Agregar las filas de promedio y desviación estándar al DataFrame
    summary_df = pd.concat([summary_df, average_row_df, std_dev_row_df], ignore_index=True)

    # Actualizar la tabla con los resultados
    for row in tabla.get_children():
        tabla.delete(row)

    for _, row in summary_df.iterrows():
        tabla.insert("", "end", values=tuple(row))

    # Crear los gráficos y guardarlos en la lista (los marcadores van en la posición detectada de cada pico)
    for index, row in final_df.iterrows():
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(row['Raman Shift'], row['Intensity'], label=row['File'])
        ax.scatter(row['ID pos'], row['ID'], color='red', label='ID')
        ax.scatter(row['IG pos'], row['IG'], color='green', label='IG')
        ax.scatter(row['I2D pos'], row['I2D'], color='blue', label='I2D')
        ax.set_xlabel("Raman Shift (cm⁻¹)")
        ax.set_ylabel("Intensity")
        ax.grid(True)
        ax.legend()
        all_graphs.append(fig)

    # Mostrar el primer gráfico
    mostrar_grafico(0)

# Función para reiniciar el dashboard
def reset_dashboard():
    global all_graphs, current_graph_index

    # Limpiar lista de archivos
    lista_archivos.delete(0, tk.END)

    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # Limpiar gráfico
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    # Reiniciar estado interno
    all_graphs = []
    current_graph_index = 0

# Función para mostrar un gráfico por su índice
def mostrar_grafico(index):
    global current_graph_index

    # Limpiar el área de gráficos
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    current_graph_index = index
    fig = all_graphs[current_graph_index]

    # Crear el canvas para el gráfico
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Agregar la barra de herramientas de navegación del gráfico
    toolbar = NavigationToolbar2Tk(canvas, frame_grafico)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Función para mostrar el siguiente gráfico
def mostrar_siguiente_grafico():
    if current_graph_index < len(all_graphs) - 1:
        mostrar_grafico(current_graph_index + 1)

# Función para mostrar el gráfico anterior
def mostrar_anterior_grafico():
    if current_graph_index > 0:
        mostrar_grafico(current_graph_index - 1)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Raman Analysis App")
ventana.geometry("1200x800")

# Marco izquierdo para el botón y la lista de archivos
frame_izquierdo = tk.Frame(ventana)
frame_izquierdo.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Botón para seleccionar archivos
btn_seleccionar = tk.Button(frame_izquierdo, text="Select files", command=seleccionar_archivos)
btn_seleccionar.pack(pady=10)

# Lista de archivos seleccionados
lista_archivos = tk.Listbox(frame_izquierdo, height=15)
lista_archivos.pack(padx=10, pady=10, fill=tk.BOTH)

# Botones para generar el análisis y reiniciar
btn_analisis = tk.Button(frame_izquierdo, text="Generar análisis", command=generar_analisis)
btn_analisis.pack(pady=10)
btn_reset = tk.Button(frame_izquierdo, text="Reset", command=reset_dashboard)
btn_reset.pack(pady=5)

# Marco derecho para la tabla de resultados y el gráfico
frame_derecho = tk.Frame(ventana)
frame_derecho.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill=tk.BOTH)

# Crear scrollbar horizontal
scrollbar_x = tk.Scrollbar(frame_derecho, orient="horizontal")
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

# Crear tabla con scrollbar
cols = ("File", "ID", "ID pos", "IG", "IG pos", "I2D", "I2D pos", "ID/IG", "I2D/IG", "La (nm)")
tabla = ttk.Treeview(frame_derecho, columns=cols, show="headings", height=10, xscrollcommand=scrollbar_x.set)
tabla.pack(side=tk.TOP, fill=tk.X)

# Configurar el scrollbar
scrollbar_x.config(command=tabla.xview)

encabezados_visibles = {
    "File": "File",
    "ID": "ID",
    "ID pos": "ID pos (cm⁻¹)",
    "IG": "IG",
    "IG pos": "IG pos (cm⁻¹)",
    "I2D": "I2D",
    "I2D pos": "I2D pos (cm⁻¹)",
    "ID/IG": "ID/IG",
    "I2D/IG": "I2D/IG",
    "La (nm)": "La (nm)"
}

for col in cols:
    tabla.heading(col, text=encabezados_visibles[col])

# Marco para el gráfico debajo de la tabla
frame_grafico = tk.Frame(ventana)
frame_grafico.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

# Botones para navegar entre los gráficos
frame_navegacion = tk.Frame(ventana)
frame_navegacion.pack(side=tk.TOP, pady=10)

btn_anterior = tk.Button(frame_navegacion, text="Anterior", command=mostrar_anterior_grafico)
btn_anterior.pack(side=tk.LEFT, padx=10)

btn_siguiente = tk.Button(frame_navegacion, text="Siguiente", command=mostrar_siguiente_grafico)
btn_siguiente.pack(side=tk.LEFT, padx=10)

# Pie de página
footer = tk.Label(ventana, text="Developed by: Natalia Polo")
footer.pack(side=tk.BOTTOM, pady=10)

# Ejecutar la aplicación
ventana.mainloop()
