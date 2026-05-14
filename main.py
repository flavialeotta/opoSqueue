import sys
import asyncio

from PySide6.QtWidgets import QApplication

from qasync import QEventLoop

from ui.windows.title_screen import TitleScreen


async def main():
    app = QApplication(sys.argv)
    window = TitleScreen()
    window.show()

    while True:
        app.processEvents()
        await asyncio.sleep(0.01)
        
        # Check our custom flag OR if the X was clicked
        if window.should_exit or not window.isVisible():
            break
    
    # After the loop breaks, we force the cleanup
    app.quit()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("Opossum is going to sleep. Goodbye!")

    