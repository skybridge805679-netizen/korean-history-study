#!/bin/zsh
cd -- "${0:A:h}"
if command -v python3 >/dev/null 2>&1; then
  python3 run.py
elif [[ -x "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" ]]; then
  "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" run.py
else
  echo "Python 3가 필요합니다. https://www.python.org/downloads/ 에서 설치해 주세요."
  read "?Enter 키를 누르면 닫힙니다."
fi
