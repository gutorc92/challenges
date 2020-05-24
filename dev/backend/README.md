[![pipeline status](https://gitlab.com/grcprojetos/post-press/general-api/badges/dev/pipeline.svg)](https://gitlab.com/grcprojetos/post-press/general-api/commits/dev)
[![coverage report](https://gitlab.com/grcprojetos/post-press/general-api/badges/dev/coverage.svg)](https://gitlab.com/grcprojetos/post-press/general-api/commits/dev)

# API de Usuários

# Instalando e configurando

A API foi feita visando o uso de Python3.

>$ pip install -r requirements.txt

*Obs.*

Recomenda-se fortemente que se tenha um ambiente virtual dedicado por aplicações, para evitar comprometer a estabildiade do seu sistema operacional. Utilize o [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) ou um container [Docker](https://hub.docker.com/_/python/).


- Crie um arquivp `.env` no mesmo diretório do arquivo [api.py](api.py) com o seguinte formato:

```
MONGO_USER=admin
MONGO_PASS=admin
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DBNAME=eduqc
```

# Executando

> $ python api.py

A API deve estar disponivel na porta 8000.


# Executando os testes

> $ coverage run --source=. -m unittest discover -s test

# Executando o linter

> $ pylint *.py

# Servindo

Sirva com:

> gunicorn -b :8000  -w 8 -k tornado --log-level warning --log-file error_logs.log   wsgi

# Configurando servidor

### Utilizando o repositório clonado

- Instale o app via `pip install -r requirements.txt`.
- Crie o arquivo `.env` de acordo com o exemplo nos [Snippets](https://gitlab.com/grcprojetos/post-press/general-api/snippets/).
- Instale o Supervisor e o Nginx via APT.
- Crie o arquivo de configuração do Supervisor em `/etc/supervisor/conf.d` de acordo com o exemplo nos [Snippets](https://gitlab.com/grcprojetos/post-press/general-api/snippets/).
- Crie o arquivo de configuração do Nginx em `/etc/nginx/sites-available/` de acordo com o exemplo nos [Snippets](https://gitlab.com/grcprojetos/post-press/general-api/snippets/).
- Crie um link simbolico do arquivo de configuração do Nginx para `/etc/nginx/sites-enabled/` para habilitar o serviço.
- Habilite o serviço do Supervisor.
- Habilite o serviço do Nginx.
- Atualize a lista de serviços do Supervisor com `supervisorctl reread`
- Atualize o status dos serviços do Supervisor com `supervisorctl update`

### Utilizando containers

- Baixe o *docker-compose.yml*
- Logue no registry do gitlab: `docker login registry.gitlab.com`
- Levante o serviço com `docker-compose up -d`
- Garanta que o serviço esta rodando na porta 80

# Deploy

### Utilizando o repositório clonado

- Torne-se `sudo`
- Vá ao diretório `/www` e localize o repositório
- Baixe as atualizações: `git pull`
- Reinicie o Supervisor: `supervisorctl reload all`
- Espere alguns segundos ate que a aplicação seja levantada
- Verifique o status da aplicação no Supervisor: `supervisorctl status`


### Utilizando containers

- Baixe a ultima versão da api: `docker pull registry.gitlab.com/grcprojetos/post-press/general-api:prod`
- Vá ao diretório onde o *docker-compose.yml* se encontra
- Derrube o serviço atual: `docker-compose down`
- Levante o novo serviço: `docker-compose up -d`
- Garanta que o serviço esta rodando na porta 80
