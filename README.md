# Trotiurban — Automação de testes (Urban Scooter)

Testes automatizados em Python para o projeto final de QA (TripleTen), cobrindo:

- **Tarefa 1 (Web)**: testes de UI com Selenium no formulário "Para quem é a scooter" (`codtestertroti.py` + `cod_troti.py`).
- **Tarefa 3 (API)**: testes de API com `requests` + `pytest` para os endpoints de Adicionar/Excluir entregador (`test_api_courier.py`).

## Estrutura

| Arquivo | Papel |
|---|---|
| `data.py` | URLs dos servidores e dados de teste (Page Object Model / config) |
| `helpers.py` | Funções utilitárias (checar servidor no ar, gerar login único) |
| `cod_troti.py` | Page Object do formulário web (`UrbanScooterOrderPage`) |
| `codtestertroti.py` | Testes Selenium (Tarefa 1) |
| `test_api_courier.py` | Testes de API (Tarefa 3) |

## Bugs conhecidos (marcados com `@pytest.mark.xfail`)

Vários testes documentam bugs já reportados no Jira (JSQ-1 a JSQ-17) e são marcados
como `xfail`: eles descrevem o comportamento **correto** esperado, então falham de
propósito enquanto o bug não for corrigido. Quando aparecer `XPASS` na execução,
significa que o bug foi corrigido e o `xfail` pode ser removido do teste.

## Configuração

Os servidores de teste (TripleTen) expiram após 2h de inatividade. Antes de rodar,
atualize as URLs em `data.py` **ou** exporte as variáveis de ambiente:

```bash
export URBAN_SCOOTER_URL="https://cnt-novo-id....containerhub.tripleten-services.com/order?lng=pt"
export URBAN_SCOOTER_API_URL="https://cnt-novo-id....containerhub.tripleten-services.com"
```

## Instalação

```bash
pip install -r requirements.txt
```

Também é necessário ter o [ChromeDriver](https://chromedriver.chromium.org/) compatível
com sua versão do Chrome no PATH (ou usar `webdriver-manager`, se preferir).

## Rodando os testes

```bash
# Todos os testes de API
pytest test_api_courier.py -v

# Todos os testes web
pytest codtestertroti.py -v

# Tudo
pytest -v
```

## Publicando no GitHub

```bash
git add .
git commit -m "Automação de testes Web (Selenium) e API (requests/pytest) - Urban Scooter"
git remote add origin <URL_DO_SEU_REPOSITORIO_GITHUB>
git push -u origin master
```
