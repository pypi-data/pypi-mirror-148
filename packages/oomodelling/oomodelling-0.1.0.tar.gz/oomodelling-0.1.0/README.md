# Object Oriented Modelling Framework for Causal Models

# Installing from pip
```
pip install oomodelling
```

# Installing the package from source code

Open terminal in this folder.

```
pip install -e .
```

# Publishing this package on pypi

Install twine on virtual environment: `pip install twine`

See [publish_package.ps1](./publish_package.ps1)

## Common Issues

Error:
```
error: invalid command 'bdist_wheel'
```
Solution:
```
pip install wheel
```