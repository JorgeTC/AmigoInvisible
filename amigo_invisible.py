from random import shuffle

# Los miembros de una misma casa están en una misma lista.
# No queremos que dos miembros de la misma casa se regalen
participantes = [['jose', 'rosa'], ['pepa'], ['jul', 'cris'], ['raul'],
                 ['nuria', 'jesus', 'celia', 'clara', 'mariana'],
                 ['luis', 'maribel', 'marta'], ['jorge', 'sasha']]


def calcular_restricciones(regaladores: list[list[str]]) -> dict[str, set[str]]:
    restricciones = dict()
    for casa in regaladores:
        for regalador in casa:
            restricciones[regalador] = {*casa}
    return restricciones


def restriccion_mutua(restricciones: dict[str, set[str]], participante1, participante2):
    restricciones[participante1].add(participante2)
    restricciones[participante2].add(participante1)


restricciones = calcular_restricciones(participantes)
participantes = [item for sublist in participantes for item in sublist]


def print_solution(sol: dict[str, str]):
    reagaladores_escritos = set()
    for regalador, regalado in sol.items():
        if regalador in reagaladores_escritos:
            continue
        siguiente_regalador = regalado
        mensaje = f"A {regalador} le ha tocado {regalado}"
        while siguiente_regalador != regalador:
            siguiente_regalado = sol[siguiente_regalador]
            mensaje += f"\nA {siguiente_regalador} le ha tocado {siguiente_regalado}"
            siguiente_regalador = siguiente_regalado
            reagaladores_escritos.add(siguiente_regalador)
        print(mensaje)


def sorteo(regaladores: list[str], regalados: list[str], resultado: dict[str, str]):

    # Caso base, todos los participantes tienen a quién regalar
    if not regaladores:
        return True

    # Vamos a intentar asignar un regalado al primer regalador de la lista
    regalador = regaladores[0]
    # Lista con las personas que aún no tienen a quién regalar
    regaladores_restantes = regaladores[1:]

    # Añado aleatoriedad al iterar los posibles regalados
    shuffle(regalados)

    # Itero todas las personas que aún no tienen quien les regale
    for regalado in regalados:

        # Si la persona actual no puede ser regalada por el regalador, paso a la siguiente
        if regalado in restricciones[regalador]:
            continue

        # Lista con las personas que aún no tienen quien les regale
        regalados_restantes = [reg for reg in regalados if reg != regalado]

        # Añado a la solución la asignación actual
        resultado[regalador] = regalado
        # De forma recursiva llamo a la función para que me diga si la asignación me da una situación resoluble
        if sorteo(regaladores_restantes, regalados_restantes, resultado):
            # La asignación es correcta, salgo de la función
            return True
        else:
            # La asignación no es correcta, la elimino e intento asignarle otro regalado
            del resultado[regalador]

    # Ninguna de las personas que quedan por regalar pueden ser regaladas por el regalador actual
    return False


def main():
    resultado: dict[str, str] = dict()
    sorteo(participantes, participantes.copy(), resultado)
    print_solution(resultado)


if __name__ == '__main__':
    main()

