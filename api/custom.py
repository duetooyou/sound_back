from rest_framework.serializers import Field
from calendar import month_abbr


class MonthField(Field):
    def to_representation(self, value):
        if value:
            return f"{month_abbr[value]}"
        return value


class YearField(Field):
    def to_representation(self, value):
        return str(value)
