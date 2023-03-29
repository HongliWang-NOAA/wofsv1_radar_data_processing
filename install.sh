cd dist
F=$(ls -A | head -1)
micromamba run -n wofs-radar python -m pip install $F