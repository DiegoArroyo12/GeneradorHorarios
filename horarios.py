from models.materia import Materia
from models.grupo import Grupo

def probar_conexion():
    """Prueba las conexiones y modelos"""
    
    print("\n" + "="*50)
    print("PROBANDO MODELOS Y CONEXIÓN")
    print("="*50 + "\n")
    
    # 1. Obtener materias del semestre 1
    print("Materias del semestre 1:")
    materias = Materia.obtenerPorSemestre(1)
    
    if materias:
        for mat in materias:
            print(f"  - {mat}")
    else:
        print("  No hay materias registradas")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. Si hay materias, obtener grupos de la primera
    if materias:
        materia_ejemplo = materias[0]
        print(f"Grupos de '{materia_ejemplo.nombre}' en turno Matutino:")
        
        grupos = Grupo.obtenerGruposPorMateriaTurno(
            materia_ejemplo.id_materia, 
            'Matutino'
        )
        
        if grupos:
            for grupo in grupos:
                print(f"\n  Grupo {grupo.grupo}:")
                print(f"  Profesor: {grupo.profesor}")
                print(f"  Salón: {grupo.salon}")
                for horario in grupo.horarios:
                    print(f"  {horario['dias']} {horario['hora_inicio']} - {horario['hora_fin']}")
        else:
            print("  No hay grupos disponibles")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    probar_conexion()