# Guidelines to package compilation

## Installation

In the project root, run these commands:

```bash	
python setup.py build
```	

```bash
python setup.py install develop

```

```bash
pip install . 

```

## Build docker image

```bash
docker build -t aleobons/wildlife:0.1 .
```