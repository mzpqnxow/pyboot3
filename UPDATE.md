## Updating Packages / Adding Support For New Minor Versions of Python

Roughly:

```
python3.9 -mpip install -I --root $(realpath macroot) --upgrade --no-binary :all: -r pyboot3-developer-requirements.txt
```
