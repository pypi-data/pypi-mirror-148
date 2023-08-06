# logger-bro

A convenient logger package for quick integrations with monitoring tools

---

### Before publishing a new change

- Bump the version in `setup.py`

- Build the package

```console
python setup.py sdist bdist_wheel
```

- Publish the dist folder using `twin upload dist/*`

```console
twin upload dist/*
```
