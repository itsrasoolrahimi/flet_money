import flet as ft
from server.datetime_farsi import DatetimeFarsi
from server.google_sheet_handler import GoogleSheetHandler

last_digit = None


class UserInput(ft.Container):
    def __init__(self, page: ft.Page):

        super().__init__()
        self.alignment = ft.alignment.center
        # self.bgcolor = "blue"
        self.expand = True

        self.money_pic = ft.Image(
            src="/pictures/money.png",
            width=280
        )

        def format_money_input(e):
            global last_digit
            raw_money_input = str(self.money_input.value.replace(",", ""))
            if str(last_digit) == str(raw_money_input[1:]) and len(raw_money_input) > 4:
                raw_money_input = raw_money_input[1:] + raw_money_input[0]

            formatted_money_digit = '{:,}'.format(int(raw_money_input))
            self.money_input.value = str(formatted_money_digit)
            self.money_input.update()
            last_digit = raw_money_input

        self.money_input = ft.TextField(
            cursor_width=0,
            width=300,
            height=60,
            border_color="white",
            hint_text="قیمت را به تومان وارد کنید",
            border_radius=20,
            text_align=ft.TextAlign.CENTER,
            on_change=format_money_input
        )
        self.hour_input = ft.TextField(
            width=100,
            height=60,
            border_color="white",
            hint_text="ساعت",
            border_radius=20,
            text_align=ft.TextAlign.CENTER
        )
        self.colon_text = ft.Text(
            value=":",
            weight=ft.FontWeight.BOLD,
        )
        self.minute_input = ft.TextField(
            width=100,
            height=60,
            border_color="white",
            hint_text="دقیقه",
            border_radius=20,
            text_align=ft.TextAlign.CENTER
        )
        self.time_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.hour_input,
                self.colon_text,
                self.minute_input
            ]
        )

        self.withdrawal = ft.Text(
            value="برداشت",
            weight=ft.FontWeight.BOLD,
            size=20,
            color="red"
        )

        def switch_change(e):
            if self.action_type_switch.value:
                self.withdrawal.color = "white"
                self.deposit.color = "green"
            else:
                self.withdrawal.color = "red"
                self.deposit.color = "white"
            page.update()

        self.action_type_switch = ft.Switch(
            active_color="green",
            inactive_thumb_color="red",
            inactive_track_color="#661825",
            on_change=switch_change,
        )

        self.deposit = ft.Text(
            value="واریز",
            weight=ft.FontWeight.BOLD,
            size=20
        )

        self.action_type_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.withdrawal,
                self.action_type_switch,
                self.deposit
            ]
        )

        self.title = ft.TextField(
            width=200,
            height=60,
            border_color="white",
            hint_text="عنوان",
            border_radius=20,
            text_align=ft.TextAlign.CENTER,
            rtl=True
        )

        self.description = ft.TextField(
            width=300,
            # height=60,
            multiline=True,
            min_lines=1,
            max_lines=3,
            border_color="white",
            hint_text="... توضیح",
            border_radius=20,
            text_align=ft.TextAlign.CENTER,
            rtl=True
        )
        self.add_finance_button = ft.ElevatedButton(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(value="ثبت اطلاعات", size=20),
                ]
            ),
            style=ft.ButtonStyle(
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=20)
                }
            ),
            color="white",
            bgcolor="green",
            width=200,
            height=50,
            on_click=self.add_finance_data,
        )
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.money_pic,
                            ft.Container(height=20),
                            self.money_input,
                            self.time_row,
                            self.action_type_row,
                            self.title,
                            self.description,
                            ft.Container(height=5),
                            self.add_finance_button
                        ]
                    )
                )
            ]
        )

    def add_finance_data(self, e):
        datetime_farsi = DatetimeFarsi()
        today_persian_name = datetime_farsi.today_day_name()
        today_persian_date = datetime_farsi.today_date()


        google_sheet_handler = GoogleSheetHandler()
        adding_time = self.hour_input.value + ":" + self.minute_input.value

        money = self.money_input.value

        if self.action_type_switch.value:
            transaction_type = "واریز"
        else:
            transaction_type = "برداشت"

        title = self.title.value

        description = self.description.value

        google_sheet_handler.add_data(
            data_list=[
                today_persian_name,
                today_persian_date,
                adding_time,
                money,
                transaction_type,
                title,
                description
            ]
        )

        self.money_input.value = ""
        self.hour_input.value = ""
        self.minute_input.value = ""
        self.title.value = ""
        self.description.value = ""

        dlg = ft.AlertDialog(
            title=ft.Text("ثبت موفقیت آمیز")
        )
        self.page.dialog = dlg
        dlg.open = True

        self.page.update()
