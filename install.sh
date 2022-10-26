cd dist
F=$(ls -A | head -1)
conda run -n wofs-radar python -m pip install $F