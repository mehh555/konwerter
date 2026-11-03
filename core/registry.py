from core.errors import ConversionError

REGISTRY = {}


def register(src, dst):
    def wrap(func):
        REGISTRY[src, dst] = func
        return func
    return wrap


def available_targets(path):
    return sorted(dst for src, dst in REGISTRY if src == path.suffix.lower())


def convert(source, fmt, out_dir):
    fmt = "." + fmt.lower().lstrip(".")
    func = REGISTRY.get((source.suffix.lower(), fmt))

    if not source.is_file():
        raise ConversionError(f"Nie ma pliku {source}")
    if not out_dir.is_dir():
        raise ConversionError(f"Nie ma katalogu {out_dir}")
    if not func:
        raise ConversionError(f"Nie obsługuję {source.suffix} -> {fmt}")

    target = out_dir / (source.stem + fmt)
    try:
        func(source, target)
    except UnicodeDecodeError:
        raise ConversionError("Plik nie jest w UTF-8")
    except OSError as e:
        raise ConversionError(f"Błąd pliku: {e}")
    return target