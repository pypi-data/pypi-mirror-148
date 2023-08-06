"""
    Module for interacting with the Gab.com website.
"""

# pylint: disable=too-many-arguments

import os
import ssl
import tempfile
import time
from typing import Optional

from autoselenium import Driver  # type: ignore

# black from .download import download_file
from download import download  # type: ignore
from pyjpgclipboard import clipboard_load_jpg  # type: ignore
from selenium.webdriver.common.action_chains import ActionChains  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore

ssl._create_default_https_context = (  # pylint: disable=protected-access
    ssl._create_unverified_context  # pylint: disable=protected-access
)

# Width and height need to be this value in order for the gab sign in to
# work.
WIDTH = 1200
HEIGHT = 800

TIMEOUT_IMAGE_UPLOAD = 60  # Wait upto 60 seconds to upload the image.


def _action_login(driver: Driver, username: str, password: str) -> None:
    """Logs into Gab.com and posts the given content."""
    driver.delete_all_cookies()  # Delete any cookies, otherwise sign in breaks.
    driver.set_window_size(WIDTH, HEIGHT)  # Yes this is needed tool, or it breaks.
    # Handle Page sign in, where the user and password are entered.
    driver.get("https://gab.com/auth/sign_in")
    el_email = driver.find_element_by_id("user_email")
    el_email.click()
    el_email.send_keys(username)
    el_password = driver.find_element_by_id("user_password")
    el_password.click()
    el_password.send_keys(password)
    el_submit_btn = driver.find_element_by_name("button")
    el_submit_btn.click()


def _action_make_post(
    driver: Driver,
    content: str,
    jpg_path: Optional[str] = None,
    dry_run: Optional[bool] = False,
) -> None:
    """Makes a social media post"""
    driver.get("https://gab.com/compose")
    el_compose_window = driver.find_element_by_css_selector("div.DraftEditor-root")
    el_compose_window.click()
    # Now use the keyboard to enter in the content.
    actions = ActionChains(driver)
    actions.send_keys(content)
    actions.perform()
    # Upload the image if it's been specified.
    if jpg_path is not None:
        # Copy the image to the clipboard and then paste it into the post.
        if "http" in jpg_path:
            # download the image url to a local temp file and then put it on the clipboard.
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                try:
                    temp.close()
                    download(jpg_path, temp.name)
                    clipboard_load_jpg(temp.name)
                finally:
                    os.remove(temp.name)
        else:
            clipboard_load_jpg(jpg_path)
        # Send a paste command to the keyboard.
        actions = ActionChains(driver)
        actions.key_down(Keys.META)
        actions.send_keys("v")
        actions.perform()
        timeout = time.time() + TIMEOUT_IMAGE_UPLOAD
        while True:
            try:
                # Wait for the image to upload.
                # Find the element with the xpath that includes an image source
                driver.find_element_by_xpath(
                    '//img[contains(@src, "media_attachments")]'
                )
                break
            except Exception:  # pylint: disable=broad-except
                if time.time() > timeout:
                    print(
                        f"{__file__}: Failed to upload image, because timed out waiting for "
                        "{jpg_path} to upload"
                    )
                    break
                time.sleep(0.5)
    # Perform the post action.
    # Find an element that contains "Post"
    el_post_btn = driver.find_element_by_xpath('//*[contains(text(), "Post")]')
    # put the mouse over the button of el_post_btn and click it.
    actions = ActionChains(driver)
    actions.move_to_element(el_post_btn)
    actions.click()
    if not dry_run:
        actions.perform()


def gab_post(
    username: str,
    password: str,
    content: str,
    jpg_path: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    """Logs into Gab.com and posts the given content."""
    # Note that we must use the firefox driver. For some reason the chrome driver
    # skips the sign in page and causes an error to occure.
    with Driver("firefox", root="drivers") as driver:
        _action_login(driver, username, password)
        _action_make_post(driver, content, jpg_path=jpg_path, dry_run=dry_run)
