import datetime
import tkinter as tk
import tkinter.messagebox
from enum import Enum, auto

import customtkinter
from tkcalendar import Calendar

from controller import *
from models import Holiday

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class FrameEnum(Enum):
    EMPLOYEES = auto()
    HOLIDAYS = auto()
    CATEGORIES = auto()


class App(customtkinter.CTk):

    WIDTH = 1280
    HEIGHT = 960

    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.title("Евиденција броја радних дана запослених")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.employees = self.controller.get_all_employees()
        self.categories = self.controller.get_all_categories()
        self.active_frame = FrameEnum.EMPLOYEES
        self.start_date = None
        self.end_date = None
        self.frames = {
            FrameEnum.EMPLOYEES: {
                "actions": (
                    self._show_employees_frame,
                    self._hide_employees_frame,
                ),
                "confirm": self.add_new_employee,
            },
            FrameEnum.CATEGORIES: {
                "actions": (
                    self._show_categories_frame,
                    self._hide_categories_frame,
                ),
                "confirm": self.add_new_category,
            },
            FrameEnum.HOLIDAYS: {
                "actions": (
                    self._show_holidays_frame,
                    self._hide_holidays_frame,
                ),
                "confirm": self.add_new_holiday,
            },
        }
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=180, corner_radius=0
        )
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(
            0, minsize=10
        )  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(
            8, minsize=20
        )  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(
            11, minsize=10
        )  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(
            master=self.frame_left,
            text="Евиденција г. одмора",
            text_font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_employees = customtkinter.CTkButton(
            master=self.frame_left,
            text="Запослени",
            command=lambda: self.show(FrameEnum.EMPLOYEES),
        )
        self.button_employees.grid(row=2, column=0, pady=10, padx=20)

        self.button_holidays = customtkinter.CTkButton(
            master=self.frame_left,
            text="Годишњи одмор",
            command=lambda: self.show(FrameEnum.HOLIDAYS),
        )
        self.button_holidays.grid(row=3, column=0, pady=10, padx=20)

        self.button_categories = customtkinter.CTkButton(
            master=self.frame_left,
            text="Категорије",
            command=lambda: self.show(FrameEnum.CATEGORIES),
        )
        self.button_categories.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(
            master=self.frame_left, text="Appearance Mode:"
        )
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(
            master=self.frame_left,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode,
        )
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure(7, weight=1)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ frame_right ============

        self.combobox_employees = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=[str(e) for e in self.employees] or ["Немате унетих запослених"],
        )
        self.combobox_employees.grid(
            row=1, column=0, columnspan=2, pady=10, padx=20, sticky="we"
        )

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Унос категорије: ",
            text_font=("Roboto Medium", -16),
            anchor="w",
        )
        self.label_3.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            sticky="wesn",
        )

        self.combobox_categories = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=[category.name for category in self.categories]
            or ["Немате унетих категорија"],
        )
        self.combobox_categories.grid(
            row=3, column=0, columnspan=2, pady=10, padx=20, sticky="we"
        )

        self.label_2 = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Унос новог запосленог: ",
            text_font=("Roboto Medium", -16),
            anchor="w",
        )  # font name and size in px
        self.label_2.grid(row=0, column=0, columnspan=2, padx=20, sticky="we")

        self.entry_employe_name = customtkinter.CTkEntry(
            master=self.frame_right,
            width=120,
            placeholder_text="Име и презиме новог запосленог",
        )
        self.entry_employe_name.grid(
            row=1, column=0, columnspan=2, pady=10, padx=20, sticky="we"
        )
        self.entry_number_of_holidays = customtkinter.CTkEntry(
            master=self.frame_right,
            width=120,
            placeholder_text="Број дана",
        )
        self.entry_number_of_holidays.grid(
            row=2, column=0, columnspan=2, pady=10, padx=20, sticky="we"
        )

        self.button_confirm = customtkinter.CTkButton(
            master=self.frame_right,
            width=20,
            text="Потврди",
            command=self.confirm,
        )
        self.button_confirm.grid(
            row=5,
            column=0,
            pady=20,
            padx=20,
            sticky="we",
        )

        self.entry_category = customtkinter.CTkEntry(
            master=self.frame_right,
            width=120,
            placeholder_text="Назив категорије",
        )

        self.entry_category.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=10,
            padx=20,
            sticky="wesn",
        )

        self.button_from = customtkinter.CTkButton(
            master=self.frame_right,
            text="Датум од",
            command=lambda: self.show_calendar(self.button_from, True),
        )
        self.button_from.grid(
            row=4,
            column=0,
            pady=20,
            padx=20,
            sticky="we",
        )

        self.button_to = customtkinter.CTkButton(
            master=self.frame_right,
            width=20,
            text="Датум до",
            command=lambda: self.show_calendar(self.button_to, False),
        )
        self.button_to.grid(
            row=4,
            column=1,
            pady=20,
            padx=20,
            sticky="we",
        )

        # set default values
        self.optionmenu_1.set("Dark")
        self._hide_employees_frame()
        self._hide_categories_frame()
        self.show(FrameEnum.HOLIDAYS)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def confirm(self):
        self.frames[self.active_frame]["confirm"]()

    def add_new_employee(self):
        # TODO: Add validations for input
        first_name, last_name = self.entry_employe_name.get().split(" ")

        employee = Employee(
            first_name, last_name, int(self.entry_number_of_holidays.get()), []
        )

        self.controller.add_new_employee(employee)

        self._refresh_employees_combobox()

    def _refresh_employees_combobox(self):
        self.combobox_employees.configure(
            values=[str(e) for e in self.controller.get_all_employees()]
        )

    def add_new_category(self):
        # TODO: Add validations for input
        category = self.entry_category.get()
        self.controller.add_new_category(category)
        self.combobox_categories.configure(
            values=[category.name for category in self.controller.get_all_categories()]
        )

    def add_new_holiday(self):
        # TODO: Add validations for input
        # Find selected employee
        first_name, last_name = self.combobox_employees.get().split(",")[0].split(" ")
        employee = list(
            filter(
                lambda e: e.first_name == first_name and e.last_name == last_name,
                self.employees,
            )
        )[0]
        category = str(self.combobox_categories.get())
        employee.add_new_holiday(Holiday(self.start_date, self.end_date, category))
        self.controller.update_employee(employee)
        self._clear_new_holiday_inputs()
        self.combobox_employees.set(employee)

    def on_closing(self, event=0):
        self.destroy()

    def show(self, frame_name):
        if self.active_frame and self.active_frame == frame_name:
            return
        self._hide_active_frame()
        self._show_frame(frame_name)

    def _show_frame(self, frame_name):
        self.active_frame = frame_name
        self.frames[frame_name]["actions"][0]()

    def _hide_active_frame(self):
        self.frames[self.active_frame]["actions"][1]()

    def _show_employees_frame(self):
        self.entry_employe_name.grid()
        self.entry_number_of_holidays.grid()
        self.label_2.configure(text="Унос новог запосленог:")

    def _hide_employees_frame(self):
        self.entry_employe_name.grid_remove()
        self.entry_number_of_holidays.grid_remove()

    def _show_categories_frame(self):
        self.entry_category.grid()
        self.label_2.configure(text="Унос нове категорије годишњег одмора: ")

    def _hide_categories_frame(self):
        self.entry_category.grid_remove()

    def _show_holidays_frame(self):
        self.combobox_employees.grid()
        self.combobox_categories.grid()
        self.label_2.configure(text="Унос новог годишњег одмора:")
        self.label_3.grid()
        self.button_from.grid()
        self.button_to.grid()

    def _hide_holidays_frame(self):
        self.combobox_employees.grid_remove()
        self.combobox_categories.grid_remove()
        self.label_3.grid_remove()
        self.button_from.grid_remove()
        self.button_to.grid_remove()

    def show_calendar(self, button, start=True):
        def get_selected_date():
            date = calendar.selection_get()
            button.configure(text=str(date))
            if start:
                self.start_date = date
            else:
                self.end_date = date
            top.destroy()

        today = datetime.date.today()

        top = tk.Toplevel(self)

        calendar = Calendar(
            top,
            font="Arial 26",
            selectmode="day",
            year=today.year,
            month=today.month,
            day=today.day,
        )

        calendar.pack(fill="both", expand=True)
        customtkinter.CTkButton(
            master=top,
            width=20,
            text="OK",
            command=get_selected_date,
        ).pack()

    def _clear_new_holiday_inputs(self):
        self.button_from.configure(text="Датум од")
        self.button_to.configure(text="Датум до")
        self._refresh_employees_combobox()


if __name__ == "__main__":
    app = App()
    app.mainloop()
