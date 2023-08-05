class ProcessEmployee:

    def __init__(self, employee):
        self.employee = employee

    def validate_employee_to_receive_msg(self):

        if self.employee.get_last_birthday_notification != self.employee.get_current_date:
            if self.employee.has_started_working:
                if self.employee.is_still_working:
                    if self.employee.can_receive_wishes:
                        if self.employee.is_today_celebration_day:
                            return True
        return False
