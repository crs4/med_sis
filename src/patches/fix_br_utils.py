"""
Patch per il bug UnboundLocalError in geonode.br.management.commands.utils.utils

La funzione remove_existing_tables() chiama curs.close() fuori dal loop for:
se pg_tables è vuoto, 'curs' non viene mai assegnato → UnboundLocalError.

Questo script va eseguito una volta all'avvio del container Django
(dall'entrypoint.sh) per applicare la correzione in-place.
"""
import importlib
import inspect
import os
import sys

def patch():
    try:
        import geonode.br.management.commands.utils.utils as mod
    except ImportError:
        return

    src_path = inspect.getfile(mod)
    with open(src_path) as f:
        content = f.read()

    marker = "# PATCHED: fix_br_utils"
    if marker in content:
        return

    old = (
        "    curs.close()\n"
        "    conn.close()"
    )
    new = (
        f"    # {marker}\n"
        "    try:\n"
        "        curs.close()\n"
        "    except Exception:\n"
        "        pass\n"
        "    try:\n"
        "        conn.close()\n"
        "    except Exception:\n"
        "        pass"
    )

    if old not in content:
        return

    content = content.replace(old, new, 1)
    with open(src_path, "w") as f:
        f.write(content)
    print(f"[fix_br_utils] Patched {src_path}")

if __name__ == "__main__":
    patch()
