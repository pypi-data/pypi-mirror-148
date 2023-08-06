import pathlib

TEMPLATES_DIR: pathlib.Path = (
    pathlib.Path(__file__).resolve(strict=True).parent / "templates"
)
APP_TEMPLATES_DIR: pathlib.Path = TEMPLATES_DIR / "app_template"

PROJECT_TEMPLATE_URL_BASIC: pathlib.Path = TEMPLATES_DIR / "basic_project_template"
PROJECT_TEMPLATE_URL_MEDIOR: pathlib.Path = TEMPLATES_DIR / "medior_project_template"
PROJECT_TEMPLATE_URL_ADVANCED: pathlib.Path = (
    TEMPLATES_DIR / "advanced_project_template"
)
