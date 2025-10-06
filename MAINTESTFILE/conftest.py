# MAINTESTFILE/conftest.py
import os
import datetime
import subprocess
import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait

# Adjust this import to where your BaseTest actually lives
try:
    from Test.BaseTest import BaseTest
except ImportError:
    from Test import BaseTest


# ---------- Helpers ----------
def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
    return path

def _timestamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def _safe_nodeid(nodeid: str):
    return nodeid.replace("::", "__").replace("/", "_").replace("\\", "_")

# ---------- Session-wide logging ----------
def pytest_configure(config):
    base_dir = _ensure_dir(os.path.join(os.getcwd(), "reports"))
    logs_dir = _ensure_dir(os.path.join(base_dir, "logs"))
    # session log file (captures everything)
    sess_path = os.path.join(logs_dir, f"session-{_timestamp()}.log")

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # Avoid duplicate handlers if reloaded
    if not any(isinstance(h, logging.FileHandler) and getattr(h, "_is_session", False) for h in root.handlers):
        fh = logging.FileHandler(sess_path, encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"))
        fh._is_session = True  # mark so we don't add twice
        root.addHandler(fh)

@pytest.fixture(scope="class")
def driver(request):
    """
    Primary fixture: creates Appium driver and returns it.
    Works with tests that accept a `driver` parameter and/or use self.driver.
    """
    base = BaseTest()
    drv = base.driver
    assert drv is not None, "BaseTest().driver is None — check your BaseTest init"
    request.cls.driver = drv
    yield drv
    try:
        drv.quit()
    except Exception:
        pass

@pytest.fixture(scope="class")
def driver_setup(request, driver):
    """
    Backward-compatible alias for files that use `@pytest.mark.usefixtures("driver_setup")`
    and expect self.driver / self.wait to exist.
    """
    request.cls.driver = driver
    request.cls.wait = WebDriverWait(driver, 10)
    yield
    # teardown handled by `driver` fixture


# ---------- Per-test logging handlers ----------
def pytest_runtest_setup(item):
    """Create a per-test file handler and attach to root logger."""
    base_dir = _ensure_dir(os.path.join(os.getcwd(), "reports"))
    logs_dir = _ensure_dir(os.path.join(base_dir, "logs"))
    safe_name = _safe_nodeid(item.nodeid)
    log_file = os.path.join(logs_dir, f"{safe_name}.log")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"))

    root = logging.getLogger()
    root.addHandler(fh)

    # stash for later removal/attachment
    item._log_file = log_file
    item._log_handler = fh

def pytest_runtest_teardown(item):
    """Remove/close the per-test file handler."""
    fh = getattr(item, "_log_handler", None)
    if fh:
        root = logging.getLogger()
        try:
            root.removeHandler(fh)
        except Exception:
            pass
        try:
            fh.close()
        except Exception:
            pass


# ---------- Artifacts on failure (screenshots, page source, logcat, attach logs) ----------
def _dump_logcat(drv, out_path):
    """
    Try to grab Android logcat via Appium; fall back to adb if available.
    """
    text = ""
    # 1) Appium logcat
    try:
        entries = drv.get_log("logcat")
        if isinstance(entries, list):
            text = "\n".join(e.get("message", "") for e in entries)
    except Exception:
        pass

    # 2) adb fallback
    if not text:
        try:
            raw = subprocess.check_output(["adb", "logcat", "-d"], timeout=8)
            text = raw.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    if text:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On test failure, save screenshot + page source + logcat and attach logs to pytest-html.
    Also attach the per-test log file link and a short tail inline.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when not in ("setup", "call"):
        return

    failed = report.failed
    if hasattr(report, "wasxfail"):
        failed = failed or report.skipped
    if not failed and not hasattr(item, "_log_file"):
        return

    # Collect driver
    drv = None
    if "driver" in item.funcargs:
        drv = item.funcargs["driver"]
    elif hasattr(item, "instance"):
        drv = getattr(item.instance, "driver", None)

    # Build paths
    base_dir = _ensure_dir(os.path.join(os.getcwd(), "reports"))
    shots_dir = _ensure_dir(os.path.join(base_dir, "screenshots"))
    src_dir = _ensure_dir(os.path.join(base_dir, "pagesource"))
    logs_dir = _ensure_dir(os.path.join(base_dir, "logs"))
    safe_name = _safe_nodeid(report.nodeid)
    ts = _timestamp()
    png_path = os.path.join(shots_dir, f"{safe_name}__{report.when}__{ts}.png")
    src_path = os.path.join(src_dir, f"{safe_name}__{report.when}__{ts}.xml")
    logcat_path = os.path.join(logs_dir, f"{safe_name}__logcat__{report.when}__{ts}.txt")
    per_test_log = getattr(item, "_log_file", None)

    # Save screenshot & page source on failure
    if failed and drv is not None:
        try:
            drv.save_screenshot(png_path)
        except Exception:
            pass
        try:
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(drv.page_source)
        except Exception:
            pass
        # logcat
        try:
            _dump_logcat(drv, logcat_path)
        except Exception:
            pass

    # Attach to pytest-html (if present)
    extras = getattr(report, "extra", [])
    try:
        from pytest_html import extras as html_extras

        # Screenshot inline
        if failed and os.path.exists(png_path):
            extras.append(html_extras.png(png_path))

        # Links to page source & logcat
        if failed and os.path.exists(src_path):
            extras.append(html_extras.url(src_path, name="Page Source"))
        if failed and os.path.exists(logcat_path):
            extras.append(html_extras.url(logcat_path, name="Logcat"))

        # Link the per-test log file (always useful)
        if per_test_log and os.path.exists(per_test_log):
            extras.append(html_extras.url(per_test_log, name="Test Log"))

            # Also embed a short tail for quick viewing
            try:
                with open(per_test_log, "r", encoding="utf-8") as f:
                    tail = "".join(f.readlines()[-200:])
                if tail:
                    extras.append(html_extras.text(tail, name="Test Log (last 200 lines)"))
            except Exception:
                pass

        report.extra = extras
    except Exception:
        report.extra = extras
