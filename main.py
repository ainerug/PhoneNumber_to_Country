import sys
import phonenumbers
import pytz
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox


class PhoneInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create widgets
        label = QLabel('Enter phone number (including country code):')
        self.number_input = QLineEdit()
        self.country_output = QLabel()
        self.time_output = QLabel()
        self.error_output = QLabel()

        check_button = QPushButton('Check')
        check_button.clicked.connect(self.check_number)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.number_input)
        layout.addWidget(check_button)
        layout.addWidget(self.country_output)
        layout.addWidget(self.time_output)
        layout.addWidget(self.error_output)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Phone Info')
        self.setGeometry(100, 100, 400, 200)
        self.show()

    def check_number(self):
        # Get phone number from input
        number_str = self.number_input.text()

        # Parse phone number and check if it's valid
        try:
            number = phonenumbers.parse(number_str, None)
            if not phonenumbers.is_valid_number(number):
                raise Exception('Invalid phone number')
        except phonenumbers.phonenumberutil.NumberParseException:
            self.error_output.setText('Invalid phone number')
            return

        # Get country name
        from phonenumbers import geocoder
        country_name = geocoder.description_for_number(number, 'en')
        self.country_output.setText('Country: {}'.format(country_name))

        # Get time zone and local time
        from phonenumbers import timezone
        time_zone = timezone.time_zones_for_number(number)[0]
        local_time = pytz.timezone(time_zone).localize(datetime.now())
        self.time_output.setText('Local time: {}'.format(local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PhoneInfoWidget()
    sys.exit(app.exec_())
