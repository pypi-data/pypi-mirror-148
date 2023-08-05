from src.utils.operation                        import Operation as ops


class Employee:
    _current_date = ops.get_today_date()

    def __init__(self, employee_info, excluded_employees):
        self.excluded_employees    = excluded_employees
        self.emp_id                = employee_info.get('id')
        self.name                  = employee_info.get('name')
        self.last_name             = employee_info.get('lastname')
        self.date_of_birth         = employee_info.get('dateOfBirth')
        self.emp_start_date        = employee_info.get('employmentStartDate')
        self.emp_end_date          = employee_info.get('employmentEndDate')
        self.last_notification     = employee_info.get('lastNotification')
        self.last_birth_notified   = employee_info.get('lastBirthdayNotified')
        self.dob                   = ops.str_to_date(self.date_of_birth)       if self.date_of_birth       else None
        self.__emp_start_date      = ops.str_to_date(self.emp_start_date)      if self.emp_start_date      else None
        self.__emp_end_date        = ops.str_to_date(self.emp_end_date)        if self.emp_end_date        else None
        self.__last_notification   = ops.str_to_date(self.last_notification)   if self.last_notification   else None
        self.__last_birth_notified = ops.str_to_date(self.last_birth_notified) if self.last_birth_notified else None

    @property
    def get_current_date(self):
        return self._current_date

    @property
    def is_still_working(self):
        if self.__emp_end_date:
            if self._current_date > self.__emp_end_date:
                return True
            return False
        return True

    @property
    def is_today_celebration_day(self):
        return (self._current_date.month == self.dob.month and self._current_date.day == self.dob.day)

    @property
    def has_started_working(self):
        return self.__emp_start_date and self._current_date >= self.__emp_start_date

    @property
    def can_receive_wishes(self):
        return self.emp_id not in self.excluded_employees

    @property
    def get_employment_dob(self):
        return self.dob

    @property
    def get_employment_start_date(self):
        return self.__emp_start_date

    @property
    def get_employment_end_date(self):
        return self.__emp_end_date

    @property
    def get_last_notification(self):
        return self.__last_notification

    @property
    def get_last_birthday_notification(self):
        return self.__last_notification
