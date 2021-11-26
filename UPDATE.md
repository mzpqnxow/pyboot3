## Updating Packages / Adding Support For New Minor Versions of Python

Roughly:

```
python3.9 -mpip install --system -I --root $(realpath macroot) --upgrade --no-binary :all: -r pyboot3-developer-requirements.txt --no-warn-script-location
```
