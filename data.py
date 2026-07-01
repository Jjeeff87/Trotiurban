import os

# ==========================================================
# Configuração do servidor — Tarefa 1 (Web / Fazer pedido)
# ==========================================================
# O servidor de teste (TripleTen) expira após 2h de inatividade.
# Toda vez que reiniciar o servidor, atualize a URL abaixo OU exporte a
# variável de ambiente URBAN_SCOOTER_URL antes de rodar os testes:
#   export URBAN_SCOOTER_URL="https://cnt-novo-id....containerhub.tripleten-services.com/order?lng=pt"
URBAN_SCOOTER_URL = os.getenv(
    "URBAN_SCOOTER_URL",
    "https://cnt-b1de1780-a68d-4e53-b822-08dd98be58ad.containerhub.tripleten-services.com/order?lng=pt",
)

# Dados de teste válidos para o formulário "Para quem é a scooter"
FIRST_NAME = "Maria"
LAST_NAME = "Silva"
ADDRESS = "Rua Augusta, 123"
METRO_STATION_SEARCH = "1st"
METRO_STATION_EXPECTED = "1st Street"
PHONE_NUMBER = "+12345678901"  # 12 caracteres — dentro do limite documentado

# Dados usados nos testes negativos / de bugs conhecidos
ADDRESS_INVALID_CHAR = "Rua Augusta #123"
ADDRESS_MAX_LENGTH_50 = "a" * 50
NAME_WITH_ACCENT = "José"
PHONE_MIN_LENGTH_10 = "+123456789"       # 10 chars — deveria ser aceito (BUG JSQ-3)
PHONE_ABOVE_MAX_13 = "+123456789012"     # 13 chars — deveria ser rejeitado (BUG JSQ-4)
PHONE_BOUNDARY_11 = "+1234567890"        # 11 chars — estado visual inconsistente (BUG JSQ-5)

# Cores de borda usadas pela aplicação para indicar campo válido/inválido
VALID_BORDER_COLOR = "rgb(26, 27, 34)"
INVALID_BORDER_COLOR = "rgb(253, 110, 112)"


# ==========================================================
# Configuração da API — Tarefa 3 (Backend / Couriers)
# ==========================================================
# Assim como o servidor web, o servidor da API expira após 2h de inatividade.
# Atualize a URL abaixo ou exporte URBAN_SCOOTER_API_URL antes de rodar os testes.
API_BASE_URL = os.getenv(
    "URBAN_SCOOTER_API_URL",
    "https://cnt-83d97b55-2300-4985-837d-f369c65e2b33.containerhub.tripleten-services.com",
)

VALID_PASSWORD = "1234"
