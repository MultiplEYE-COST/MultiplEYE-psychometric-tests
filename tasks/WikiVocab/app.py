import argparse
import sys

from PyQt6.QtWidgets import QApplication

from welcome import MyWelcomeWindow


def window(result_folder: str) -> None:
    app = QApplication(sys.argv)
    win = MyWelcomeWindow(result_folder=result_folder)
    win.setWindowTitle("VocabTest")
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--participant_folder',
        type=str,
    )

    args = parser.parse_args()
    window(args.participant_folder)
