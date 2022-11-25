import datetime
from dataclasses import dataclass

from dateutil import parser

DATE_FORMAT = "%-d-%-m-%Y"


class JSONSerializable:
    def toJSON(self):
        return self.__dict__


@dataclass
class Holiday(JSONSerializable):
    id: int
    start_date: datetime.date
    end_date: datetime.date
    category: str

    def __init__(self, start_date, end_date, category, id=None) -> None:
        if isinstance(start_date, str):
            self.start_date = parser.parse(start_date)
        else:
            self.start_date = start_date

        if isinstance(end_date, str):
            self.end_date = parser.parse(end_date)
        else:
            self.end_date = end_date
        self.id = id
        self.category = category

    def __str__(self) -> str:
        return f"{self.start_date} - {self.end_date} [{self.category}]"

    def _daterange(self, start_date, end_date):
        """Generator of daterange function.
        Here we add 1 because we want to include end_date

        Args:
            start_date (_type_): _description_
            end_date (_type_): _description_

        Yields:
            _type_: _description_
        """
        for n in range(int((end_date - start_date).days + 1)):
            yield start_date + datetime.timedelta(n)

    def calculate_days(self, start_date, end_date):
        working_days = 0
        for single_date in self._daterange(start_date, end_date):
            weekday = single_date.weekday()
            if weekday != 5 and weekday != 6:
                working_days += 1
            # TODO: Here we will check if the specified date
            #       is in non working vacation days. If it is
            #       we will not increase working days

        return working_days

    def toJSON(self):
        return dict(
            start_date=self.start_date.strftime(DATE_FORMAT),
            end_date=self.end_date.strftime(DATE_FORMAT),
            category=self.category,
        )


@dataclass
class Employee(JSONSerializable):
    id: int
    first_name: str
    last_name: str
    number_of_holidays_left: int
    holidays: list[Holiday]

    def __init__(
        self, first_name, last_name, number_of_holidays_left, holidays, id=None
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.number_of_holidays_left = number_of_holidays_left
        if (
            isinstance(holidays, list)
            and len(holidays) > 0
            and isinstance(holidays[0], Holiday)
        ):
            self.holidays = holidays
        else:
            self.holidays = [Holiday(**h) for h in holidays]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, бр. дана {self.number_of_holidays_left}"

    def add_new_holiday(self, holiday: Holiday):
        holiday_days = holiday.calculate_days(holiday.start_date, holiday.end_date)
        if self.number_of_holidays_left < holiday_days:
            raise ValueError("Немате толико слободних дана")
        self.holidays.append(holiday)
        self.number_of_holidays_left -= holiday_days

    def toJSON(self):
        if self.__dict__["holidays"]:
            self.__dict__["holidays"] = [h.toJSON() for h in self.__dict__["holidays"]]
        return self.__dict__


@dataclass
class Category(JSONSerializable):
    id: int
    name: str

    def __init__(self, name, id=None) -> None:
        self.name = name
        self.id = id
