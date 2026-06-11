# 🏗️ Clean Architecture — Aim Trainer

Documentación completa de la arquitectura del Aim Trainer implementado con Python y Pygame, siguiendo principios **SOLID**, **Clean Architecture** y **Domain-Driven Design**.

---

## 📐 Diagrama de Capas (Clean Architecture)

```mermaid
graph TB
    subgraph "Frameworks & Drivers"
        MAIN["main.py<br/>Punto de Entrada"]
        PYGAME["Pygame<br/>Framework Externo"]
    end

    subgraph "Interface Adapters"
        CORE["Core Layer<br/>GameLoop (Facade)<br/>FPSManager"]
        INPUT["Input Manager<br/>EventHandler<br/>SensitivityManager"]
        UI["UI/Stats<br/>TextRenderer<br/>StatsManager"]
        CONFIG["Config<br/>ConfigManager"]
    end

    subgraph "Application Business Rules"
        ENTITIES["Game Entities<br/>Target<br/>Crosshair"]
    end

    subgraph "Enterprise Business Rules"
        UTILS["Utils<br/>math_utils<br/>(funciones puras)"]
    end

    MAIN --> CORE
    CORE --> INPUT
    CORE --> UI
    CORE --> ENTITIES
    CORE --> CONFIG
    INPUT --> PYGAME
    UI --> PYGAME
    ENTITIES --> UTILS
    ENTITIES --> PYGAME
    CONFIG --> PYGAME

    style MAIN fill:#f9f,stroke:#333,stroke-width:2px
    style CORE fill:#bbf,stroke:#333,stroke-width:2px
    style INPUT fill:#bfb,stroke:#333,stroke-width:2px
    style UI fill:#bfb,stroke:#333,stroke-width:2px
    style CONFIG fill:#bfb,stroke:#333,stroke-width:2px
    style ENTITIES fill:#fbb,stroke:#333,stroke-width:2px
    style UTILS fill:#ddd,stroke:#333,stroke-width:2px
```

**Regla de dependencia:** Las dependencias apuntan hacia adentro. Las capas externas dependen de las internas, nunca al revés.

---

## 🔄 Diagrama de Flujo del Bucle Principal

```mermaid
sequenceDiagram
    participant Main as main.py
    participant GL as GameLoop
    participant FM as FPSManager
    participant EH as EventHandler
    participant SM as SensitivityManager
    participant TG as Target(s)
    participant CH as Crosshair
    participant ST as StatsManager
    participant TR as TextRenderer
    participant PG as Pygame Display

    Main->>GL: run()
    GL->>GL: initialize()
    GL->>PG: pygame.init()
    GL->>PG: display.set_mode(HWSURFACE | DOUBLEBUF)
    GL->>PG: mouse.set_visible(False)
    GL->>GL: reset_game()

    loop while running
        GL->>FM: tick() → dt_ms
        FM->>PG: Clock.tick(240)
        FM-->>GL: dt_ms (perf_counter)

        GL->>EH: update()
        EH->>PG: mouse.get_rel() → raw_dx, raw_dy
        EH->>PG: event.get() [drenar todos]
        EH-->>GL: events, raw_dx, raw_dy

        GL->>GL: process_events()
        alt SHOOT
            GL->>ST: register_shot()
            GL->>TG: inside_circle?(crosshair, target)
            alt HIT
                GL->>ST: register_hit(reaction_time)
                GL->>TG: hit() → DYING
            else MISS
                Note over GL: click al aire
            end
        else SENSITIVITY_UP/DOWN
            GL->>SM: multiplier ±= 0.1
        else TARGET_SIZE_UP/DOWN
            GL->>GL: radius ±= 5
        else RESTART
            GL->>GL: reset_game()
        else TOGGLE_PAUSE
            GL->>GL: paused = !paused
        else TOGGLE_MODE
            GL->>GL: flicking ↔ tracking
        else FULLSCREEN
            GL->>PG: toggle_fullscreen()
        end

        alt not paused
            GL->>SM: apply(raw_dx, raw_dy)
            SM-->>GL: dx_eff, dy_eff
            GL->>GL: crosshair_x += dx_eff
            GL->>GL: crosshair_y += dy_eff
            GL->>GL: clamp(crosshair en ventana)

            loop for each target
                GL->>TG: update(dt_ms)
                TG->>TG: state machine (SPAWNING→ALIVE→DYING→DEAD)
            end

            GL->>GL: update_spawner(dt_ms)
            GL->>GL: cleanup_targets()
            alt target EXPIRED
                GL->>ST: register_miss()
            end
        end

        GL->>GL: render()
        GL->>PG: screen.fill(20, 20, 30)

        loop for each target
            GL->>TG: draw(screen)
            TG->>PG: draw.circle()
        end

        GL->>CH: draw(screen, crosshair_x, crosshair_y)
        CH->>PG: draw.rect() × 4 + draw.circle()

        GL->>TR: render_lines(screen, stats_lines)
        TR->>PG: font.render() + blit()

        alt paused
            GL->>TR: "PAUSED"
        end
        alt game_over
            GL->>TR: "GAME OVER"
        end

        GL->>PG: display.flip()
    end

    GL->>PG: mouse.set_visible(True)
    GL->>PG: pygame.quit()
```

---

## 🧩 Diagrama de Clases (UML Simplificado)

```mermaid
classDiagram
    class GameLoop {
        +ConfigManager config
        +FPSManager fps_manager
        +EventHandler event_handler
        +SensitivityManager sensitivity
        +StatsManager stats
        +TextRenderer text_renderer
        +Crosshair crosshair
        +List~Target~ targets
        +float crosshair_x, crosshair_y
        +bool running, paused, game_over
        +str current_mode
        --
        +initialize()
        +run()
        +reset_game()
        -process_events()
        -handle_shot()
        -update_targets(dt_ms)
        -update_spawner(dt_ms)
        -cleanup_targets()
        -spawn_target()
        -render()
        -render_ui()
        -toggle_mode()
        -toggle_fullscreen()
        +shutdown()
    }

    class FPSManager {
        -Clock _clock
        +int fps_limit
        -float _dt_ms
        -float _current_fps
        -float _last_time
        --
        +tick()
        +dt_ms: float
        +dt_seconds: float
        +current_fps: float
    }

    class EventHandler {
        -List~GameEvent~ _events
        -float _raw_dx, _raw_dy
        -Tuple _mouse_pos
        -set _keys_pressed
        --
        +update()
        -process_keydown(key)
        +events: List~GameEvent~
        +raw_mouse_rel: Tuple
        +mouse_pos: Tuple
        +has_event(event_type): bool
    }

    class SensitivityManager {
        +float multiplier
        +bool invert_y
        --
        +apply(raw_dx, raw_dy): Tuple
    }

    class Target {
        +float x, y
        +int radius
        +Tuple color, hit_color
        +int lifetime_ms
        +TargetState state
        +float spawn_duration_ms
        +float dying_duration_ms
        --
        +update(dt_ms)
        +hit(): bool
        +position: Tuple
        +draw_radius: float
        +is_clickable: bool
        +is_alive: bool
        +is_removable: bool
        +draw(screen)
    }

    class TargetState {
        <<enumeration>>
        SPAWNING
        ALIVE
        DYING
        EXPIRED
        DEAD
    }

    class Crosshair {
        +int size
        +int thickness
        +Tuple color
        +int gap
        +int dot_radius
        --
        +draw(screen, x, y)
    }

    class StatsManager {
        +int hits, misses, total_shots
        +int combo, best_combo, score
        +int total_targets_spawned
        -List~float~ _reaction_times
        --
        +reset()
        +register_shot()
        +register_hit(reaction_time_ms)
        +register_miss()
        +register_target_spawned()
        +accuracy: float
        +avg_reaction_time_ms: float
        +best_reaction_time_ms: float
        +last_reaction_time_ms: float
        +get_summary_lines(): List~str~
    }

    class TextRenderer {
        +str font_name
        +int font_size
        +Tuple text_color
        +int background_alpha
        -Font _font
        --
        -ensure_font()
        +set_font_size(size)
        +render_line(screen, text, x, y)
        +render_lines(screen, lines, x, y)
        +render_with_background(screen, text, x, y)
    }

    class ConfigManager {
        -Dict _config
        -ConfigManager _instance
        --
        +load(filepath)
        +get(key_path, default): Any
        +window_width: int
        +window_height: int
        +fps_limit: int
        +sensitivity_multiplier: float
        +target_radius: int
        +target_lifetime_ms: int
        +crosshair_size: int
        +game_mode_mode: str
        +ui_font_size: int
    }

    class GameEvent {
        <<enumeration>>
        QUIT
        SHOOT
        SHOOT_RELEASE
        RESTART
        TOGGLE_PAUSE
        SENSITIVITY_UP
        SENSITIVITY_DOWN
        TARGET_SIZE_UP
        TARGET_SIZE_DOWN
        TOGGLE_MODE
        FULLSCREEN
    }

    GameLoop --> FPSManager
    GameLoop --> EventHandler
    GameLoop --> SensitivityManager
    GameLoop --> StatsManager
    GameLoop --> TextRenderer
    GameLoop --> ConfigManager
    GameLoop --> Crosshair
    GameLoop --> "0..*" Target
    Target --> TargetState
    EventHandler --> GameEvent
```

---

## 🔁 Máquina de Estados del Target

```mermaid
stateDiagram-v2
    [*] --> SPAWNING: spawn_target()
    
    SPAWNING --> ALIVE: spawn_timer ≥ spawn_duration_ms
    SPAWNING --> SPAWNING: animación de escala (0→1)
    
    ALIVE --> DYING: hit() [click sobre target]
    ALIVE --> EXPIRED: alive_timer ≥ lifetime_ms
    
    DYING --> DEAD: dying_timer ≥ dying_duration_ms
    DYING --> DYING: feedback visual (color verde)
    
    EXPIRED --> [*]: cleanup (registra miss)
    DEAD --> [*]: cleanup
    
    note right of SPAWNING
        150 ms
        Escala: 0 → 1
    end note
    
    note right of ALIVE
        Clickable
        lifetime_ms configurable
    end note
    
    note right of DYING
        120 ms
        Color: hit_color
    end note
```

---

## 📊 Diagrama de Flujo de Datos

```mermaid
flowchart LR
    subgraph Input
        MOUSE["Mouse Hardware"]
        KB["Teclado"]
    end

    subgraph "Input Layer"
        PYGAME_IN["pygame.mouse.get_rel()<br/>pygame.event.get()"]
        EH2["EventHandler"]
        SM2["SensitivityManager"]
    end

    subgraph "Game Logic"
        GL2["GameLoop"]
        SPAWN["Target Spawner"]
        COL["Collision Detection"]
        FSM["Target FSM"]
    end

    subgraph "Stats"
        ST2["StatsManager"]
    end

    subgraph "Rendering"
        REND["Render Pipeline"]
        TR2["TextRenderer"]
        CH2["Crosshair"]
    end

    subgraph Output
        SCREEN["Pantalla<br/>(display.flip)"]
    end

    MOUSE -->|"Δx, Δy"| PYGAME_IN
    KB -->|"scancodes"| PYGAME_IN
    PYGAME_IN -->|"raw_dx, raw_dy<br/>GameEvents"| EH2
    EH2 -->|"raw_dx, raw_dy"| SM2
    SM2 -->|"dx_eff, dy_eff"| GL2
    EH2 -->|"GameEvent[]"| GL2
    
    GL2 -->|"dt_ms"| FSM
    GL2 -->|"spawn command"| SPAWN
    GL2 -->|"crosshair_xy"| COL
    
    SPAWN -->|"new Target()"| FSM
    COL -->|"hit: true/false"| ST2
    
    ST2 -->|"stats_lines[]"| TR2
    GL2 -->|"crosshair_xy"| CH2
    FSM -->|"targets[]"| REND
    
    REND --> SCREEN
    TR2 --> REND
    CH2 --> REND
```

---

## 📦 Diagrama de Paquetes (Dependencias)

```mermaid
graph TD
    subgraph "main.py"
        MAIN_PKG["Entry Point"]
    end

    subgraph "core"
        GL["GameLoop"]
        FPS["FPSManager"]
    end

    subgraph "input_manager"
        EH["EventHandler"]
        SM["SensitivityManager"]
        GE["GameEvent"]
    end

    subgraph "game_entities"
        TGT["Target"]
        TS["TargetState"]
        CH["Crosshair"]
    end

    subgraph "ui_stats"
        TR["TextRenderer"]
        STM["StatsManager"]
    end

    subgraph "config"
        CM["ConfigManager"]
    end

    subgraph "utils"
        MU["math_utils"]
    end

    subgraph "External"
        PG["pygame"]
    end

    MAIN_PKG --> GL
    GL --> FPS
    GL --> EH
    GL --> SM
    GL --> TGT
    GL --> CH
    GL --> TR
    GL --> STM
    GL --> CM
    
    EH --> GE
    EH --> PG
    SM --> PG
    TGT --> TS
    TGT --> PG
    CH --> PG
    TR --> PG
    CM --> PG["json (stdlib)"]
    MU --> PG["math (stdlib)"]
    
    TGT --> MU
    GL --> MU

    style MAIN_PKG fill:#f9f,stroke:#333
    style GL fill:#bbf,stroke:#333
    style PG fill:#ddd,stroke:#333
```

---

## 🎯 Principios SOLID Aplicados

```mermaid
mindmap
  root((SOLID))
    SRP<br/>Single Responsibility
      GameLoop: solo orquestación
      FPSManager: solo tiempo
      EventHandler: solo captura de input
      SensitivityManager: solo transformación
      Target: solo ciclo de vida
      Crosshair: solo renderizado de mira
      TextRenderer: solo renderizado de texto
      StatsManager: solo cálculo estadístico
      ConfigManager: solo acceso a configuración
    OCP<br/>Open/Closed
      TargetState enum: añadir estados sin modificar lógica
      GameEvent enum: añadir eventos sin tocar handler
      Nuevos modos: extender modo sin cambiar GameLoop
    LSP<br/>Liskov Substitution
      Target subclases: TrackingTarget puede sustituir a Target
      sin romper el sistema de spawn/colisión
    ISP<br/>Interface Segregation
      Cada módulo expone solo lo necesario
      Sin interfaces monolíticas
    DIP<br/>Dependency Inversion
      GameLoop depende de abstracciones (clases)
      No depende de pygame directamente
      ConfigManager abstrae el origen de datos (JSON)
```

---

## ⚡ Estrategia Anti Input Lag

```mermaid
flowchart TD
    A["Frame N comienza"] --> B["pygame.mouse.get_rel()"]
    B --> C["Acumula TODO el desplazamiento<br/>desde Frame N-1"]
    C --> D["pygame.event.get()"]
    D --> E["Drena TODOS los eventos<br/>pendientes en la cola"]
    E --> F["Procesa lógica del juego<br/>(solo 1 iteración de eventos)"]
    F --> G["Renderiza frame"]
    G --> H["display.flip()"]
    H --> I["Frame N+1 comienza"]
    
    B -.->|"RAW INPUT<br/>float preciso"| C
    D -.->|"Sin pérdida<br/>de eventos"| E
    
    style B fill:#bfb,stroke:#333
    style D fill:#bfb,stroke:#333
    style G fill:#bbf,stroke:#333
```

---

## 📐 Vistas de Arquitectura (4+1 Views)

### Vista Lógica

```mermaid
graph TD
    subgraph "Vista Lógica"
        A["GameLoop<br/>(Controller)"]
        B["Target<br/>(Entity)"]
        C["Crosshair<br/>(Entity)"]
        D["StatsManager<br/>(Service)"]
        E["SensitivityManager<br/>(Service)"]
        F["EventHandler<br/>(Boundary)"]
        G["TextRenderer<br/>(Boundary)"]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
```

### Vista de Procesos

```mermaid
sequenceDiagram
    participant Main as Main Thread
    participant Game as Game Loop
    participant Render as Render Pipeline
    
    Main->>Game: run()
    loop 240 FPS
        Game->>Game: Input Processing (sync)
        Game->>Game: Game Logic (sync)
        Game->>Render: Render Frame
        Render->>Render: GPU Flip
    end
```

### Vista de Desarrollo

```
core/           ← Capa de aplicación
input_manager/  ← Adaptadores de entrada
game_entities/  ← Entidades de dominio
ui_stats/       ← Adaptadores de salida
config/         ← Configuración
utils/          ← Utilidades compartidas
```

### Vista Física

```
┌──────────────────────────────────┐
│  PC del Usuario                  │
│  ┌────────────────────────────┐  │
│  │  main.py                   │  │
│  │  ┌──────────────────────┐  │  │
│  │  │  Python 3.11         │  │  │
│  │  │  ┌────────────────┐  │  │  │
│  │  │  │  Pygame 2.6    │  │  │  │
│  │  │  │  ┌──────────┐  │  │  │  │
│  │  │  │  │  SDL 2   │  │  │  │  │
│  │  │  │  │  GPU     │  │  │  │  │
│  │  │  │  └──────────┘  │  │  │  │
│  │  │  └────────────────┘  │  │  │
│  │  └──────────────────────┘  │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │  resources/config.json    │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

### Vista de Escenarios (Casos de Uso)

```mermaid
flowchart LR
    subgraph "Casos de Uso Principales"
        UC1["🎯 Jugar Partida Flicking<br/>30 targets, máxima precisión"]
        UC2["🔄 Cambiar Modo<br/>Flicking ↔ Tracking"]
        UC3["⚙️ Ajustar Sensibilidad<br/>en caliente con +/-"]
        UC4["📏 Ajustar Tamaño Target<br/>en caliente con [/]"]
        UC5["⏸️ Pausar/Reanudar<br/>ESC o P"]
        UC6["🔄 Reiniciar Sesión<br/>R"]
        UC7["🖥️ Pantalla Completa<br/>F11"]
    end
```

---

## 📊 Resumen de Métricas de Código

| Métrica | Valor |
|---|---|
| **Módulos** | 6 paquetes |
| **Archivos Python** | 13 |
| **Clases** | 8 principales |
| **Enums** | 2 (TargetState, GameEvent) |
| **Funciones puras** | 3 (utils) |
| **Líneas totales** | ~900 |
| **Dependencia externa** | Solo Pygame |
| **Archivos de configuración** | 1 JSON |
| **Documentación** | 2 Markdown |
