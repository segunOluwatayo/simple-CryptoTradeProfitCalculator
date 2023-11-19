'''
UPDATED VERSION - 2022
JLEBRON / B. FOGARTY
Please make sure you use the PEP guide for naming conventions in your submission
- detailed guide: https://www.python.org/dev/peps/pep-0008/
- some examples: https://stackoverflow.com/questions/159720/what-is-the-naming-convention-in-python-for-variable-and-function-names

This assignment is heavily based on
A Currency Converter GUI Program - Python PyQt5 Desktop Application Development Tutorial
- GitHub: https://github.com/DarBeck/PyQT5_Tutorial/blob/master/currency_converter.py
- YouTube: https://www.youtube.com/watch?v=weKpTw1SjM4 - detailed explanaton
- Keep in mind this example uses PyQt5 not PyQt6

- Layout
    - I would suggest QGridLayout
    - Use a QCalendarWidget which you will get from Zetcode tutorial called "Widgets" https://zetcode.com/pyqt6/widgets/

PyCharm Configuration Options
- Viewing Documentation when working with PyCharm https://www.jetbrains.com/help/pycharm/viewing-external-documentation.html
- Configuring Python external Documenation on PyCharm https://www.jetbrains.com/help/pycharm/settings-tools-python-external-documentation.html
'''

# TODO: Delete the above, and include in a comment your name and student number
# TODO: Remember to fully comment your code
# TODO: Include a comment 'EXTRA FEATURE' and explain what your Extra Feature does
# TODO: Don't forget to document your design choices in your UI Design Document


# standard imports
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, \
    QPushButton
from PyQt6 import QtCore


class CryptoTradeProfitCalculator(QDialog):
    '''
    Provides the following functionality:

    - Allows the selection of the Crypto Coin to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    - Additional functionality

    '''

    def __init__(self):
        '''
        This method requires substantial updates
        Each of the widgets should be suitably initalized and laid out
        '''
        super().__init__()

        # setting up dictionary of Crypto Coins
        self.data = self.make_data()
        # sorting the dictionary of Crypto Coins by the keys. The keys at the high level are dates, so we are sorting by date
        self.stocks = sorted(self.data.keys())

        # Create an instance of QGridLayout
        self.layout = QGridLayout()

        # Set the layout to the dialog
        self.setLayout(self.layout)

        # Set the font for the whole widget
        font = QFont("Helvetica", 12)
        self.setFont(font)

        # Create a QPushButton for reset and set its style
        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("""
                    QPushButton { 
                   background-color: #007BFF; 
                   color: white; 
                   font-family: Helvetica; 
                   font-size: 18px; 
                   font-weight: bold; }
                    QPushButton { background-color: #007BFF; color: white; }
                    QPushButton:hover { background-color: #0056b3; }
                    QPushButton:pressed { background-color: #003f80; }
                """)
        self.layout.addWidget(self.reset_button, 7, 1, 2, 3)

        # Create QComboBox for CryptoCurrency and set its border
        self.crypto_combo = QComboBox()
        self.crypto_combo.setStyleSheet("QComboBox { border: 2px solid gray; border-radius: 10px; }")

        # # Set the background color of the whole window
        self.setStyleSheet("background-color: #72bcd4;")

        # Connect the button's clicked signal to the reset slot
        self.reset_button.clicked.connect(self.resetFields)

        # -------- EXAMPLE --------

        # the following lines of code are for debugging purposes and show you how to access the self.data to get dates and prices
        # TODO: uncomment to print all the dates and close prices for BTC
        print("all the dates and close prices for BTC", self.data['BTC'])
        # print the close price for BTC on 04/29/2013
        print("the close price for BTC on 04/29/2013", self.data['BTC'][QDate(2013, 4, 29)])

        # The data in the file is in the following range
        #     first date in dataset - 29th Apr 2013
        #     last date in dataset - 6th Jul 2021
        # When the calendars load we want to ensure that the default dates selected are within the date range above
        #     we can do this by setting variables to store suitable default values for sellCalendar and buyCalendar.
        self.sellCalendarDefaultDate = sorted(self.data['BTC'].keys())[-1]
        # Accessing the last element of a python list is explained with method 2 on https://www.geeksforgeeks.org/python-how-to-get-the-last-element-of-list/
        print("self.sellCalendarStartDate", self.sellCalendarDefaultDate)
        # self.buyCalendarDefaultDate = ???
        # print("self.buyCalendarStartDate", self.buyCalendarDefaultDate)

        # -------- END OF EXAMPLE --------

        # TODO: create QLabel for CryptoCurrency purchased
        # create a QLabel widget with the text "CryptoCurrency purchased:"
        self.crypto_label = QLabel("CryptoCurrency purchased:")

        # TODO: create QComboBox and populate it with a list of CrytoCurrencies
        # create a QComboBox widget
        self.crypto_combo = QComboBox()
        # populate it with the list of cryptocurrencies stored in self.stocks
        self.crypto_combo.addItems(self.stocks)

        # TODO: create CalendarWidgets for selection of purchase and sell dates
        # create a QLabel widget with the text "Purchase Date:"
        self.purchase_date_label = QLabel("Purchase Date:")
        # create a QCalendarWidget widget for the purchase date
        self.purchase_calendar = QCalendarWidget()
        # set the default selected date to two weeks before the most recent date
        self.purchase_calendar.setSelectedDate(self.sellCalendarDefaultDate.addDays(-14))
        # create a QLabel widget with the text "Sell Date:"
        self.sell_date_label = QLabel("Sell Date:")
        # create a QCalendarWidget widget for the sell date
        self.sell_calendar = QCalendarWidget()
        # set the default selected date to the most recent date
        self.sell_calendar.setSelectedDate(self.sellCalendarDefaultDate)

        # TODO: create QSpinBox to select CryptoCurrency quantity purchased
        # create a QSpinBox widget
        self.quantity_spin = QSpinBox()
        # set the minimum and maximum values to 1 and 1000
        self.quantity_spin.setRange(1, 1000)
        # set the default value to 1
        self.quantity_spin.setValue(1)

        # TODO: create QLabels to show the CryptoCurrency purchase total
        # create a QLabel widget with the text "Purchase total:"
        self.purchase_label = QLabel("Purchase total:")
        # create a QLabel widget with the text "0.00"
        self.purchase_value = QLabel("0.00")

        # TODO: create QLabels to show the CryptoCurrency sell total
        # create a QLabel widget with the text "Sell total:"
        self.sell_label = QLabel("Sell total:")
        # create a QLabel widget with the text "0.00"
        self.sell_value = QLabel("0.00")

        # TODO: create QLabels to show the CryptoCurrency profit total
        # create a QLabel widget with the text "Profit total:"
        self.profit_label = QLabel("Profit total:")
        # create a QLabel widget with the text "0.00"
        self.profit_value = QLabel("0.00")

        # TODO: initialize the layout - 6 rows to start

        # row 0 - CrytoCurrency selection
        # add the crypto_label widget to the first row and first column of the layout
        self.layout.addWidget(self.crypto_label, 0, 0)
        # add the crypto_combo widget to the first row and second column of the layout
        self.layout.addWidget(self.crypto_combo, 0, 1)
        # align the widgets to the top of the layout
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # row 1 - quantity selection
        # add a QLabel widget with the text "Quantity purchased:" to the second row and first column of the layout
        self.layout.addWidget(QLabel("Quantity purchased:"), 1, 0)
        # add the quantity_spin widget to the second row and second column of the layout
        self.layout.addWidget(self.quantity_spin, 1, 1)

        # row 2 - purchase date selection
        # add the purchase_calendar widget to the third row and first column of the layout, and make it span one row and two columns
        self.layout.addWidget(self.purchase_calendar, 2, 0, 1, 2)
        # add the purchase_date_label widget to the third row and first column of the layout
        self.layout.addWidget(self.purchase_date_label, 2, 0)
        # add the purchase_calendar widget to the third row and second column of the layout, and make it span one row and two columns
        self.layout.addWidget(self.purchase_calendar, 2, 1, 1, 2)
        # row 3 - display purchase total
        # add the purchase_label widget to the fourth row and first column of the layout
        self.layout.addWidget(self.purchase_label, 3, 0)
        # add the purchase_value widget to the fourth row and second column of the layout
        self.layout.addWidget(self.purchase_value, 3, 1)

        # row 4 - sell date selection
        # add the sell_calendar widget to the fifth row and first column of the layout, and make it span one row and two columns
        self.layout.addWidget(self.sell_calendar, 4, 0, 1, 2)
        # add the sell_date_label widget to the fifth row and first column of the layout
        self.layout.addWidget(self.sell_date_label, 4, 0)
        # add the sell_calendar widget to the fifth row and second column of the layout, and make it span one row and two columns
        self.layout.addWidget(self.sell_calendar, 4, 1, 1, 2)

        # row 5 - display sell total
        self.layout.addWidget(self.sell_label, 5, 0)  # add the sell_label widget to the sixth row and first column of the layout
        self.layout.addWidget(self.sell_value, 5, 1)  # add the sell_value widget to the sixth row and second column of the layout

        # row 6 - display sell total
        # row 6 - display profit total
        # add the profit_label widget to the seventh row and first column of the layout
        self.layout.addWidget(self.profit_label, 6, 0)
        # add the profit_value widget to the seventh row and second column of the layout
        self.layout.addWidget(self.profit_value, 6, 1)

        # TODO: set the calendar values
        # purchase: two weeks before most recent
        # sell: most recent
        # set the minimum date for the purchase calendar to the first date in the data
        self.purchase_calendar.setMinimumDate(sorted(self.data['BTC'].keys())[0])
        # set the maximum date for the purchase calendar to one day before the most recent date
        self.purchase_calendar.setMaximumDate(self.sellCalendarDefaultDate.addDays(-1))
        # set the minimum date for the sell calendar to one day after the selected purchase date
        self.sell_calendar.setMinimumDate(self.purchase_calendar.selectedDate().addDays(1))
        # set the maximum date for the sell calendar to the most recent date
        self.sell_calendar.setMaximumDate(self.sellCalendarDefaultDate)

        # TODO: connecting signals to slots to that a change in one control updates the UI
        # connect the activated signal of the crypto_combo widget to the updateUi slot
        self.crypto_combo.activated.connect(self.updateUi)
        # connect the valueChanged signal of the quantity_spin widget to the updateUi slot
        self.quantity_spin.valueChanged.connect(self.updateUi)
        # connect the selectionChanged signal of the purchase_calendar widget to the updateUi slot
        self.purchase_calendar.selectionChanged.connect(self.updateUi)
        # connect the selectionChanged signal of the sell_calendar widget to the updateUi slot
        self.sell_calendar.selectionChanged.connect(self.updateUi)

        # TODO: set the window title
        # set the window title to "Cryptocurrency Profit Calculator"
        self.setWindowTitle(
            "Cryptocurrency Profit Calculator")
        # TODO: update the UI
        # TODO: update the UI
        self.updateUi()
        self.update()

    def resetFields(self):
        # Reset all fields to their initial states
        self.crypto_combo.setCurrentIndex(0)
        self.quantity_spin.setValue(1)
        self.purchase_calendar.setSelectedDate(self.sellCalendarDefaultDate.addDays(-14))
        self.sell_calendar.setSelectedDate(self.sellCalendarDefaultDate)
        self.updateUi()

    def updateUi(self):
        '''
        This requires substantial development
        Updates the Ui when control values are changed, should also be called when the app initializes
        :return:
        '''
        try:
            print("Update UI")
            # TODO: get selected dates from calendars
            # get the selected purchase date from the purchase_calendar widget
            purchase_date = self.purchase_calendar.selectedDate()
            # get the selected sell date from the sell_calendar widget
            sell_date = self.sell_calendar.selectedDate()

            # TODO: perform necessary calculations to calculate totals
            # get the selected cryptocurrency from the crypto_combo widget
            crypto = self.crypto_combo.currentText()
            # get the selected quantity from the quantity_spin widget
            quantity = self.quantity_spin.value()
            # get the purchase price from the data dictionary
            purchase_price = self.data[crypto][purchase_date]
            # get the sell price from the data dictionary
            sell_price = self.data[crypto][sell_date]
            # calculate the purchase total
            purchase_total = purchase_price * quantity
            # calculate the sell total
            sell_total = sell_price * quantity
            # calculate the profit total
            profit_total = sell_total - purchase_total

            # TODO: update the label displaying totals
            # update the purchase_value label with the formatted purchase total
            self.purchase_value.setText(f"{purchase_total:.2f}")
            # update the sell_value label with the formatted sell total
            self.sell_value.setText(f"{sell_total:.2f}")
            # update the profit_value label with the formatted profit total
            self.profit_value.setText(f"{profit_total:.2f}")
        except Exception as e:
            print(e)
            # set the purchase_value label to "N/A" if there is an error
            self.purchase_value.setText("N/A")
            # set the sell_value label to "N/A" if there is an error
            self.sell_value.setText("N/A")
            # set the profit_value label to "N/A" if there is an error
            self.profit_value.setText("N/A")



    ################ YOU DO NOT HAVE TO EDIT CODE BELOW THIS POINT  ########################################################

    def make_data(self):
        '''
        This code is complete
         Data source is derived from https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory but use the provided file to avoid confusion

         Stock   -> Date      -> Close
            BTC     -> 29/04/2013 -> 144.54
                    -> 30/04/2013 -> 139
                    .....
                    -> 06/07/2021 -> 34235.19345

                    ...

        Helpful tutorials to understand this
        - https://stackoverflow.com/questions/482410/how-do-i-convert-a-string-to-a-double-in-python
        - nested dictionaries https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
        - https://www.tutorialspoint.com/python3/python_strings.htm
        :return: a dictionary of dictionaries
        '''
        data = {}  # empty data dictionary (will store what we read from the file here)
        try:
            file = open("../Downloads/combined.csv", "r")  # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
            file_rows = []  # empty list of file rows
            # add rows to the file_rows list
            for row in file:
                file_rows.append(row.strip())  # https://www.geeksforgeeks.org/python-string-strip-2/
            print("**************************************************************************")
            print("combined.csv read successfully. Rows read from file: " + str(len(file_rows)))

            # get the column headings of the CSV file
            print("____________________________________________________")
            print("Headings of file:")
            row0 = file_rows[0]
            line = row0.split(",")
            column_headings = line
            print(column_headings)

            # get the unique list of CryptoCurrencies from the CSV file
            non_unique_cryptos = []
            file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
            for row in file_rows_from_row1_to_end:
                line = row.split(",")
                non_unique_cryptos.append(line[6])
            cryptos = self.unique(non_unique_cryptos)
            print("____________________________________________________")
            print("Total Currencies found: " + str(len(cryptos)))
            print(str(cryptos))

            # build the base dictionary of CryptoCurrencies
            for crypto in cryptos:
                data[crypto] = {}

            # build the dictionary of dictionaries
            for row in file_rows_from_row1_to_end:
                line = row.split(",")
                date = self.string_date_into_QDate(line[0])
                crypto = line[6]
                close_price = line[4]
                # include error handling code if close price is incorrect
                data[crypto][date] = float(close_price)
        except:
            print("Error: combined.csv file not found. ")
            print("Make sure you have imported this file into your project.")
        #return the data
        print("____________________________________________________")
        print("Amount of Currencies stored in data:", len(data)) #will be 0 if empty/error
        print("**************************************************************************")
        return data

    def string_date_into_QDate(self, date_String):
        '''
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        '''
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list


# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    currency_converter = CryptoTradeProfitCalculator()
    currency_converter.show()
    sys.exit(app.exec())
