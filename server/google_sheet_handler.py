import gspread

class GoogleSheetHandler:
    def add_data(self, data_list):
        sa = gspread.service_account(filename="server/rasool_data_api.json")
        sh = sa.open("Rasool_data")

        wks = sh.worksheet("personal_finance")

        new_list = data_list
        wks.append_row(new_list, table_range="A1:G1")

