import tkinter as tk
from tkinter import ttk

PALABRAS_RESERVADAS = ["if", "else", "while", "int", "float", "return"]

def analizar_lexico(codigo):
    tokens = []
    linea = 1
    columna = 1
    i = 0
    longitud = len(codigo)

    while i < longitud:
        caracter = codigo[i]

        # 1. Ignorar espacios en blanco y tabulaciones
        if caracter == ' ' or caracter == '\t':
            i += 1
            columna += 1
            continue

        # 2. Controlar saltos de línea
        if caracter == '\n':
            linea += 1
            columna = 1
            i += 1
            continue

        # 3. Manejo de Comentarios de Línea (#) - Variante Python
        if caracter == '#':
            while i < longitud and codigo[i] != '\n':
                i += 1
                columna += 1
            continue  # Consume el comentario sin generar token

        # 4. Operadores Distintivos de 2 Caracteres (//, **, :=) y Relacionales Compuestos
        if i + 1 < longitud:
            par = codigo[i:i+2]
            if par in ['//', '**', ':=']:
                tokens.append((linea, columna, "DISTINCT_OP", par))
                i += 2
                columna += 2
                continue
            elif par in ['==', '!=', '<=', '>=']:
                tokens.append((linea, columna, "RELOP", par))
                i += 2
                columna += 2
                continue

        # 5. Operador Lógico 'and', Palabras Reservadas e Identificadores (Solo _ y letras)
        if caracter.isalpha() or caracter == '_':
            inicio_columna = columna
            lexema = ""
            
            while i < longitud and (codigo[i].isalnum() or codigo[i] == '_'):
                lexema += codigo[i]
                i += 1
                columna += 1

            if lexema == "and":
                tipo = "LOGICAL_OP"  # Regla específica para 'and'
            elif lexema in PALABRAS_RESERVADAS:
                tipo = "KEYWORD"
            else:
                tipo = "IDENTIFIER"

            tokens.append((linea, inicio_columna, tipo, lexema))
            continue

        # 6. Números (enteros y decimales)
        if caracter.isdigit():
            inicio_columna = columna
            lexema = ""
            
            while i < longitud and (codigo[i].isdigit() or codigo[i] == '.'):
                lexema += codigo[i]
                i += 1
                columna += 1

            tokens.append((linea, inicio_columna, "NUMBER", lexema))
            continue

        # 7. Asignación y Operadores Relacionales Simples
        if caracter == '=':
            tokens.append((linea, columna, "ASSIGN", '='))
            i += 1
            columna += 1
            continue
        elif caracter in ['<', '>']:
            tokens.append((linea, columna, "RELOP", caracter))
            i += 1
            columna += 1
            continue

        # 8. Operadores Aritméticos Simples (+, -, *, /)
        if caracter in ['+', '-', '*', '/']:
            tokens.append((linea, columna, "ARITHOP", caracter))
            i += 1
            columna += 1
            continue

        # 9. Elemento Especial (Dos puntos :) y Delimitadores
        if caracter == ':':
            tokens.append((linea, columna, "BLOCK_COLON", caracter))
            i += 1
            columna += 1
            continue

        if caracter in [';', ',', '(', ')', '{', '}']:
            tokens.append((linea, columna, "DELIMITER", caracter))
            i += 1
            columna += 1
            continue

        # 10. Carácter no reconocido (Error Léxico)
        tokens.append((linea, columna, "ERROR", caracter))
        i += 1
        columna += 1

    return tokens

# interdaz gráfica con Tkinter
def ejecutar_analisis():
    texto_codigo = entrada_texto.get("1.0", tk.END)
    for fila in tabla.get_children():
        tabla.delete(fila)

    lista_tokens = analizar_lexico(texto_codigo)
    for lin, col, tipo, lex in lista_tokens:
        tabla.insert("", tk.END, values=(lin, col, tipo, lex))

def borrar_texto():
    entrada_texto.delete("1.0", tk.END)
    for fila in tabla.get_children():
        tabla.delete(fila)

ventana = tk.Tk()
ventana.title("Analizador Léxico - Variante Python")
ventana.geometry("700x600")

label_entrada = tk.Label(ventana, text="Código fuente de entrada:", font=("Arial", 10, "bold"))
label_entrada.pack(anchor="w", padx=10, pady=(10, 0))

entrada_texto = tk.Text(ventana, height=8, font=("Consolas", 10))
entrada_texto.pack(fill="x", padx=10, pady=5)

# Ejemplo precargado con las características de la Variante 2
codigo_prueba = """int contador = 0 # Comentario de linea
if contador < 10 and contador != 5:
    contador := contador ** 2 // 3
"""
entrada_texto.insert(tk.END, codigo_prueba)

frame_botones = tk.Frame(ventana)
frame_botones.pack(fill="x", padx=10, pady=5)

btn_analizar = tk.Button(frame_botones, text="Analizar Código", bg="#2196F3", fg="white", font=("Arial", 9, "bold"), command=ejecutar_analisis)
btn_analizar.pack(side="left", padx=(0, 5))

btn_limpiar = tk.Button(frame_botones, text="Limpiar", command=borrar_texto)
btn_limpiar.pack(side="left")

label_salida = tk.Label(ventana, text="Tabla de Tokens:", font=("Arial", 10, "bold"))
label_salida.pack(anchor="w", padx=10, pady=(10, 0))

columnas = ("linea", "columna", "tipo", "lexema")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

tabla.heading("linea", text="Línea")
tabla.heading("columna", text="Columna")
tabla.heading("tipo", text="Tipo de Token")
tabla.heading("lexema", text="Lexema")

tabla.column("linea", width=80, anchor="center")
tabla.column("columna", width=80, anchor="center")
tabla.column("tipo", width=180, anchor="center")
tabla.column("lexema", width=220, anchor="w")

scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

ejecutar_analisis()
ventana.mainloop()