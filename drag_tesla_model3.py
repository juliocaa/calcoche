"""Calculo de la resistencia aerodinamica de un Tesla Model 3 en funcion de la velocidad"""

import argparse

# Constantes
# Coeficiente de arrastre (Cd) aproximado del Tesla Model 3
DRAG_COEFFICIENT = 0.23
# Area frontal aproximada en metros cuadrados
FRONTAL_AREA = 2.22
# Densidad del aire a nivel del mar en kg/m^3
AIR_DENSITY = 1.225

def drag_force(velocity_kmh: float, cd: float = DRAG_COEFFICIENT,
               area: float = FRONTAL_AREA, rho: float = AIR_DENSITY) -> float:
    """Calcula la fuerza de resistencia aerodinamica.

    Parameters
    ----------
    velocity_kmh : float
        Velocidad en kilometros por hora.
    cd : float
        Coeficiente de arrastre (Cd).
    area : float
        Area frontal en metros cuadrados.
    rho : float
        Densidad del aire en kg/m^3.

    Returns
    -------
    float
        Fuerza de resistencia en Newtons.
    """
    velocity_ms = velocity_kmh / 3.6  # Conversion de km/h a m/s
    return 0.5 * cd * area * rho * velocity_ms ** 2

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula la resistencia aerodinamica de un Tesla Model 3")
    parser.add_argument(
        "velocidad",
        type=float,
        help="Velocidad en km/h")
    args = parser.parse_args()
    force = drag_force(args.velocidad)
    print(
        f"Resistencia aerodinamica a {args.velocidad} km/h: {force:.2f} N")

if __name__ == "__main__":
    main()
