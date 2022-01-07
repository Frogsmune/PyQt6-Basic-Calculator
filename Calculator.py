import sys
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

ERROR_MSG = "ERROR"

class PyCalcUi(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.result=QLineEdit()
        self.result.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.result.setReadOnly(True)
        self.buttons={}
        buttons={
           "(": (1,0),
           ")": (1, 1),
           "=": (5, 0),
           "1": (2, 0),
           "2": (2, 1),
           "3": (2, 2),
           "4": (3, 0),
           "5": (3, 1),
           "6": (3, 2),
           "7": (4, 0),
           "8": (4, 1),
           "9": (4, 2),
           "0": (5, 2),
           "00": (5, 1),
           "-": (2, 3),
           "+": (1, 3),
           "/": (3, 3),
           "*": (4, 3),
           "C/Del": (1, 2),
           ".": (5, 3)
        }
        self.mainLayout=QVBoxLayout(self)
        grid = QGridLayout()
        grid.addWidget(self.result, 0, 0, 1, 4)
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            grid.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.mainLayout.addLayout(grid)
        self.mainLayout.addStretch()

        self.setLayout(grid)
        self.setFixedSize(280, 190)
        self.setWindowTitle('Calculator')
    def setDisplayText(self, text):
        self.result.setText(text)
        self.result.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.result.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText("")

def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result

# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    """PyCalc's Controller."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {"=", "C"}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons["="].clicked.connect(self._calculateResult)
        self._view.result.returnPressed.connect(self._calculateResult)
        self._view.buttons["C/Del"].clicked.connect(self._view.clearDisplay)

# Client code
def main():
    """Main function."""
    # Create an instance of `QApplication`
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyCalcUi()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    # Execute calculator's main loop
    sys.exit(pycalc.exec())


if __name__ == "__main__":
    main()
