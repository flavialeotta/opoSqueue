import sys
import asyncio

from PySide6.QtWidgets import QApplication

from qasync import QEventLoop

from ui.windows.title_screen import TitleScreen


async def main():
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = TitleScreen()
    window.resize(480, 320)
    window.show()

    

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
    