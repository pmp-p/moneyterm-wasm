# /// pyproject
# [project]
# name = "moneyterm-test"
# version = "2024"
# description = "TUI Expense and Budget Tracker"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
#  "six",
#  "bs4",
#  "markdown-it-py",
#  "pygments",
#  "rich",
#  "mdurl",
#  "textual",
#  "ofxparse",
#  "plotext",
#  "textual-plotext",
#  "dateutil",
# ]
# ///

# python-dateutil


import pygbag.aio as asyncio

import asyncio
import textual
import pickle

from pathlib import Path


import moneyterm
import moneyterm.screens
import moneyterm.screens.tabbedcontentscreen

import moneyterm.utils.ledger


class MoneyTerm(textual.app.App):
    """Finance dashboard TUI."""

    LEDGER = moneyterm.utils.ledger.Ledger()
    CSS_PATH = "moneyterm/tcss/moneyterm.tcss"
    BINDINGS = []
    SCREENS = {"tabbedcontent": moneyterm.screens.tabbedcontentscreen.TabbedContentScreen(LEDGER)}

    def __init__(self) -> None:
        super().__init__()
        self.LEDGER.read_ledger_pkl()

    def on_mount(self) -> None:
        """Mount the app."""
        self.push_screen("tabbedcontent")


async def main():
    loop = asyncio.get_event_loop()
    app = MoneyTerm()

    try:
        if sys.platform in ("emscripten", "wasi"):
            for f in Path(".").glob("*.whl"):
                os.unlink(f)
            print(" ===================================== ")
            async with app.run_test(headless=True, size=(100, 32)) as pilot:
                while not loop.is_closed():
                    await asyncio.sleep(0.016)
        else:
            await app.run_async()

    except asyncio.exceptions.CancelledError:
        print("Cancelled")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        pass


asyncio.run(main())
