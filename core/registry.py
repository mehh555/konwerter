from pathlib import Path

from core.errors import ConversionError

REGISTRY = {}

def register(source_ext: str, target_ext: str):
    def decorator(func):
        REGISTRY[(source_ext, target_ext)] = func
        return func
    return decorator

def available_targets(source: Path) -> list[str]:
    return [dst for (src,dst) in REGISTRY if src == source.suffix.lower]

def convert(source: Path, target_ext: str, output_dir: Path) -> Path:
    target_ext = "." + target_ext.lower().lstrip(".")
    if not source.is_file():
        raise ConversionError(f"Nie znaleziono pliku: {source}")
    if not output_dir.is_dir():
        raise ConversionError(f"Nie ma katalogu: {output_dir}")

    func = REGISTRY.get((source.suffix.lower(), target_ext))
    if func is None:
        raise ConversionError(f"Nieobsługiwana konwersja: {source.suffix} -> {target_ext}")

    target = output_dir / (source.stem + target_ext)
    func(source, target)
    return target