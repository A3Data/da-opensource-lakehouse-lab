# BEM VINDO EU.A3

Nesse Lab falaremos um pouco sobre como montar um DataWarehouse/LakeHouse para estudos!

Na pasta data estão presentes os arquivos .csv que iremos utilizar
Na pasta conf está o arquivo .env utilizado como variaveis de ambiente
Na pasta volumes encontram-se os volumes utilizados pelo container

## CONFIGURAÇÕES INICIAIS

### Instalação GIT
https://git-scm.com/download/win

git config --global user.name USER
git config --global user.email EMAIL

### Instalação Chocolatey
https://chocolatey.org/install
PowerShell as ADMIN: Set-ExecutionPolicy AllSigned
PowerShell as ADMIN: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

### ATENÇÂO 
Quando instalar um pacote pelo Choco, a seguinte mensagem será exibida Do you want to run the script?([Y]es/[A]ll - yes to all/[N]o/[P]rint):
Nesse caso, digitar A e pressionar Enter para permitir que todos os scripts de instalações sejam executados

#### Instalação Kind Docker
Na Windows VM:
	Criar a máquina, executar o Power Shell como ADMIN e Set-VMProcessor -VMName <Nome VM>-ExposeVirtualizationExtensions $true
	Iniciar a máquina, ir em Ativar ou Desativar recursos do Windows, ativar HyperV. Reiniciar a Maquina

PowerShell as ADMIN: wsl --install -d ubuntu
PowerShell as ADMIN: choco install kind


# Configuração dos serviços

## Configuração Inicial / MinIO

No primeiro momento, deve-se iniciar o [MinIO](http://localhost:9001/), para criação dos Buckets (bronze, silver, gold) e Chaves de acesso:
'''
docker-compose up minio
'''

Feito isso, pode-se dropar o container (Ctrl+C) e inicia-lo por completo usando 
'''
docker-compose up
'''

Após a conclusão de download de todas a imagens e o container estar rodando é possível acessar os serviços atrvés das urls abaixo:

### URLs
[Nessie](http://localhost:19120/)
[Dremio](http://localhost:9047)
[MinIO](http://localhost:9001/)
[PGAdmin/Postgres](http://localhost:8070/)
[Jupyter/Spark](http://localhost:8888/)

## Configuração Dremio

Ao acessar a interface do dremio pela primeira vez, deve-se realizar o cadastro.
Agora vamos adicionar a conexão com o Nessie e MinIO, com as configurações abaixo:
Add Source Nessie configuration

### General
* Name NessieDataCatalog
* Nessie Endpoint URL: `http://nessie:19120/api/v2`
* Nessie Authentication Type: `None`

### Storage
* Authentication Type: `AWS Access Key`
* AWS Access Key: `Adicionar a access key criada no minio`
* AWS Access Secret: `Adicionar a secret key criada no minio`
* AWS Root Path: `/bronze/`

#### Properties
Adicionar as propriedades abaixo:
1. `fs.s3a.path.style.access` = `true`
2. `fs.s3a.endpoint` = `minio:9000`
3. `dremio.s3.compat` = `true`

* Desmarcar Encrypt connection

## Configuração Postgres


# Links úteis

https://www.dremio.com/blog/intro-to-dremio-nessie-and-apache-iceberg-on-your-laptop/

https://medium.com/@khurrammeraj17/creating-a-lakehouse-by-using-apache-spark-minio-nessie-catalog-and-dremio-67c23a335616

https://blog.min.io/uncover-data-lake-nessie-dremio-iceberg/

https://projectnessie.org/guides/spark-s3/


