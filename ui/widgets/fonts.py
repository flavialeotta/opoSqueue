from PySide6.QtGui import QFontDatabase, QFont

class CustomFont():
    def __init__(self, tff_path, size=12):
        self.font_id = QFontDatabase.addApplicationFont(tff_path)
        
        # Safety check: if font_id is -1, the file wasn't found/loaded
        if self.font_id == -1:
            print(f"Warning: Could not load font at {tff_path}")
            self.pixel_font = QFont("Courier", size) # Fallback font
            return

        families = QFontDatabase.applicationFontFamilies(self.font_id)
        if families:
            self.font_family = families[0]
            self.pixel_font = QFont(self.font_family, size)
        else:
            self.pixel_font = QFont("Courier", size)