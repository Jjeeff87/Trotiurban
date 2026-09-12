import os

# ==========================================================
# Server configuration, Task 1 (Web / Place order)
# ==========================================================
# The TripleTen test server expires after 2h of inactivity.
# Every time the server is restarted, update the URL below OR export the
# URBAN_SCOOTER_URL environment variable before running the tests:
#   export URBAN_SCOOTER_URL="https://cnt-novo-id....containerhub.tripleten-services.com/order?lng=pt"  # noqa: E501
URBAN_SCOOTER_URL = os.getenv(
    "URBAN_SCOOTER_URL",
    "https://cnt-b1de1780-a68d-4e53-b822-08dd98be58ad.containerhub.tripleten-services.com"
    "/order?lng=pt",
)

# Valid test data for the "Who is the scooter for" form
FIRST_NAME = "Maria"
LAST_NAME = "Silva"
ADDRESS = "Rua Augusta, 123"
METRO_STATION_SEARCH = "1st"
METRO_STATION_EXPECTED = "1st Street"
PHONE_NUMBER = "+12345678901"  # 12 characters, within the documented limit

# Data used in the negative tests / known bug tests
ADDRESS_INVALID_CHAR = "Rua Augusta #123"
ADDRESS_MAX_LENGTH_50 = "a" * 50
NAME_WITH_ACCENT = "José"
PHONE_MIN_LENGTH_10 = "+123456789"  # 10 chars, should be accepted (BUG JSQ-3)
PHONE_ABOVE_MAX_13 = "+123456789012"  # 13 chars, should be rejected (BUG JSQ-4)
PHONE_BOUNDARY_11 = "+1234567890"  # 11 chars, inconsistent visual state (BUG JSQ-5)

# Border colors used by the application to indicate a valid/invalid field
VALID_BORDER_COLOR = "rgb(26, 27, 34)"
INVALID_BORDER_COLOR = "rgb(253, 110, 112)"


# ==========================================================
# API configuration, Task 3 (Backend / Couriers)
# ==========================================================
# Just like the web server, the API server expires after 2h of inactivity.
# Update the URL below or export URBAN_SCOOTER_API_URL before running the tests.
API_BASE_URL = os.getenv(
    "URBAN_SCOOTER_API_URL",
    "https://cnt-83d97b55-2300-4985-837d-f369c65e2b33.containerhub.tripleten-services.com",
)

VALID_PASSWORD = "1234"
