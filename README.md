# AimTrainer
Un simulador de puntería de alto rendimiento, desarrollado en Python con Pygame, diseñado específicamente para mejorar la memoria muscular y la precisión en juegos
=======
# 🎯 Aim Trainer — Python/Pygame

Aim Trainer de alto rendimiento enfocado en la práctica de reflejos, precisión y ajuste de sensibilidad "en caliente". Desarrollado con Python y Pygame siguiendo principios **SOLID** y **Clean Architecture**.

---

## 🚀 Ejecución Rápida

```bash
pip install pygame
python main.py
```

---

## 🎮 Controles

| Tecla | Acción |
|---|---|
| **Mouse** | Mover crosshair |
| **Click Izquierdo** | Disparar |
| **ESC / P** | Pausar / Reanudar |
| **R** | Reiniciar sesión |
| **M** | Cambiar modo (Flicking ↔ Tracking) |
| **F11** | Pantalla completa |
| **+ / -** | Ajustar sensibilidad (±0.1) |
| **[ / ]** | Ajustar tamaño del target (±5 px) |

---

## 📁 Estructura del Proyecto

```
AimTrainer/
├── main.py                          # Punto de entrada
├── README.md                        # Este archivo
├── clean-architecture.md            # Documentación de arquitectura (Mermaid)
├── resources/
│   └── config.json                  # Configuración externa (JSON)
├── core/
│   ├── __init__.py
│   ├── game_loop.py                 # GameLoop — Orquestador principal (Facade)
│   └── fps_manager.py               # FPSManager — Control de FPS y delta time
├── input_manager/
│   ├── __init__.py
│   ├── event_handler.py             # EventHandler — Captura de eventos Pygame
│   └── sensitivity_manager.py       # SensitivityManager — Fórmula de sensibilidad
├── game_entities/
│   ├── __init__.py
│   ├── target.py                    # Target — Máquina de estados finitos
│   └── crosshair.py                 # Crosshair — Mira competitiva
├── ui_stats/
│   ├── __init__.py
│   ├── text_renderer.py             # TextRenderer — Renderizado de texto
│   └── stats_manager.py             # StatsManager — Métricas de rendimiento
├── config/
│   ├── __init__.py
│   └── config_manager.py            # ConfigManager — Acceso tipado a JSON
└── utils/
    ├── __init__.py
    └── math_utils.py                # clamp, distance, inside_circle
```

---

## ⚙️ Configuración (`resources/config.json`)

```json
{
  "window": { "width": 800, "height": 600, "fps": 240 },
  "sensitivity": { "multiplier": 1.0, "invert_y": false },
  "target": { "radius": 30, "lifetime_ms": 2000, "spawn_delay_ms": 500 },
  "crosshair": { "size": 20, "thickness": 2, "gap": 4 },
  "game_mode": { "mode": "flicking", "total_targets": 30, "infinite": false }
}
```

Todos los parámetros son modificables sin tocar código.

---

## 🧠 Fórmula de Sensibilidad (eDPI)

```
raw_dx, raw_dy = pygame.mouse.get_rel()   ← Raw Input acumulado
dx_efectivo = raw_dx × multiplier
dy_efectivo = raw_dy × multiplier × (-1 si invert_y)
crosshair += (dx_efectivo, dy_efectivo)
```

Equivalente al sistema de sensibilidad de juegos competitivos: `eDPI = DPI × sensibilidad_juego`.

---

## 📊 Métricas en Tiempo Real

| Métrica | Descripción |
|---|---|
| **Score** | Puntuación ponderada (hit base + speed bonus + combo bonus) |
| **Accuracy** | `(hits / total_shots) × 100%` |
| **Avg Reaction** | Tiempo promedio entre spawn y click (ms) |
| **Best Reaction** | Mejor tiempo de reacción registrado (ms) |
| **Last Reaction** | Último tiempo de reacción (ms) — feedback inmediato |
| **Combo** | Racha de aciertos consecutivos |
| **FPS** | Frames por segundo actuales |

---

## 🏗️ Principios de Diseño

| Principio | Aplicación |
|---|---|
| **SRP** | Cada módulo tiene una única responsabilidad |
| **OCP** | Nuevos modos/eventos se añaden extendiendo, sin modificar el núcleo |
| **DIP** | `GameLoop` depende de abstracciones (clases), no de implementaciones concretas |
| **Facade** | `GameLoop` centraliza la interacción entre subsistemas |
| **Singleton** | `ConfigManager` única instancia compartida |

---

## 🔧 Requisitos

- Python 3.10+
- Pygame 2.6+

---

## 📄 Licencia

Proyecto educativo de práctica de arquitectura de software.
>>>>>>> 05d9917 (Aimtrainer)
