# Trotiurban: Test Automation (Urban Scooter)

Final project for the TripleTen QA program. Automated Python tests covering both
the UI and the API of the same business flow:

- **Task 1 (Web)**: UI tests with Selenium on the "Who is the scooter for" form (`codtestertroti.py` + `cod_troti.py`).
- **Task 3 (API)**: API tests with `requests` + `pytest` for the Add/Delete courier endpoints (`test_api_courier.py`).

## Structure

| File | Role |
|---|---|
| `data.py` | Server URLs and test data (Page Object Model / config) |
| `helpers.py` | Utility functions (check if server is up, generate unique login) |
| `cod_troti.py` | Page Object for the web form (`UrbanScooterOrderPage`) |
| `codtestertroti.py` | Selenium tests (Task 1) |
| `test_api_courier.py` | API tests (Task 3) |

## Known bugs (marked with `@pytest.mark.xfail`)

Several tests document bugs already reported in Jira (JSQ-1 to JSQ-17) and are marked
as `xfail`: they describe the **correct** expected behavior, so they fail on purpose
while the bug remains unfixed. When `XPASS` shows up during a run, it means the bug
has been fixed and the `xfail` can be removed from the test.

## Configuration

The TripleTen test servers expire after 2h of inactivity. Before running the tests,
update the URLs in `data.py` **or** export the environment variables:

```bash
export URBAN_SCOOTER_URL="https://cnt-novo-id....containerhub.tripleten-services.com/order?lng=pt"
export URBAN_SCOOTER_API_URL="https://cnt-novo-id....containerhub.tripleten-services.com"
```

## Installation

```bash
pip install -r requirements.txt
```

You also need a [ChromeDriver](https://chromedriver.chromium.org/) compatible with
your Chrome version on the PATH (or use `webdriver-manager`, if you prefer).

## Running the tests

```bash
# All API tests
pytest test_api_courier.py -v

# All web tests
pytest codtestertroti.py -v

# Everything (the project's pytest.ini tells pytest to recognize codtestertroti.py
# as a test file, since its name doesn't follow the test_*.py pattern)
pytest -v
```

## Code quality

```bash
pip install -r requirements-dev.txt
black --check .
flake8 .
```

CI (GitHub Actions, in `.github/workflows/lint.yml`) runs `black --check` and
`flake8` on every push/PR. It doesn't run the actual tests in CI because they
depend on a TripleTen sandbox server that expires after 2h of inactivity (see the
"Configuration" section above), so running them in CI would only make sense with
an active server at the time.

## Publishing to GitHub

```bash
git add .
git commit -m "Web (Selenium) and API (requests/pytest) test automation - Urban Scooter"
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin master
```
