cd dist
F=$(ls -A | head -1)
/root/.local/bin/micromamba run -n wofs-radar python -m pip install $F