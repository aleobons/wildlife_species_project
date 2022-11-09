# Instruções para compilação do pacote

## Instalação

No diretório raiz do projeto, execute os comandos:

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
docker build -t aleobons/wildlife:0.2 .
```