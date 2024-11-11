# Caju Tech Challenge

## Autorizador de transações

O objetivo desse projeto é umplementar uma API REST que processe transações de cartão de crédito.

### Decisões técnicas
- A camada de domínio guarda as regras de negócio, é a mais complexa e a que possui mais testes.
- Nessa camada:
    - A camada `model` guarda os modelos;
    - A camada `service` guarda as regras de negócio;

- A camada repository controla as operações no banco de dados 
    - Escolhi o MongoDB por conta de sua estrutura de documentos, se encaixou bem na modelagem do problema

- A camada routes guarda os endpoints

## Como executar localmente

A Aplicação está conteinerizada, então é necessário o Docker para rodar localmente. Recomendo também a instalação do `MongoDB Compass` pra facilitar as consultas aos dados.

Dentro da pasta raiz do projeto, digite:

 ``docker-compose build; docker-compose up``

 Isso iniciará a api na porta 8080

 No endpoint http://localhost:8000/docs você encontrará o swagger da API.

 ### Chamadas

 ## Criar conta

```bash
 curl --location 'http://localhost:8000/account' --header 'Content-Type: application/json' --data-raw '{"email": "some-user@mailcom"}'
```

## Buscar conta pelo ID

```bash
curl --location 'http://localhost:8000/account/<ACCOUNT_ID>'
```

## Criar uma transação
```bash
curl --location 'http://localhost:8000/transaction' \
--header 'Content-Type: application/json' \
--data '{
    "account_id": "<ACCOUNT_ID>",
    "total_amount": 120.5,
    "mcc": "5411",
    "merchant": "MC Donalds"
}'
```


## Adicionar ou debitar saldo de uma conta

balance_type aceita os tipoes: `FOOD`, `MEAL` e `CASH`

operation aceita 1 (CRÉDITO) e 2 (DÉBITO)

```bash
    curl --location 'http://localhost:8000/account/<ACCOUNT_ID>/balance' \
    --header 'Content-Type: application/json' \
    --data '{
        "balance_type": "MEAL",
        "operation": 1, 
        "amount": 1000
    }'
```

 ## Como rodar os testes

    - Dependências:
        - Python 3.13
        - Pytest

Recomendo a criação de um ambiente virtual para o projeto.

Depois de ativar o `venv`, instale as dependências do projeto com `pip install -r requirements.txt` 

Para testar, execute: `python -m tests` na raiz do projeto


# Transações simultaneas

Eu lidaria com isso implementando um lock otimista, já que dada as especificações do problema, a chance disso acontecer é pequena. Inclusive, já deixei a solução encaminhada pra isso com o `balance.last_updated`

A ideia seria a seguinte: 
- A primeira coisa que o authorizer faz é buscar a conta, que traz seus balances e a data da última atualização de cada um deles.

- No momento da atualização (repository.update_balance()) eu adicionaria uma condição para checar o campo last_update. E só atualizaria o balance se as datas fossem iguais.
    - Se as datas forem diferentes significa que o balance foi atualizado e a versão que temos está desatualizada. O que deveria gerar um erro e impedir a atualização do balance.
    - Caso contrário, o balance seria atualizado assim como o campo last_update
