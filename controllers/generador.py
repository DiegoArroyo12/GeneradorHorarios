from itertools import product
from models.grupo import Grupo
from datetime import datetime, timedelta

class GeneradorHorarios:
    """Clase para generar combinaciones de hotarios sin conflictos"""
    
    def __init__(self):
        self.materiasSeleccionadas = []
        self.turno = None
        self.opcionesMateria = {}
        self.horariosGenerados = []
        
    def generar(self, ids_materias, turno, limite=20):
        """
        Genera horarios válidos sin conflictos
        
        Args:
            ids_materias (list): Lista de IDs de materias seleccionadas
            turno (str): 'Matutino'o 'Vespertino'
            limite (int): Número máximo de opciones a devolver
            
        Returns: 
            list: Lista de combinaciones válidas de grupos
        """
        
        self.materiasSeleccionadas = ids_materias
        self.turno = turno
        self.horariosGenerados = []
        
        print(f"Generando horarios para {len(ids_materias)} materias...")
        
        # Grupos disponibles por materia
        self.opcionesMateria = {}
        
        for id_materia in ids_materias:
            grupos = Grupo.obtenerGruposPorMateriaTurno(id_materia, turno)
            
            if not grupos:
                print(f"No hay grupos disponibles para la materia ID {id_materia}")
                return []
            
            self.opcionesMateria[id_materia] = grupos
            print(f"Materia {id_materia}: {len(grupos)} grupo(s) disponible(s)")
        
        # Generar combinaciones posibles
        combinaciones = self._generarCombinaciones()
        print(f"Total de combinaciones posibles {len(combinaciones)}")
        
        # Filtrar solo las válidas (sin conflictos)
        horariosValidos = []
        
        for i, combinacion in enumerate(combinaciones, 1):
            if not self._tieneConflictos(combinacion):
                horariosValidos.append(combinacion)
                
                # Limitar el número de opciones
                if len(horariosValidos) >= limite: break

        print(f"Horarios válidos encontrados: {len(horariosValidos)}")
        
        self.horariosGenerados = horariosValidos
        return horariosValidos
    
    def _generarCombinaciones(self):
        """
        Genera todas las combinaciones posibles usando producto cartesiano
        
        Return: 
            list: Lista de tuplas, cada una es una combinación de grupos
        """
        
        # Listas de grupos por materia en orden
        listasGrupos = [
            self.opcionesMateria[id_materia] for id_materia in self.materiasSeleccionadas
        ]
        
        # Producto cartesiano: todas las posibles combinaciones
        combinaciones = list(product(*listasGrupos))
        
        return combinaciones
    
    def _tieneConflictos(self, combinacion):
        """
        Verifica si una combinación de grupos tiene conflictos de horario
        
        Args:
            combinacion (tuple): Tupla de objetos Grupo
            
        Return:
            bool: True si hay conflictos, False si es válida
        """
        
        # Comparar cada grupo con los demás
        for i, grupo1 in enumerate(combinacion):
            for grupo2 in combinacion[i + 1:]:
                if self._gruposEmpalman(grupo1, grupo2): return True

        return False
    
    def _gruposEmpalman(self, grupo1, grupo2):
        """
        Verifica si dos grupos tienen conflicto de horario
        
        Args:
            grupo1, grupo2: Objetos Grupo a comparar
            
        Returns:
            bool: True si se empalman, False si no
        """
        
        # Obtener horarios detallados (dia por dia) de ambos grupos
        horarios1 = Grupo.obtenerHorariosDetallados(grupo1.id_grupo)
        horarios2 = Grupo.obtenerHorariosDetallados(grupo2.id_grupo)
        
        # Comparar cada horario de grupo 1 con cada horario de grupo 2
        for h1 in horarios1:
            for h2 in horarios2:
                if h1['dia_semana'] == h2['dia_semana']:
                    if self._horasEmpalmadas(
                        h1['hora_inicio'], h1['hora_fin'],
                        h2['hora_inicio'], h2['hora_fin']
                    ): return True
                    
        return False
    
    def _horasEmpalmadas(self, inicio1, fin1, inicio2, fin2):
        """
        Verifica si dos rangos de tiempo se empalman
        
        Args:
            inicio1, fin1: timedelta - Horario del primer grupo
            inicio2, fin2: timedelta - Horario del segundo grupo
            
        Returns:
            bool: True si se empalman, False si no
        """
        
        # Convertir timedelta a minutos para facilitar la comparación
        inicio1_mins = inicio1.total_seconds() / 60
        fin1_mins = fin1.total_seconds() / 60
        inicio2_mins = inicio2.total_seconds() / 60
        fin2_mins = fin2.total_seconds() / 60
        
        # Dos rangos se empalman si:
        # - El inicio de uno está entre el inicio y fin del otro, O
        # - El fin de uno está entre el inicio y fin del otro, O
        # - Uno contiene completamente al otro
        
        empalman = (
            (inicio1_mins < fin2_mins and fin1_mins > inicio2_mins) or
            (inicio2_mins < fin1_mins and fin2_mins > inicio1_mins)
        )
        
        return empalman
    
    def obtenerResumenHorario(self, combinacion):
        """
        Genera un resumen legible de una combinación de grupos
        
        Args:
            combinacion (tuple): Tupla de objetos Grupo
            
        Returns:
            str: texto formateado con el horario completo
        """
        
        resumen = ""
        resumen += "="*60 + "\n"
        resumen += "OPCIÓN DE HORARIO\n"
        resumen += "="*60 + "\n\n"
        
        for grupo in combinacion:
            resumen += f"{grupo.materia['clave']} - {grupo.materia['nombre']}\n"
            resumen += f"   Profesor: {grupo.profesor}\n"
            resumen += f"   Salón: {grupo.salon}\n"
            resumen += f"   Grupo: {grupo.grupo}\n"
            
            for horario in grupo.horarios:
                resumen += f"   {horario['dias']} | {horario['hora_inicio']} - {horario['hora_fin']}\n"
            
            resumen += "\n"
        
        resumen += "="*60 + "\n"
        
        return resumen
    
    def obtenerHorarioDia(self, combinacion):
        """
        Organiza un horario por días de la semana
        
        Args:
            combinacion (tuple): Tupla de objetos Grupo
            
        Returns:
            dict: Diccionario con días como llaves y lista de clases como valores
        """
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        horario_por_dia = {dia: [] for dia in dias_semana}
        
        for grupo in combinacion:
            # Obtener horarios detallados (día por día)
            horarios = Grupo.obtenerHorariosDetallados(grupo.id_grupo)
            
            for horario in horarios:
                dia = horario['dia_semana']
                
                clase_info = {
                    'materia': f"{grupo.materia['clave']} - {grupo.materia['nombre']}",
                    'profesor': grupo.profesor,
                    'salon': grupo.salon,
                    'grupo': grupo.grupo,
                    'hora_inicio': horario['hora_inicio'],
                    'hora_fin': horario['hora_fin']
                }
                
                horario_por_dia[dia].append(clase_info)
        
        # Ordenar cada día por hora de inicio
        for dia in dias_semana:
            horario_por_dia[dia].sort(key=lambda x: x['hora_inicio'])
        
        return horario_por_dia
    
    def imprimirHorarioDia(self, combinacion):
        """
        Imprime un horario organizado por días (vista de tabla)
        
        Args:
            combinacion (tuple): Tupla de objetos Grupo
        """
        horario = self.obtenerHorarioDia(combinacion)
        
        print("\n" + "="*80)
        print("HORARIO SEMANAL")
        print("="*80 + "\n")
        
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        
        for dia in dias_semana:
            clases = horario[dia]
            
            if clases:
                print(f"{dia.upper()}")
                print("-" * 80)
                
                for clase in clases:
                    print(f"  {clase['hora_inicio']} - {clase['hora_fin']} | {clase['materia']}")
                    print(f"    {clase['profesor']} | {clase['salon']} | Grupo {clase['grupo']}")
                    print()
            else:
                print(f"{dia.upper()}")
                print("-" * 80)
                print("  Sin clases\n")
        
        print("="*80 + "\n")