"""Simulación sencilla de una célula pensada para ejecutarse en un celular.

La simulación modela una célula con tres estados básicos:
- Energía (ATP disponible)
- Hidratación
- Salud de membrana

Cada ciclo representa una "hora" de actividad y consume recursos.
Se incluyen eventos aleatorios para hacer la dinámica más realista.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
import time


@dataclass
class Celula:
    energia: float = 100.0
    hidratacion: float = 100.0
    membrana: float = 100.0
    ciclo: int = 0
    historial: list[str] = field(default_factory=list)

    def viva(self) -> bool:
        return self.energia > 0 and self.hidratacion > 0 and self.membrana > 0

    def _limitar(self) -> None:
        self.energia = max(0.0, min(100.0, self.energia))
        self.hidratacion = max(0.0, min(100.0, self.hidratacion))
        self.membrana = max(0.0, min(100.0, self.membrana))

    def metabolizar(self) -> None:
        """Consume recursos base por ciclo."""
        self.ciclo += 1
        self.energia -= random.uniform(6.0, 12.0)
        self.hidratacion -= random.uniform(4.0, 9.0)
        self.membrana -= random.uniform(1.0, 4.0)

    def aplicar_evento(self) -> str:
        """Aplica un evento aleatorio (estrés o recuperación)."""
        evento = random.choice(
            [
                "mitocondria_eficiente",
                "entrada_de_nutrientes",
                "estres_oxidativo",
                "reparacion_membrana",
                "deshidratacion",
                "sin_cambios",
            ]
        )

        if evento == "mitocondria_eficiente":
            self.energia += random.uniform(8.0, 16.0)
            mensaje = "⚡ Mitocondria eficiente: aumenta la energía."
        elif evento == "entrada_de_nutrientes":
            self.energia += random.uniform(5.0, 10.0)
            self.hidratacion += random.uniform(4.0, 8.0)
            mensaje = "🍽️ Entrada de nutrientes: mejora energía e hidratación."
        elif evento == "estres_oxidativo":
            self.membrana -= random.uniform(7.0, 14.0)
            self.energia -= random.uniform(3.0, 8.0)
            mensaje = "☣️ Estrés oxidativo: daña membrana y consume energía."
        elif evento == "reparacion_membrana":
            self.membrana += random.uniform(6.0, 12.0)
            self.energia -= random.uniform(2.0, 5.0)
            mensaje = "🩹 Reparación de membrana: sube membrana, baja energía."
        elif evento == "deshidratacion":
            self.hidratacion -= random.uniform(8.0, 15.0)
            mensaje = "🏜️ Deshidratación: cae la hidratación rápidamente."
        else:
            mensaje = "➖ Sin cambios relevantes este ciclo."

        self._limitar()
        self.historial.append(mensaje)
        return mensaje

    def estado(self) -> str:
        return (
            f"Ciclo {self.ciclo:02d} | "
            f"Energía: {self.energia:5.1f}% | "
            f"Hidratación: {self.hidratacion:5.1f}% | "
            f"Membrana: {self.membrana:5.1f}%"
        )


def simular(ciclos: int = 12, pausa: float = 0.6, semilla: int | None = None) -> None:
    if semilla is not None:
        random.seed(semilla)

    celula = Celula()

    print("📱 Simulación de célula para celular")
    print("-" * 56)

    for _ in range(ciclos):
        if not celula.viva():
            print("\n❌ La célula colapsó antes de completar todos los ciclos.")
            break

        celula.metabolizar()
        evento = celula.aplicar_evento()

        print(celula.estado())
        print(f"   {evento}")

        if pausa > 0:
            time.sleep(pausa)

    print("-" * 56)
    if celula.viva():
        print("✅ Simulación finalizada: la célula sigue estable.")
    else:
        print("⚠️ Simulación finalizada: la célula no sobrevivió.")


if __name__ == "__main__":
    simular(ciclos=12, pausa=0.5)
