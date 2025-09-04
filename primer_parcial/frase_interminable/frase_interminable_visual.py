import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
import time

class FraseInterminableVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("La Frase Interminable - Visualización")
        self.root.geometry("1200x900")
        
        # Variables del juego
        self.jugadores = []
        self.num_jugadores = 0
        self.frases_dichas = 0  # Contador de frases exitosas
        self.frase_anterior = ""
        self.estado = "configuracion"  # configuracion, etapa1, etapa2, etapa3, juego
        
        # Variables para comparación paso a paso
        self.indice_comparacion = 0
        self.comparacion_activa = False
        self.frase_a_comparar = ""
        self.nueva_frase = ""
        self.comparaciones_realizadas = []  # Para guardar el historial sin spoilers
        
        # Variables para normalización paso a paso
        self.normalizacion_activa = False
        self.frase_original = ""
        self.indice_normalizacion = 0
        self.texto_siendo_normalizado = ""
        self.cambios_encontrados = []  # Lista de cambios: {'tipo': 'espacio'/'mayuscula', 'pos': int, 'char': str}
        self.tipo_cambio_actual = ""
        
        # Crear la interfaz
        self.crear_interfaz()
        
    def normalizar_espacios(self, texto):
        """Normaliza espacios múltiples a uno solo y convierte a minúsculas"""
        texto_sin_espacios = re.sub(r'\s+', ' ', texto.strip())
        return texto_sin_espacios.lower()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="La Frase Interminable", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Configuración inicial
        self.frame_config = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        self.frame_config.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.frame_config, text="Número de jugadores:").grid(row=0, column=0, sticky=tk.W)
        self.entry_jugadores = ttk.Entry(self.frame_config, width=10)
        self.entry_jugadores.grid(row=0, column=1, padx=5)
        
        ttk.Button(self.frame_config, text="Iniciar Juego", 
                  command=self.iniciar_juego).grid(row=0, column=2, padx=5)
        
        # Información del juego
        self.frame_info = ttk.LabelFrame(main_frame, text="Estado del Juego", padding="10")
        self.frame_info.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.label_frases = ttk.Label(self.frame_info, text="Frases dichas: 0")
        self.label_frases.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.label_turno = ttk.Label(self.frame_info, text="Turno actual: Jugador 1")
        self.label_turno.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.label_frase = ttk.Label(self.frame_info, text="Frase anterior: (vacía)", 
                                    wraplength=600, justify=tk.LEFT)
        self.label_frase.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Frame para las etapas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Etapa 1: Validación y Verificación
        self.frame_etapa1 = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_etapa1, text="Etapa 1: Validación y Verificación")
        self.crear_etapa1()
        
        # Etapa 2: Determinación de turno
        self.frame_etapa2 = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.frame_etapa2, text="Etapa 2: Turno")
        self.crear_etapa2()
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
    def crear_etapa1(self):
        ttk.Label(self.frame_etapa1, text="ETAPA 1: Validación y Verificación", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
        
        ttk.Label(self.frame_etapa1, text="Ingrese su frase:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_palabra = ttk.Entry(self.frame_etapa1, width=50, font=("Arial", 11))
        self.entry_palabra.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Botones de control
        button_frame = ttk.Frame(self.frame_etapa1)
        button_frame.grid(row=3, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_frame, text="1. Iniciar Normalización", 
                  command=self.iniciar_normalizacion).pack(side=tk.LEFT, padx=5)
        
        self.btn_siguiente_cambio = ttk.Button(button_frame, text="Siguiente Cambio", 
                                              command=self.normalizar_siguiente_cambio, state="disabled")
        self.btn_siguiente_cambio.pack(side=tk.LEFT, padx=5)
        
        self.btn_iniciar_comparacion = ttk.Button(button_frame, text="2. Iniciar Comparación", 
                                                 command=self.iniciar_comparacion_visual, state="disabled")
        self.btn_iniciar_comparacion.pack(side=tk.LEFT, padx=5)
        
        self.btn_siguiente_char = ttk.Button(button_frame, text="Siguiente Carácter", 
                                            command=self.comparar_siguiente_caracter, state="disabled")
        self.btn_siguiente_char.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Reiniciar", 
                  command=self.reiniciar_validacion).pack(side=tk.LEFT, padx=5)
        
        # Canvas para mostrar la comparación visual
        self.canvas_comparacion = tk.Canvas(self.frame_etapa1, height=250, bg="white", 
                                           highlightbackground="gray", highlightthickness=1)
        self.canvas_comparacion.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Área de explicación
        self.text_validacion = scrolledtext.ScrolledText(self.frame_etapa1, height=12, width=80, 
                                                        font=("Courier", 10))
        self.text_validacion.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.frame_etapa1.columnconfigure(0, weight=1)
        self.frame_etapa1.rowconfigure(5, weight=1)
        
    def crear_etapa2(self):
        ttk.Label(self.frame_etapa2, text="ETAPA 2: Determinación de Turno", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        # Canvas para mostrar el cálculo del módulo
        self.canvas_turno = tk.Canvas(self.frame_etapa2, height=150, bg="white", 
                                     highlightbackground="gray", highlightthickness=1)
        self.canvas_turno.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(self.frame_etapa2, text="Calcular Siguiente Turno", 
                  command=self.calcular_turno).grid(row=2, column=0, pady=5)
        
        # Área de explicación del módulo
        self.text_turno = scrolledtext.ScrolledText(self.frame_etapa2, height=8, width=70, 
                                                   font=("Courier", 10))
        self.text_turno.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.frame_etapa2.columnconfigure(0, weight=1)
        self.frame_etapa2.rowconfigure(3, weight=1)
        
        
    def iniciar_juego(self):
        try:
            self.num_jugadores = int(self.entry_jugadores.get())
            if self.num_jugadores < 2:
                messagebox.showerror("Error", "Debe haber al menos 2 jugadores")
                return
            
            self.jugadores = [f"Jugador {i+1}" for i in range(self.num_jugadores)]
            self.frases_dichas = 0
            self.frase_anterior = ""
            
            self.actualizar_info()
            messagebox.showinfo("Juego Iniciado", 
                              f"Juego iniciado con {self.num_jugadores} jugadores.\n"
                              f"Comienza {self.jugadores[0]}")
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de jugadores")
    
    def actualizar_info(self):
        if self.num_jugadores > 0:
            # Calcular quién tiene el turno basado en frases dichas
            jugador_actual_num = (self.frases_dichas % self.num_jugadores) + 1
            jugador_actual = f"Jugador {jugador_actual_num}"
            self.label_frases.config(text=f"Frases dichas: {self.frases_dichas}")
            self.label_turno.config(text=f"Turno actual: {jugador_actual}")
            frase_mostrar = self.frase_anterior if self.frase_anterior else "(vacía)"
            self.label_frase.config(text=f"Frase anterior: {frase_mostrar}")
    
    def iniciar_normalizacion(self):
        """Inicia el proceso de normalización paso a paso"""
        frase_nueva_raw = self.entry_palabra.get().strip()
        
        self.canvas_comparacion.delete("all")
        self.text_validacion.delete(1.0, tk.END)
        self.text_validacion.insert(tk.END, "=== PASO 1: NORMALIZACIÓN PASO A PASO ===\n\n")
        
        if not frase_nueva_raw:
            self.text_validacion.insert(tk.END, "❌ ERROR: Input vacío\n")
            self.text_validacion.insert(tk.END, "Debe ingresar al menos una palabra.\n")
            return
        
        self.text_validacion.insert(tk.END, f"Texto original: '{frase_nueva_raw}'\n")
        self.text_validacion.insert(tk.END, f"Longitud original: {len(frase_nueva_raw)} caracteres\n\n")
        
        # Preparar variables para normalización paso a paso
        self.frase_original = frase_nueva_raw
        self.texto_siendo_normalizado = frase_nueva_raw
        self.indice_normalizacion = 0
        self.cambios_encontrados = []
        
        # Encontrar todos los cambios necesarios
        self.encontrar_cambios_normalizacion(frase_nueva_raw)
        
        if not self.cambios_encontrados:
            self.text_validacion.insert(tk.END, "✅ No se requiere normalización\n")
            self.text_validacion.insert(tk.END, "El texto ya está en formato correcto\n")
            self.nueva_frase = frase_nueva_raw.lower()  # Solo convertir a minúsculas
            self.entry_palabra.delete(0, tk.END)
            self.entry_palabra.insert(0, self.nueva_frase)
            self.btn_iniciar_comparacion.config(state="normal")
            self.dibujar_estado_normalizacion_completa()
        else:
            total_cambios = len(self.cambios_encontrados)
            espacios = sum(1 for c in self.cambios_encontrados if c['tipo'] == 'espacio')
            mayusculas = sum(1 for c in self.cambios_encontrados if c['tipo'] == 'mayuscula')
            
            self.text_validacion.insert(tk.END, f"🔍 Se encontraron {total_cambios} cambios necesarios:\n")
            self.text_validacion.insert(tk.END, f"   - {espacios} espacios múltiples a eliminar\n")
            self.text_validacion.insert(tk.END, f"   - {mayusculas} mayúsculas a convertir\n")
            self.text_validacion.insert(tk.END, "Presione 'Siguiente Cambio' para normalizar paso a paso\n\n")
            self.normalizacion_activa = True
            self.btn_siguiente_cambio.config(state="normal")
            self.dibujar_estado_normalizacion_inicial()
    
    def encontrar_cambios_normalizacion(self, texto):
        """Encuentra todos los cambios necesarios: espacios múltiples y mayúsculas"""
        self.cambios_encontrados = []
        
        # Encontrar espacios múltiples
        i = 0
        while i < len(texto) - 1:
            if texto[i] == ' ' and texto[i + 1] == ' ':
                # Encontrar todos los espacios consecutivos
                j = i + 1
                while j < len(texto) and texto[j] == ' ':
                    self.cambios_encontrados.append({
                        'tipo': 'espacio',
                        'pos': j,
                        'char': ' ',
                        'accion': 'eliminar'
                    })
                    j += 1
                i = j
            else:
                i += 1
        
        # Encontrar mayúsculas
        for i, char in enumerate(texto):
            if char.isupper():
                self.cambios_encontrados.append({
                    'tipo': 'mayuscula',
                    'pos': i,
                    'char': char,
                    'nuevo_char': char.lower(),
                    'accion': 'convertir'
                })
        
        # Ordenar cambios por posición (espacios primero, luego mayúsculas)
        self.cambios_encontrados.sort(key=lambda x: (x['pos'], x['tipo'] == 'mayuscula'))
    
    def normalizar_siguiente_cambio(self):
        """Realiza el siguiente cambio de normalización"""
        if not self.normalizacion_activa or self.indice_normalizacion >= len(self.cambios_encontrados):
            self.finalizar_normalizacion()
            return
        
        cambio = self.cambios_encontrados[self.indice_normalizacion]
        self.tipo_cambio_actual = cambio['tipo']
        
        # Ajustar posición según eliminaciones previas
        espacios_eliminados = sum(1 for i in range(self.indice_normalizacion) 
                                 if self.cambios_encontrados[i]['tipo'] == 'espacio')
        pos_actual = cambio['pos'] - espacios_eliminados
        
        self.text_validacion.insert(tk.END, f"Paso {self.indice_normalizacion + 1}: ")
        
        if cambio['tipo'] == 'espacio':
            self.text_validacion.insert(tk.END, f"Eliminando espacio en posición {pos_actual}\n")
            self.text_validacion.insert(tk.END, f"Antes: '{self.texto_siendo_normalizado}'\n")
            
            # Eliminar el espacio
            self.texto_siendo_normalizado = (self.texto_siendo_normalizado[:pos_actual] + 
                                           self.texto_siendo_normalizado[pos_actual + 1:])
            
        elif cambio['tipo'] == 'mayuscula':
            char_original = cambio['char']
            char_nuevo = cambio['nuevo_char']
            self.text_validacion.insert(tk.END, f"Convirtiendo '{char_original}' → '{char_nuevo}' en posición {pos_actual}\n")
            self.text_validacion.insert(tk.END, f"Antes: '{self.texto_siendo_normalizado}'\n")
            
            # Convertir la mayúscula
            texto_lista = list(self.texto_siendo_normalizado)
            if pos_actual < len(texto_lista):
                texto_lista[pos_actual] = char_nuevo
                self.texto_siendo_normalizado = ''.join(texto_lista)
        
        self.text_validacion.insert(tk.END, f"Después: '{self.texto_siendo_normalizado}'\n\n")
        
        self.indice_normalizacion += 1
        
        # Actualizar visualización
        self.dibujar_estado_normalizacion_paso(pos_actual, cambio)
        
        # Verificar si terminamos
        if self.indice_normalizacion >= len(self.cambios_encontrados):
            self.finalizar_normalizacion()
    
    def finalizar_normalizacion(self):
        """Finaliza el proceso de normalización"""
        self.normalizacion_activa = False
        self.btn_siguiente_cambio.config(state="disabled")
        
        # Contar tipos de cambios realizados
        espacios_eliminados = sum(1 for c in self.cambios_encontrados if c['tipo'] == 'espacio')
        mayusculas_convertidas = sum(1 for c in self.cambios_encontrados if c['tipo'] == 'mayuscula')
        
        self.text_validacion.insert(tk.END, "✅ Normalización completada\n")
        self.text_validacion.insert(tk.END, f"Texto final: '{self.texto_siendo_normalizado}'\n")
        self.text_validacion.insert(tk.END, f"Cambios realizados:\n")
        self.text_validacion.insert(tk.END, f"   - {espacios_eliminados} espacios eliminados\n")
        self.text_validacion.insert(tk.END, f"   - {mayusculas_convertidas} mayúsculas convertidas\n")
        self.text_validacion.insert(tk.END, "Presione '2. Iniciar Comparación' para continuar\n")
        
        # Actualizar el campo de entrada y variables
        self.entry_palabra.delete(0, tk.END)
        self.entry_palabra.insert(0, self.texto_siendo_normalizado)
        self.nueva_frase = self.texto_siendo_normalizado
        
        # Habilitar siguiente paso
        self.btn_iniciar_comparacion.config(state="normal")
        
        # Mostrar resultado final
        self.dibujar_estado_normalizacion_completa()
    
    def dibujar_estado_normalizacion_inicial(self):
        """Dibuja el estado inicial de la normalización"""
        self.canvas_comparacion.delete("all")
        
        # Título
        self.canvas_comparacion.create_text(10, 10, anchor="w", 
                                           text="Normalización paso a paso: espacios + mayúsculas", 
                                           font=("Arial", 12, "bold"))
        
        # Mostrar texto original
        self.canvas_comparacion.create_text(10, 40, anchor="w", 
                                           text="Texto a normalizar:", font=("Arial", 10, "bold"))
        
        self.dibujar_texto_con_cambios(self.texto_siendo_normalizado, 60, -1)  # -1 = no mostrar iterador aún
        
        # Leyenda
        self.canvas_comparacion.create_text(10, 120, anchor="w", 
                                           text="Leyenda: ␣ = espacio | Rojo = espacios a eliminar | Azul = mayúsculas a convertir", 
                                           font=("Arial", 9), fill="gray")
    
    def dibujar_estado_normalizacion_paso(self, pos_cambiada, cambio):
        """Dibuja el estado después de realizar un cambio"""
        self.canvas_comparacion.delete("all")
        
        # Título según tipo de cambio
        if cambio['tipo'] == 'espacio':
            titulo = f"Paso {self.indice_normalizacion}: Espacio eliminado"
        else:
            titulo = f"Paso {self.indice_normalizacion}: Mayúscula convertida"
        
        self.canvas_comparacion.create_text(10, 10, anchor="w", 
                                           text=titulo, 
                                           font=("Arial", 12, "bold"))
        
        # Mostrar texto actual
        self.canvas_comparacion.create_text(10, 40, anchor="w", 
                                           text="Texto actual:", font=("Arial", 10, "bold"))
        
        # Mostrar donde se realizó el cambio
        self.dibujar_texto_con_cambios(self.texto_siendo_normalizado, 60, pos_cambiada)
        
        # Mostrar progreso
        restantes = len(self.cambios_encontrados) - self.indice_normalizacion
        espacios_hechos = sum(1 for i in range(self.indice_normalizacion) 
                             if self.cambios_encontrados[i]['tipo'] == 'espacio')
        mayusculas_hechas = sum(1 for i in range(self.indice_normalizacion) 
                               if self.cambios_encontrados[i]['tipo'] == 'mayuscula')
        
        self.canvas_comparacion.create_text(10, 100, anchor="w", 
                                           text=f"Cambios: {espacios_hechos} espacios + {mayusculas_hechas} mayúsculas | Restantes: {restantes}", 
                                           font=("Arial", 10), fill="blue")
    
    def dibujar_estado_normalizacion_completa(self):
        """Dibuja el estado final de la normalización"""
        self.canvas_comparacion.delete("all")
        
        # Título
        self.canvas_comparacion.create_text(10, 10, anchor="w", 
                                           text="Normalización completada", 
                                           font=("Arial", 12, "bold"), fill="green")
        
        # Comparación antes/después
        self.canvas_comparacion.create_text(10, 40, anchor="w", 
                                           text="Original:", font=("Arial", 10, "bold"))
        self.dibujar_texto_simple(self.frase_original, 60, "black")
        
        self.canvas_comparacion.create_text(10, 90, anchor="w", 
                                           text="Normalizado:", font=("Arial", 10, "bold"))
        self.dibujar_texto_simple(self.texto_siendo_normalizado, 110, "green")
        
        # Estadísticas
        espacios_eliminados = sum(1 for c in self.cambios_encontrados if c['tipo'] == 'espacio')
        mayusculas_convertidas = sum(1 for c in self.cambios_encontrados if c['tipo'] == 'mayuscula')
        
        self.canvas_comparacion.create_text(10, 150, anchor="w", 
                                           text=f"✅ {espacios_eliminados} espacios eliminados + {mayusculas_convertidas} mayúsculas convertidas", 
                                           font=("Arial", 10), fill="green")
    
    def dibujar_texto_con_cambios(self, texto, y_pos, pos_iterador):
        """Dibuja texto mostrando espacios múltiples y mayúsculas a cambiar"""
        x_offset = 10
        char_width = 15
        
        for i, char in enumerate(texto):
            # Determinar color según tipo de cambio necesario
            color = "black"  # Por defecto
            
            # Rojo para espacios múltiples
            if char == ' ' and i < len(texto) - 1 and texto[i + 1] == ' ':
                color = "red"
            # Azul para mayúsculas
            elif char.isupper():
                color = "blue"
            
            display_char = '␣' if char == ' ' else char
            self.canvas_comparacion.create_text(x_offset + i * char_width, y_pos, anchor="w", 
                                               text=display_char, font=("Courier", 11), fill=color)
        
        # Dibujar iterador si se especificó posición
        if pos_iterador >= 0:
            x_pos = x_offset + pos_iterador * char_width
            
            if self.tipo_cambio_actual == 'espacio':
                self.canvas_comparacion.create_text(x_pos, y_pos + 20, anchor="w", 
                                                   text="↓", font=("Arial", 12), fill="red")
                self.canvas_comparacion.create_text(x_pos + 10, y_pos + 20, anchor="w", 
                                                   text="ELIMINADO", font=("Arial", 8), fill="red")
            else:  # mayuscula
                self.canvas_comparacion.create_text(x_pos, y_pos + 20, anchor="w", 
                                                   text="↓", font=("Arial", 12), fill="blue")
                self.canvas_comparacion.create_text(x_pos + 10, y_pos + 20, anchor="w", 
                                                   text="CONVERTIDO", font=("Arial", 8), fill="blue")
    
    def dibujar_texto_simple(self, texto, y_pos, color):
        """Dibuja texto simple sin iterador"""
        x_offset = 10
        char_width = 15
        
        for i, char in enumerate(texto):
            display_char = '␣' if char == ' ' else char
            self.canvas_comparacion.create_text(x_offset + i * char_width, y_pos, anchor="w", 
                                               text=display_char, font=("Courier", 11), fill=color)
    
    def iniciar_comparacion_visual(self):
        """Inicia la comparación visual paso a paso"""
        self.text_validacion.insert(tk.END, "\n=== PASO 2: COMPARACIÓN VISUAL ===\n\n")
        
        self.frase_a_comparar = self.normalizar_espacios(self.frase_anterior) if self.frase_anterior else ""
        
        palabras = self.nueva_frase.split()
        self.text_validacion.insert(tk.END, f"Nueva frase: '{self.nueva_frase}'\n")
        self.text_validacion.insert(tk.END, f"Número de palabras: {len(palabras)}\n\n")
        
        if not self.frase_a_comparar:
            self.text_validacion.insert(tk.END, "📋 Primera jugada: Cualquier frase es válida\n")
            self.text_validacion.insert(tk.END, "✅ Validación y verificación completadas exitosamente\n")
            self.procesar_palabra_valida(self.nueva_frase)
            return
        
        self.text_validacion.insert(tk.END, f"📋 REGLA: Debe comenzar con la frase anterior completa\n")
        self.text_validacion.insert(tk.END, f"Frase anterior: '{self.frase_a_comparar}'\n")
        self.text_validacion.insert(tk.END, f"Su frase: '{self.nueva_frase}'\n\n")
        
        # IMPORTANTE: No hacer validación previa - permitir comparación paso a paso
        # Preparar comparación visual paso a paso
        self.indice_comparacion = 0
        self.comparacion_activa = True
        self.comparaciones_realizadas = []  # Limpiar historial
        self.btn_siguiente_char.config(state="normal")
        self.btn_iniciar_comparacion.config(state="disabled")
        
        self.text_validacion.insert(tk.END, "🔍 Iniciando verificación caracter por caracter:\n")
        self.text_validacion.insert(tk.END, "Presione 'Siguiente Carácter' para avanzar paso a paso\n")
        self.text_validacion.insert(tk.END, "⚠️  El resultado se mostrará al final - ¡Sin spoilers!\n\n")
        
        self.dibujar_estado_inicial()
    
    def dibujar_estado_inicial(self):
        self.canvas_comparacion.delete("all")
        
        # Título
        self.canvas_comparacion.create_text(10, 10, anchor="w", 
                                           text="Comparación caracter por caracter:", 
                                           font=("Arial", 12, "bold"))
        
        # Dibujar las frases
        y_frase_ant = 40
        y_frase_nueva = 80
        
        self.canvas_comparacion.create_text(10, y_frase_ant - 20, anchor="w", 
                                           text="Frase anterior:", font=("Arial", 10, "bold"))
        
        self.canvas_comparacion.create_text(10, y_frase_nueva - 20, anchor="w", 
                                           text="Nueva frase:", font=("Arial", 10, "bold"))
        
        # Dibujar caracteres de ambas frases
        x_offset = 10
        char_width = 15
        
        # Frase anterior
        for i, char in enumerate(self.frase_a_comparar):
            self.canvas_comparacion.create_text(x_offset + i * char_width, y_frase_ant, anchor="w", 
                                               text=char, font=("Courier", 11), fill="blue")
            # Índice debajo de cada carácter
            self.canvas_comparacion.create_text(x_offset + i * char_width, y_frase_ant + 15, anchor="w", 
                                               text=str(i), font=("Courier", 8), fill="gray")
        
        # Nueva frase
        for i, char in enumerate(self.nueva_frase):
            color = "red" if i < len(self.frase_a_comparar) else "green"
            self.canvas_comparacion.create_text(x_offset + i * char_width, y_frase_nueva, anchor="w", 
                                               text=char, font=("Courier", 11), fill=color)
            # Índice debajo de cada carácter
            self.canvas_comparacion.create_text(x_offset + i * char_width, y_frase_nueva + 15, anchor="w", 
                                               text=str(i), font=("Courier", 8), fill="gray")
        
        # Dibujar iteradores iniciales
        self.dibujar_iteradores()
        
        # Leyenda
        self.canvas_comparacion.create_text(10, 150, anchor="w", 
                                           text="Azul: frase anterior | Rojo: parte a verificar | Verde: nueva parte", 
                                           font=("Arial", 9), fill="black")
        
        self.canvas_comparacion.create_text(10, 170, anchor="w", 
                                           text="↑ Iterador frase anterior | ↓ Iterador nueva frase", 
                                           font=("Arial", 9), fill="black")
    
    def dibujar_iteradores(self):
        # Borrar iteradores anteriores
        self.canvas_comparacion.delete("iterador_ant")
        self.canvas_comparacion.delete("iterador_nuevo")
        
        x_offset = 10
        char_width = 15
        y_frase_ant = 40
        y_frase_nueva = 80
        
        # Iterador de frase anterior (flecha hacia arriba)
        if self.indice_comparacion < len(self.frase_a_comparar):
            x_pos = x_offset + self.indice_comparacion * char_width
            self.canvas_comparacion.create_text(x_pos, y_frase_ant - 35, anchor="w", 
                                               text="↑", font=("Arial", 12), fill="blue", tags="iterador_ant")
            self.canvas_comparacion.create_text(x_pos + 10, y_frase_ant - 35, anchor="w", 
                                               text=f"i={self.indice_comparacion}", 
                                               font=("Arial", 8), fill="blue", tags="iterador_ant")
        else:
            # Mostrar que el iterador se detuvo
            x_pos = x_offset + (len(self.frase_a_comparar) - 1) * char_width if len(self.frase_a_comparar) > 0 else x_offset
            self.canvas_comparacion.create_text(x_pos, y_frase_ant - 35, anchor="w", 
                                               text="⊗", font=("Arial", 12), fill="red", tags="iterador_ant")
            self.canvas_comparacion.create_text(x_pos + 10, y_frase_ant - 35, anchor="w", 
                                               text="FIN", font=("Arial", 8), fill="red", tags="iterador_ant")
        
        # Iterador de nueva frase (flecha hacia abajo)
        if self.indice_comparacion < len(self.nueva_frase):
            x_pos = x_offset + self.indice_comparacion * char_width
            self.canvas_comparacion.create_text(x_pos, y_frase_nueva + 35, anchor="w", 
                                               text="↓", font=("Arial", 12), fill="red", tags="iterador_nuevo")
            self.canvas_comparacion.create_text(x_pos + 10, y_frase_nueva + 35, anchor="w", 
                                               text=f"j={self.indice_comparacion}", 
                                               font=("Arial", 8), fill="red", tags="iterador_nuevo")
        
    def comparar_siguiente_caracter(self):
        if not self.comparacion_activa:
            return
        
        # Verificar si hemos terminado la comparación
        if self.indice_comparacion >= len(self.frase_a_comparar):
            self.finalizar_comparacion()
            return
        
        # Obtener caracteres actuales
        char_ant = self.frase_a_comparar[self.indice_comparacion] if self.indice_comparacion < len(self.frase_a_comparar) else None
        char_nuevo = self.nueva_frase[self.indice_comparacion] if self.indice_comparacion < len(self.nueva_frase) else None
        
        # Validar comparación (sin mostrar resultado)
        if char_ant is not None and char_nuevo is not None:
            # Guardar la comparación sin revelar el resultado
            self.comparaciones_realizadas.append({
                'posicion': self.indice_comparacion,
                'char_ant': char_ant,
                'char_nuevo': char_nuevo,
                'coincide': char_ant == char_nuevo
            })
            
            if char_ant == char_nuevo:
                # Solo mostrar que se está comparando, sin el resultado
                self.text_validacion.insert(tk.END, f"🔍 Comparando posición {self.indice_comparacion}: '{char_ant}' vs '{char_nuevo}' ...\n")
                self.indice_comparacion += 1
            else:
                # Falla inmediata - mostrar error y detener
                self.text_validacion.insert(tk.END, f"🔍 Comparando posición {self.indice_comparacion}: '{char_ant}' vs '{char_nuevo}' ...\n")
                self.mostrar_resultado_final(False)
                return
        elif char_ant is not None and char_nuevo is None:
            self.text_validacion.insert(tk.END, f"🔍 Comparando posición {self.indice_comparacion}: '{char_ant}' vs (fin de frase) ...\n")
            self.mostrar_resultado_final(False)
            return
        
        # Actualizar visualización
        self.dibujar_iteradores()
        
        # Verificar si hemos completado la frase anterior
        if self.indice_comparacion >= len(self.frase_a_comparar):
            self.text_validacion.insert(tk.END, f"\n🎯 Comparación completa: {self.indice_comparacion}/{len(self.frase_a_comparar)} posiciones comparadas\n")
            self.text_validacion.insert(tk.END, "El iterador de la frase anterior se detiene aquí ⊗\n")
            self.mostrar_resultado_final(True)
    
    def mostrar_resultado_final(self, exito):
        """Muestra el resultado completo de la comparación al final"""
        self.text_validacion.insert(tk.END, "\n" + "="*50 + "\n")
        self.text_validacion.insert(tk.END, "           RESULTADO DE LA COMPARACIÓN\n")
        self.text_validacion.insert(tk.END, "="*50 + "\n\n")
        
        # Mostrar todas las comparaciones realizadas
        for comp in self.comparaciones_realizadas:
            if comp['coincide']:
                self.text_validacion.insert(tk.END, f"✅ Posición {comp['posicion']}: '{comp['char_ant']}' = '{comp['char_nuevo']}'\n")
            else:
                self.text_validacion.insert(tk.END, f"❌ Posición {comp['posicion']}: '{comp['char_ant']}' ≠ '{comp['char_nuevo']}'\n")
        
        if exito:
            self.text_validacion.insert(tk.END, f"\n✅ RESULTADO: ÉXITO - Todas las posiciones coinciden\n")
            self.finalizar_comparacion()
        else:
            self.text_validacion.insert(tk.END, f"\n❌ RESULTADO: FALLA - Las frases no coinciden\n")
            
            # Mostrar qué jugador perdió
            self.mostrar_jugador_perdedor()
            
            self.comparacion_activa = False
            self.btn_siguiente_char.config(state="disabled")
    
    def mostrar_jugador_perdedor(self):
        """Calcula y muestra qué jugador perdió basado en las frases dichas"""
        # El jugador que perdió es quien debía decir la frase actual
        jugador_perdedor_num = (self.frases_dichas % self.num_jugadores) + 1
        jugador_perdedor = f"Jugador {jugador_perdedor_num}"
        
        self.text_validacion.insert(tk.END, "\n" + "="*50 + "\n")
        self.text_validacion.insert(tk.END, "           CÁLCULO DEL JUGADOR PERDEDOR\n")
        self.text_validacion.insert(tk.END, "="*50 + "\n\n")
        
        self.text_validacion.insert(tk.END, f"Frases exitosas dichas hasta ahora: {self.frases_dichas}\n")
        self.text_validacion.insert(tk.END, f"Número total de jugadores: {self.num_jugadores}\n\n")
        
        self.text_validacion.insert(tk.END, "Cálculo del turno actual usando módulo:\n")
        self.text_validacion.insert(tk.END, f"turno_actual = frases_dichas % num_jugadores\n")
        self.text_validacion.insert(tk.END, f"turno_actual = {self.frases_dichas} % {self.num_jugadores} = {self.frases_dichas % self.num_jugadores}\n\n")
        
        self.text_validacion.insert(tk.END, "Como los jugadores se numeran desde 1:\n")
        self.text_validacion.insert(tk.END, f"jugador_actual = ({self.frases_dichas} % {self.num_jugadores}) + 1 = {jugador_perdedor_num}\n\n")
        
        self.text_validacion.insert(tk.END, f"🚨 RESULTADO: {jugador_perdedor} PERDIÓ 🚨\n")
        
        # Mostrar mensaje emergente
        messagebox.showerror("🚨 JUEGO TERMINADO 🚨", 
                           f"{jugador_perdedor} ha perdido!\n\n"
                           f"Frases exitosas: {self.frases_dichas}\n"
                           f"Turno calculado: ({self.frases_dichas} % {self.num_jugadores}) + 1 = {jugador_perdedor_num}")
    
    def finalizar_comparacion(self):
        self.comparacion_activa = False
        self.btn_siguiente_char.config(state="disabled")
        
        # Verificar que la nueva frase sea más larga
        if len(self.nueva_frase) > len(self.frase_a_comparar):
            nueva_parte = self.nueva_frase[len(self.frase_a_comparar):]
            self.text_validacion.insert(tk.END, f"\n✅ ÉXITO: Nueva parte agregada: '{nueva_parte}'\n")
            self.procesar_palabra_valida(self.nueva_frase)
        else:
            self.text_validacion.insert(tk.END, "\n❌ ERROR: Debe agregar al menos una palabra más\n")
    
    def reiniciar_validacion(self):
        self.indice_comparacion = 0
        self.comparacion_activa = False
        self.normalizacion_activa = False
        self.indice_normalizacion = 0
        self.texto_siendo_normalizado = ""
        self.cambios_encontrados = []
        self.tipo_cambio_actual = ""
        self.comparaciones_realizadas = []
        self.frase_original = ""
        self.btn_siguiente_char.config(state="disabled")
        self.btn_siguiente_cambio.config(state="disabled")
        self.btn_iniciar_comparacion.config(state="disabled")
        self.canvas_comparacion.delete("all")
        self.text_validacion.delete(1.0, tk.END)
        self.entry_palabra.delete(0, tk.END)
        # Limpiar también el canvas y texto de la etapa 2
        self.canvas_turno.delete("all")
        self.text_turno.delete(1.0, tk.END)
    
    def procesar_palabra_valida(self, frase):
        # Normalizar antes de guardar
        frase_normalizada = self.normalizar_espacios(frase)
        self.frase_anterior = frase_normalizada
        
        # Incrementar contador de frases dichas
        self.frases_dichas += 1
        
        self.text_validacion.insert(tk.END, f"\n🎯 Nueva frase establecida: '{frase_normalizada}'\n")
        self.text_validacion.insert(tk.END, f"📊 Frases exitosas dichas: {self.frases_dichas}\n")
        self.text_validacion.insert(tk.END, "Proceda a la Etapa 2 para calcular el siguiente turno.\n")
        self.actualizar_info()
    
    def calcular_turno(self):
        if self.num_jugadores == 0:
            messagebox.showerror("Error", "Debe iniciar el juego primero")
            return
        
        self.canvas_turno.delete("all")
        self.text_turno.delete(1.0, tk.END)
        self.text_turno.insert(tk.END, "=== ETAPA 2: CÁLCULO DEL SIGUIENTE TURNO ===\n\n")
        
        # Mostrar información actual y cálculo del jugador actual
        jugador_actual_num = (self.frases_dichas % self.num_jugadores) + 1
        self.text_turno.insert(tk.END, f"Frases exitosas dichas: {self.frases_dichas}\n")
        self.text_turno.insert(tk.END, f"Número total de jugadores: {self.num_jugadores}\n\n")
        
        self.text_turno.insert(tk.END, "🎯 CÁLCULO DEL JUGADOR ACTUAL:\n")
        self.text_turno.insert(tk.END, f"¿A quién le toca después de {self.frases_dichas} frases exitosas?\n")
        self.text_turno.insert(tk.END, f"Fórmula: jugador = (frases_dichas % num_jugadores) + 1\n")
        self.text_turno.insert(tk.END, f"Cálculo: jugador = ({self.frases_dichas} % {self.num_jugadores}) + 1 = {jugador_actual_num}\n")
        self.text_turno.insert(tk.END, f"👉 Respuesta: Le toca al Jugador {jugador_actual_num}\n\n")
        
        # Visualización del cálculo del módulo
        y_pos = 20
        self.canvas_turno.create_text(10, y_pos, anchor="w", 
                                     text="Cálculo del siguiente turno usando módulo:", 
                                     font=("Arial", 12, "bold"))
        
        y_pos += 30
        formula = f"siguiente_turno = (frases_dichas % num_jugadores) + 1"
        self.canvas_turno.create_text(10, y_pos, anchor="w", text=formula, 
                                     font=("Courier", 11))
        
        y_pos += 25
        calculo = f"siguiente_turno = ({self.frases_dichas} % {self.num_jugadores}) + 1"
        self.canvas_turno.create_text(10, y_pos, anchor="w", text=calculo, 
                                     font=("Courier", 11), fill="blue")
        
        y_pos += 25
        modulo_resultado = self.frases_dichas % self.num_jugadores
        resultado = f"siguiente_turno = {modulo_resultado} + 1 = {jugador_actual_num}"
        self.canvas_turno.create_text(10, y_pos, anchor="w", text=resultado, 
                                     font=("Courier", 11, "bold"), fill="green")
        
        # Explicación detallada
        self.text_turno.insert(tk.END, "Cálculo paso a paso:\n")
        self.text_turno.insert(tk.END, f"1. Frases exitosas dichas: {self.frases_dichas}\n")
        self.text_turno.insert(tk.END, f"2. Aplicar módulo: {self.frases_dichas} % {self.num_jugadores} = {modulo_resultado}\n")
        self.text_turno.insert(tk.END, f"3. Convertir a número de jugador: {modulo_resultado} + 1 = {jugador_actual_num}\n")
        
        if modulo_resultado == 0:
            self.text_turno.insert(tk.END, f"4. Como el módulo es 0, le toca al último jugador (Jugador {self.num_jugadores})\n")
        else:
            self.text_turno.insert(tk.END, f"4. Le toca al Jugador {jugador_actual_num}\n")
        
        siguiente_jugador = f"Jugador {jugador_actual_num}"
        self.text_turno.insert(tk.END, f"\n🎯 Resultado: Le toca a {siguiente_jugador}\n")
        
        self.actualizar_info()
        self.entry_palabra.delete(0, tk.END)
        
        messagebox.showinfo("Turno Calculado", 
                           f"Siguiente turno: {siguiente_jugador}\n"
                           f"Frases exitosas: {self.frases_dichas}")

def main():
    root = tk.Tk()
    app = FraseInterminableVisual(root)
    root.mainloop()

if __name__ == "__main__":
    main()