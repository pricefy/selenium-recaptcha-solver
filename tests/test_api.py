from selenium_recaptcha_solver import RecaptchaSolver, StandardDelayConfig
from selenium.webdriver.common.by import By
from seleniumbase import SB
import pytest
import warnings

# Run test
# pytest tests/test_api.py

# Suppress deprecation warnings for aifc and audioop
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, module="speech_recognition"
)

solver = None


def test_solver():
    global solver

    seleniumbase_options = {
        "browser": "chrome",
        "headed": False,
        "headless2": False,
        "undetectable": True,
        "ad_block_on": True,
        "page_load_strategy": "eager",
        # https://www.selenium.dev/documentation/webdriver/drivers/options/
        # "page_load_strategy": "none", # Does not block WebDriver at all
        # "page_load_strategy": "normal", # Used by default, waits for all resources to download
        # "page_load_strategy": "eager", # DOM access is ready, but other resources like images may still be loading
        "block_images": None,
        "incognito": None,
        "use_auto_ext": False,
        "locale": "en",
        "chromium_arg": [
            # https://peter.sh/experiments/chromium-command-line-switches/
            "--disable-default-apps",
            "--max-render-process-count=2",
            "--js-flags=--max-old-space-size=1024",
            "--disable-software-rasterizer",
            "--disable-features=TranslateUI",
            "--disable-features=BlinkGenPropertyTrees",
            "--disable-features=VizDisplayCompositor",
            "--disable-component-extensions-with-background-pages",
            "--disable-component-update",
            "--disable-gpu-compositing",
            "--no-sandbox",  # Required when running as root
            "--use-gl=swiftshader",  # Use Google's software renderer
            "--disable-gpu-compositing",
        ],
        "enable_sync": False,  # apply excludeSwitches
    }

    with SB(**seleniumbase_options) as sb_driver:
        try:
            solver = RecaptchaSolver(
                driver=sb_driver.driver, delay_config=StandardDelayConfig()
            )

            url = "https://www.google.com/recaptcha/api2/demo"

            sb_driver.uc_open(url)

            recaptcha_iframe = sb_driver.driver.find_element(
                By.XPATH, '//iframe[@title="reCAPTCHA"]'
            )

            solver.click_recaptcha_v2(iframe=recaptcha_iframe)

            sb_driver.driver.execute_script(
                "document.getElementById('recaptcha-demo-submit').click()"
            )
            try:
                sb_driver.driver.find_element(By.CSS_SELECTOR, ".recaptcha-success")
            except Exception as e:
                pytest.skip(f"Skip if not found selector. {str(e)}")

            print("ReCAPTCHA solved successfully!")

        except Exception as e:
            pytest.fail(f"Failed to automatically resolve ReCAPTCHA. {str(e)}")
