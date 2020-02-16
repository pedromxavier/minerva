# minerva
### Um renovador automático de livros da biblioteca da UFRJ

## Instalação
```
$ git clone https://github.com/pedromxavier/minerva
$ cd minerva
$ sudo python3 setup.py install
```

## Uso:

Para renovar os livros de uma conta use o comando:
```
minerva [login] [senha]
```

Para guardar em cache suas credenciais:
```
minerva -c [login] [senha]
```

Para renovar os livros de todas as credenciais armazenadas:
```
minerva -r
```
