from models.materia import Materia
from controllers.generador import GeneradorHorarios

def probar_generador():
    """Prueba el generador de horarios"""
    
    print("\n" + "="*80)
    print("GENERADOR DE HORARIOS - PRUEBA")
    print("="*80 + "\n")
    
    # 1. Seleccionar semestre y obtener materias
    semestre = 1
    turno = 'Matutino'
    
    print(f"Obteniendo materias del semestre {semestre}...")
    materias = Materia.obtenerPorSemestre(semestre)
    
    if not materias:
        print("No hay materias en ese semestre")
        return
    
    print(f"Materias disponibles:")
    for i, mat in enumerate(materias, 1):
        print(f"  {i}. {mat}")
    
    # 2. Seleccionar las primeras 3 materias (o las que haya)
    materias_seleccionadas = materias[:min(3, len(materias))]
    ids_materias = [mat.id_materia for mat in materias_seleccionadas]
    
    print(f"\nMaterias seleccionadas para generar horarios:")
    for mat in materias_seleccionadas:
        print(f"  - {mat}")
    
    # 3. Generar horarios
    print(f"\nGenerando opciones de horarios para turno {turno}...\n")
    
    generador = GeneradorHorarios()
    horarios_validos = generador.generar(ids_materias, turno, limite=5)
    
    # 4. Mostrar resultados
    if horarios_validos:
        print(f"\nSe generaron {len(horarios_validos)} opciones válidas\n")
        
        # Mostrar las primeras 2 opciones detalladamente
        for i, opcion in enumerate(horarios_validos[:2], 1):
            print(f"\n{'='*80}")
            print(f"OPCIÓN {i}")
            print('='*80)
            
            # Resumen general
            print(generador.obtenerResumenHorario(opcion))
            
            # Vista por días
            generador.imprimirHorarioDia(opcion)
            
            input("Presiona Enter para ver la siguiente opción...")
    else:
        print("\nNo se encontraron horarios válidos")
        print("   Posibles causas:")
        print("   - No hay suficientes grupos disponibles")
        print("   - Todos los horarios tienen conflictos")
        print("   - Revisa que haya datos en la tabla 'grupos' y 'horarios_grupo'")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    probar_generador()