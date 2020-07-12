# minerva
### Um renovador automático de livros da biblioteca da UFRJ

## Instalação
Requer Python3.7.x

### Linux, OSx
```
$ git clone https://github.com/pedromxavier/minerva
$ cd minerva
$ sudo python3 setup.py install
```

### Windows - Executar prompt de comando como administrador.
```
> git clone https://github.com/pedromxavier/minerva
> cd minerva
> python setup.py install
```

## Uso:

### Linux, OSx
```
$ minerva [options]
```

### Windows
```
> python -m minerva [options]
```

Para renovar os livros de uma conta use o comando:
```
minerva [user] [senha]
```

Para guardar em cache suas credenciais:
```
minerva -c [user] [senha]
```

Para renovar os livros de todas as credenciais armazenadas:
```
minerva -r
```

## Futuro:
- Implementar configurações de renovação automática (agendada).
- Implementar casos de erro ao renovar.