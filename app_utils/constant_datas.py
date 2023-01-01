year_months_en = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
year_months_short_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def days_per_month_calculator(year):
    default = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if not year % 4:
        default[1] = 29
    return default
