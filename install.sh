#!/bin/sh
# Instalador de gestion-tareas para Mac y Linux.
# Uso:
#   curl -fsSL https://raw.githubusercontent.com/gerardexe/gestion-tareas/main/install.sh | sh
set -eu

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)              asset=gestion-tareas-linux-x64 ;;
  Linux-aarch64|Linux-arm64) asset=gestion-tareas-linux-arm64 ;;
  Darwin-arm64)              asset=gestion-tareas-macos-arm64 ;;
  Darwin-x86_64)             asset=gestion-tareas-macos-x64 ;;
  *) echo "Sistema no soportado: $(uname -s) $(uname -m)" >&2; exit 1 ;;
esac

dir="$HOME/.local/bin"
mkdir -p "$dir"
echo "Descargando gestion-tareas..."
curl -fsSL "https://github.com/gerardexe/gestion-tareas/releases/latest/download/$asset" -o "$dir/gestion-tareas"
chmod +x "$dir/gestion-tareas"

case ":$PATH:" in
  *":$dir:"*)
    echo "Listo. Para usarlo escribe: gestion-tareas"
    ;;
  *)
    case "$(basename "${SHELL:-sh}")" in
      zsh)  rc="$HOME/.zshrc" ;;
      bash) if [ "$(uname -s)" = Darwin ]; then rc="$HOME/.bash_profile"; else rc="$HOME/.bashrc"; fi ;;
      *)    rc="$HOME/.profile" ;;
    esac
    grep -qs '.local/bin' "$rc" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
    echo "Listo. Cierra esta terminal, abre una nueva y escribe: gestion-tareas"
    ;;
esac
