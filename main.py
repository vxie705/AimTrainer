import sys

from core import GameLoop


def main() -> None:
    game = GameLoop()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        raise
    finally:
        game.shutdown()


if __name__ == "__main__":
    main()