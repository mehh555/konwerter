import logging
import os
import time

from core.errors import ConversionError

log = logging.getLogger("konwerter")

REGISTRY = {}


def ext(fmt):
    return "." + fmt.strip().lower().lstrip(".")


def register(src, dst):
    def wrap(func):
        REGISTRY[ext(src), ext(dst)] = func
        return func
    return wrap


def available_targets(path):
    return sorted(dst for src, dst in REGISTRY if src == path.suffix.lower())


def validate(source, fmt, out_dir):
    if not fmt:
        raise ConversionError("Nie wybrano formatu docelowego.")
    if not source.is_file():
        raise ConversionError(f"Nie ma pliku {source}. Wybierz istniejący plik.")
    if (source.suffix.lower(), ext(fmt)) not in REGISTRY:
        dostepne = ", ".join(available_targets(source)) or "brak"
        raise ConversionError(f"Nie obsługuję {source.suffix or '(brak rozszerzenia)'} -> {ext(fmt)}. "
                              f"Dla tego pliku dostępne: {dostepne}.")
    if not out_dir.is_dir():
        raise ConversionError(f"Nie ma katalogu {out_dir}. Wybierz istniejący katalog.")
    if not os.access(out_dir, os.W_OK):
        raise ConversionError(f"Brak prawa zapisu w {out_dir}. Wybierz inny katalog.")


def target_path(source, fmt, out_dir):
    return out_dir / (source.stem + ext(fmt))


def free_path(path):
    n, candidate = 1, path
    while candidate.exists():
        candidate = path.with_name(f"{path.stem} ({n}){path.suffix}")
        n += 1
    return candidate


def to_error(e):
    if isinstance(e, ConversionError):
        return e
    if isinstance(e, UnicodeDecodeError):
        return ConversionError("Plik nie jest zapisany w UTF-8. Zapisz go ponownie jako UTF-8 i spróbuj jeszcze raz.")
    if isinstance(e, PermissionError):
        return ConversionError("Brak dostępu do pliku. Zamknij go w innym programie albo wybierz inny katalog.")
    if isinstance(e, OSError):
        return ConversionError(f"Błąd pliku: {e.strerror or e}.")
    return ConversionError(f"Nieoczekiwany błąd ({type(e).__name__}): {e}")


def convert(source, fmt, out_dir, overwrite=False):
    validate(source, fmt, out_dir)
    func = REGISTRY[source.suffix.lower(), ext(fmt)]

    target = target_path(source, fmt, out_dir)
    if target.exists() and not overwrite:
        target = free_path(target)

    tmp = target.with_name(target.stem + ".tmp" + target.suffix)
    start = time.perf_counter()
    try:
        func(source, tmp)
        os.replace(tmp, target)
    except Exception as e:
        error = to_error(e)
        log.error("%s -> %s: %s", source, ext(fmt), error, exc_info=error is not e)
        raise error from e
    finally:
        tmp.unlink(missing_ok=True)

    log.info("%s -> %s (%.2f s)", source, target, time.perf_counter() - start)
    return target