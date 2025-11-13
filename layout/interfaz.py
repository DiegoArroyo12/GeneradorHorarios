import tkinter as tk
from tkinter import ttk, messagebox
from models.materia import Materia
from controllers.generador import GeneradorHorarios

class GeneradorHorariosGUI:
    """Interfaz gráfica para el generador de horarios"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Horarios - ICO")
        
        # Maximizar ventana
        self.root.state('zoomed')
        
        self.root.resizable(True, True)
        
        # Variables
        self.materias_disponibles = []
        self.materias_optativas = []
        self.materias_seleccionadas = []
        self.horarios_generados = []
        self.indice_actual = 0
        self.generador = GeneradorHorarios()
        
        # Estilos
        self.configurarEstilos()
        
        # Crear interfaz
        self.crearInterfaz()
        
    def configurarEstilos(self):
        """Configura los estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Treeview (tabla)
        style.configure("Treeview",
                       foreground="white",
                       rowheight=60,
                       fieldbackground="white",
                       font=('Arial', 11))
        
        style.configure("Treeview.Heading",
                       font=('Arial', 12, 'bold'),
                       background='#2D5BA5',
                       foreground='white',
                       relief='flat')
        
        style.map('Treeview.Heading',
                 background=[('active', '#2D5BA5')])
        
        style.configure("Treeview", rowheight=70)
        
    def crearInterfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # ===== ENCABEZADO =====
        frame_header = tk.Frame(self.root, padx=20, pady=20)
        frame_header.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(frame_header, text="GENERADOR DE HORARIOS", 
                font=('Arial', 28, 'bold'), fg='white').pack()
        
        tk.Label(frame_header, text="Ingeniería en Computación", 
                font=('Arial', 14), fg='white').pack()
        
        # ===== FRAME SUPERIOR: CONFIGURACIÓN Y MATERIAS =====
        frame_superior = tk.Frame(self.root)
        frame_superior.pack(side=tk.TOP, fill=tk.BOTH, padx=15, pady=15)
        
        # COLUMNA IZQUIERDA: Configuración
        frame_config = tk.LabelFrame(frame_superior, text=" Configuración ", 
                                     font=('Arial', 13, 'bold'), padx=20, pady=15)
        frame_config.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Semestre
        frame_semestre = tk.Frame(frame_config)
        frame_semestre.pack(fill=tk.X, pady=8)
        
        tk.Label(frame_semestre, text="Semestre:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.combo_semestre = ttk.Combobox(frame_semestre, values=list(range(1, 10)), 
                                          state='readonly', width=12, font=('Arial', 12))
        self.combo_semestre.pack(side=tk.LEFT)
        self.combo_semestre.current(0)
        self.combo_semestre.bind('<<ComboboxSelected>>', self.cargarMaterias)
        
        # Turno
        frame_turno = tk.Frame(frame_config)
        frame_turno.pack(fill=tk.X, pady=8)
        
        tk.Label(frame_turno, text="Turno:", font=('Arial', 12), 
            ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.var_turno = tk.StringVar(value='Ambos')
        
        tk.Radiobutton(frame_turno, text="Matutino", variable=self.var_turno, 
                      value='Matutino', font=('Arial', 11),
                      activebackground='#ecf0f1').pack(side=tk.LEFT, padx=8)
        tk.Radiobutton(frame_turno, text="Vespertino", variable=self.var_turno, 
                      value='Vespertino', font=('Arial', 11),
                      activebackground='#ecf0f1').pack(side=tk.LEFT, padx=8)
        tk.Radiobutton(frame_turno, text="Ambos", variable=self.var_turno, 
                      value='Ambos', font=('Arial', 11),
                      activebackground='#ecf0f1').pack(side=tk.LEFT, padx=8)
        
        # Margen de error
        frame_margen = tk.Frame(frame_config)
        frame_margen.pack(fill=tk.X, pady=8)
        
        tk.Label(frame_margen, text="Margen de error (min):", 
                font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.spinbox_margen = tk.Spinbox(frame_margen, from_=0, to=30, width=8, 
                                        font=('Arial', 12))
        self.spinbox_margen.pack(side=tk.LEFT)
        
        # Límite de opciones
        frame_limite = tk.Frame(frame_config)
        frame_limite.pack(fill=tk.X, pady=8)
        
        tk.Label(frame_limite, text="Límite de opciones:", 
                font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.spinbox_limite = tk.Spinbox(frame_limite, from_=5, to=50, width=8, 
                                        font=('Arial', 12))
        self.spinbox_limite.delete(0, tk.END)
        self.spinbox_limite.insert(0, "20")
        self.spinbox_limite.pack(side=tk.LEFT)
        
        # COLUMNA DERECHA: Materias
        frame_materias = tk.LabelFrame(frame_superior, text=" Materias ", 
                                      font=('Arial', 13, 'bold'), padx=20, pady=15)
        frame_materias.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Botón cargar materias
        tk.Button(frame_materias, text="Cargar Materias", command=self.cargarMaterias, font=('Arial', 12, 'bold'),
                 padx=20, pady=8, relief=tk.FLAT, cursor='hand2').pack(fill=tk.X, pady=(0, 10))
        
        # Frame con scroll para materias
        frame_scroll = tk.Frame(frame_materias)
        frame_scroll.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas_materias = tk.Canvas(frame_scroll, yscrollcommand=scrollbar.set, highlightthickness=0)
        self.canvas_materias.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas_materias.yview)
        
        self.frame_lista_materias = tk.Frame(self.canvas_materias)
        self.canvas_materias.create_window((0, 0), window=self.frame_lista_materias, anchor='nw')
        
        self.frame_lista_materias.bind('<Configure>', 
                                      lambda e: self.canvas_materias.configure(
                                          scrollregion=self.canvas_materias.bbox('all')))
        
        # Label de contador
        self.label_contador = tk.Label(frame_materias, text="Materias seleccionadas: 0",
                                       font=('Arial', 11, 'italic'), fg='#7f8c8d')
        self.label_contador.pack(pady=(8, 0))
        
        # Botón generar (más grande y destacado)
        frame_btn_generar = tk.Frame(frame_superior)
        frame_btn_generar.pack(side=tk.LEFT, fill=tk.Y, padx=(15, 0))
        
        tk.Button(frame_btn_generar, text="GENERAR\nHORARIOS",
                 command=self.generarHorarios, font=('Arial', 14, 'bold'),
                 padx=15, pady=15, relief=tk.FLAT, cursor='hand2').pack(expand=True)
        
        # ===== FRAME INFERIOR: TABLA DE HORARIOS =====
        frame_inferior = tk.Frame(self.root)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Navegación superior
        frame_nav_superior = tk.Frame(frame_inferior, padx=15, pady=12)
        frame_nav_superior.pack(fill=tk.X)
        
        self.label_info_horario = tk.Label(frame_nav_superior, 
                                           text="Genera horarios para ver resultados",
                                           font=('Arial', 13, 'bold'), fg='white')
        self.label_info_horario.pack(side=tk.LEFT)
        
        # Controles de navegación
        frame_controles = tk.Frame(frame_nav_superior)
        frame_controles.pack(side=tk.RIGHT)
        
        self.btn_anterior = tk.Button(frame_controles, text="Anterior", 
                                      command=self.horarioAnterior,
                                      state=tk.DISABLED, font=('Arial', 11, 'bold'),
                                      padx=20, pady=6,
                                      relief=tk.FLAT, cursor='hand2')
        self.btn_anterior.pack(side=tk.LEFT, padx=5)
        
        self.label_navegacion = tk.Label(frame_controles, text="0 / 0",
                                         font=('Arial', 12, 'bold'), fg='white', padx=15)
        self.label_navegacion.pack(side=tk.LEFT)
        
        self.btn_siguiente = tk.Button(frame_controles, text="Siguiente", 
                                       command=self.horarioSiguiente,
                                       state=tk.DISABLED, font=('Arial', 11, 'bold'),
                                       padx=20, pady=6,
                                       relief=tk.FLAT, cursor='hand2')
        self.btn_siguiente.pack(side=tk.LEFT, padx=5)
        
        self.btn_exportar = tk.Button(frame_controles, text="Exportar PDF", 
                                      command=self.exportarPDF,
                                      state=tk.DISABLED,
                                      font=('Arial', 11, 'bold'), padx=20, pady=6,
                                      relief=tk.FLAT, cursor='hand2')
        self.btn_exportar.pack(side=tk.LEFT, padx=(15, 0))
        
        # Frame para la tabla
        frame_tabla = tk.Frame(frame_inferior, relief=tk.SOLID, borderwidth=1)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        # Crear Treeview (tabla)
        columnas = ('materia', 'grupo', 'profesor', 'lunes', 'martes', 
                   'miercoles', 'jueves', 'viernes', 'sabado')
        
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('materia', text='Materia')
        self.tree.heading('grupo', text='Grupo')
        self.tree.heading('profesor', text='Profesor')
        self.tree.heading('lunes', text='Lunes')
        self.tree.heading('martes', text='Martes')
        self.tree.heading('miercoles', text='Miércoles')
        self.tree.heading('jueves', text='Jueves')
        self.tree.heading('viernes', text='Viernes')
        self.tree.heading('sabado', text='Sábado')
        
        # Anchos de columnas
        self.tree.column('materia', width=250, anchor='w')
        self.tree.column('grupo', width=80, anchor='center')
        self.tree.column('profesor', width=200, anchor='w')
        self.tree.column('lunes', width=150, anchor='center')
        self.tree.column('martes', width=150, anchor='center')
        self.tree.column('miercoles', width=150, anchor='center')
        self.tree.column('jueves', width=150, anchor='center')
        self.tree.column('viernes', width=150, anchor='center')
        self.tree.column('sabado', width=150, anchor='center')
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Empaquetar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tags para colores alternados
        self.tree.tag_configure('oddrow', background="#2D5BA5")
        self.tree.tag_configure('evenrow', background="#2D83A5")
        
    def cargarMaterias(self, event=None):
        """Carga las materias del semestre seleccionado"""
        
        # Limpiar lista anterior
        for widget in self.frame_lista_materias.winfo_children():
            widget.destroy()
        
        self.materias_disponibles = []
        self.materias_optativas = []
        self.materias_seleccionadas = []
        
        # Obtener semestre
        semestre = int(self.combo_semestre.get())
        
        # Cargar materias
        if semestre >= 6:
            materias_dict = Materia.obtenerSemestreOptativa(semestre)
            self.materias_disponibles = materias_dict['regulares']
            self.materias_optativas = materias_dict['optativas']
        else:
            self.materias_disponibles = Materia.obtenerPorSemestre(semestre)
        
        # Mostrar materias regulares
        if self.materias_disponibles:
            tk.Label(self.frame_lista_materias, text="MATERIAS REGULARES",
                    font=('Arial', 11, 'bold'), bg="#399d34",
                    pady=5).pack(fill=tk.X, pady=(0, 5))
            
            for materia in self.materias_disponibles:
                var = tk.BooleanVar()
                
                cb = tk.Checkbutton(self.frame_lista_materias, 
                                   text=f"{materia.clave} - {materia.nombre}",
                                   variable=var, font=('Arial', 11),
                                   command=self.actualizarContador,
                                   fg='white',
                                   cursor='hand2')
                cb.pack(anchor='w', padx=15, pady=3)
                
                cb.materia = materia
                cb.var = var
        
        # Mostrar optativas
        if self.materias_optativas:
            tk.Label(self.frame_lista_materias, text="MATERIAS OPTATIVAS",
                    font=('Arial', 11, 'bold'), bg="#1a564a",
                    pady=5).pack(fill=tk.X, pady=(10, 5))
            
            for materia in self.materias_optativas:
                var = tk.BooleanVar()
                
                cb = tk.Checkbutton(self.frame_lista_materias, 
                                   text=f"[OPT] {materia.clave} - {materia.nombre}",
                                   variable=var, font=('Arial', 11),
                                   command=self.actualizarContador,
                                   fg='white',
                                   cursor='hand2')
                cb.pack(anchor='w', padx=15, pady=3)
                
                cb.materia = materia
                cb.var = var
        
        if not self.materias_disponibles and not self.materias_optativas:
            tk.Label(self.frame_lista_materias, text="No hay materias disponibles",
                    font=('Arial', 11), fg='red', bg='white').pack(pady=20)
        
        self.actualizarContador()
        
    def actualizarContador(self):
        """Actualiza el contador de materias seleccionadas"""
        count = 0
        
        for widget in self.frame_lista_materias.winfo_children():
            if isinstance(widget, tk.Checkbutton) and widget.var.get():
                count += 1
        
        self.label_contador.config(text=f"Materias seleccionadas: {count}")
        
    def obtenerMateriasSeleccionadas(self):
        """Obtiene las IDs de las materias seleccionadas"""
        ids = []
        
        for widget in self.frame_lista_materias.winfo_children():
            if isinstance(widget, tk.Checkbutton) and widget.var.get():
                ids.append(widget.materia.id_materia)
        
        return ids
    
    def generarHorarios(self):
        """Genera los horarios según la configuración"""
        
        # Validar materias seleccionadas
        ids_materias = self.obtenerMateriasSeleccionadas()
        
        if not ids_materias:
            messagebox.showwarning("Sin materias", 
                                  "Debes seleccionar al menos una materia")
            return
        
        if len(ids_materias) > 7:
            respuesta = messagebox.askyesno("Advertencia", 
                                           "Has seleccionado más de 7 materias.\n" +
                                           "Esto puede tomar mucho tiempo.\n" +
                                           "Incluso puede no haber solución válida.\n\n" +
                                           "¿Deseas continuar?")
            if not respuesta:
                return
        
        # Obtener configuración
        turno = self.var_turno.get()
        margen = int(self.spinbox_margen.get())
        limite = int(self.spinbox_limite.get())
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.label_info_horario.config(text="Generando horarios, espera un momento...",
                                       fg='#f39c12')
        self.root.update()
        
        # Generar
        try:
            self.horarios_generados = self.generador.generar(
                ids_materias, 
                turno, 
                limite=limite,
                margen_error=margen
            )
            
            if self.horarios_generados:
                self.indice_actual = 0
                self.mostrarHorarioActual()
                self.actualizarNavegacion()
                
                # Habilitar botones
                self.btn_exportar.config(state=tk.NORMAL)
                
                # Mensaje de éxito
                sin_conflictos = len([h for h in self.horarios_generados if not h['tiene_advertencia']])
                con_conflictos = len(self.horarios_generados) - sin_conflictos
                
                mensaje = f"Se generaron {len(self.horarios_generados)} opciones\n\n"
                mensaje += f"• Sin conflictos: {sin_conflictos}\n"
                if con_conflictos > 0:
                    mensaje += f"• Con traslape permitido: {con_conflictos}"
                
                messagebox.showinfo("Éxito", mensaje)
            else:
                self.label_info_horario.config(text="No se encontraron horarios válidos",
                                              fg='#e74c3c')
                
                messagebox.showwarning("Sin resultados", 
                                      "No se pudieron generar horarios válidos.\n\n" +
                                      "Intenta:\n" +
                                      "• Aumentar el margen de error\n" +
                                      "• Seleccionar 'Ambos' turnos\n" +
                                      "• Reducir el número de materias")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
    
    def mostrarHorarioActual(self):
        """Muestra el horario en el índice actual en la tabla"""
        
        if not self.horarios_generados:
            return
        
        opcion = self.horarios_generados[self.indice_actual]
        
        # Actualizar info
        tiene_advertencia = opcion['tiene_advertencia']
        minutos = opcion['minutos_empalme']
        
        if tiene_advertencia:
            texto_info = f"Opción {self.indice_actual + 1} de {len(self.horarios_generados)} - Traslape de {minutos} min"
            color_info = '#e67e22'
        else:
            texto_info = f"Opción {self.indice_actual + 1} de {len(self.horarios_generados)} - Sin conflictos"
            color_info = '#27ae60'
        
        self.label_info_horario.config(text=texto_info, fg=color_info)
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener datos del horario
        combinacion = opcion['combinacion']
        
        # Organizar por materia
        for idx, grupo in enumerate(combinacion):
            # Obtener horarios detallados
            horarios = self.generador.generador.obtenerHorariosDetallados(grupo.id_grupo) if hasattr(self.generador, 'generador') else []
            
            # Si no funciona el método anterior, usar el del modelo
            from models.grupo import Grupo
            horarios = Grupo.obtenerHorariosDetallados(grupo.id_grupo)
            
            # Organizar por día
            dias_info = {
                'Lunes': '',
                'Martes': '',
                'Miércoles': '',
                'Jueves': '',
                'Viernes': '',
                'Sábado': ''
            }
            
            for h in horarios:
                dia = h['dia_semana']
                hora_inicio = str(h['hora_inicio'])[:5] if hasattr(h['hora_inicio'], 'total_seconds') else h['hora_inicio']
                hora_fin = str(h['hora_fin'])[:5] if hasattr(h['hora_fin'], 'total_seconds') else h['hora_fin']
                
                info_dia = f"{hora_inicio}-{hora_fin}\n{grupo.salon}"
                dias_info[dia] = info_dia
            
            # Formatear materia y profesor
            materia_texto = f"{grupo.materia['clave']}\n{grupo.materia['nombre']}"
            
            # Obtener correo del profesor
            from models.profesor import Profesor
            profesor_obj = Profesor.obtenerPorId(grupo.id_profesor)
            profesor_texto = grupo.profesor
            if profesor_obj and profesor_obj.correo:
                profesor_texto += f"\n{profesor_obj.correo}"
            
            # Insertar en la tabla
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            
            self.tree.insert('', 'end', values=(
                materia_texto,
                grupo.grupo,
                profesor_texto,
                dias_info['Lunes'],
                dias_info['Martes'],
                dias_info['Miércoles'],
                dias_info['Jueves'],
                dias_info['Viernes'],
                dias_info['Sábado']
            ), tags=(tag,))
    
    def actualizarNavegacion(self):
        """Actualiza los botones de navegación"""
        
        total = len(self.horarios_generados)
        
        if total == 0:
            self.btn_anterior.config(state=tk.DISABLED)
            self.btn_siguiente.config(state=tk.DISABLED)
            self.label_navegacion.config(text="0 / 0")
            return
        
        self.label_navegacion.config(text=f"{self.indice_actual + 1} / {total}")
        
        # Botón anterior
        if self.indice_actual > 0:
            self.btn_anterior.config(state=tk.NORMAL)
        else:
            self.btn_anterior.config(state=tk.DISABLED)
        
        # Botón siguiente
        if self.indice_actual < total - 1:
            self.btn_siguiente.config(state=tk.NORMAL)
        else:
            self.btn_siguiente.config(state=tk.DISABLED)
    
    def horarioAnterior(self):
        """Muestra el horario anterior"""
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrarHorarioActual()
            self.actualizarNavegacion()
    
    def horarioSiguiente(self):
        """Muestra el siguiente horario"""
        if self.indice_actual < len(self.horarios_generados) - 1:
            self.indice_actual += 1
            self.mostrarHorarioActual()
            self.actualizarNavegacion()
    
    def exportarPDF(self):
        """Exporta el horario actual a PDF"""
        messagebox.showinfo("Próximamente", "La funcionalidad de exportar a PDF aún no está disponible")