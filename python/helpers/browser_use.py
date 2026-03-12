from python.helpers import dotenv
dotenv.save_dotenv_value("ANONYMIZED_TELEMETRY", "false")
try:
    import browser_use
    import browser_use.utils
except ImportError:
    browser_use = None  # type: ignore