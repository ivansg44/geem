def synthesize_day_integer_from_day_2_digit(col_components):
    def helper(day_dd):
        if day_dd:
            return day_dd.lstrip('0')
        return day_dd
    return [helper(day_dd) for day_dd in col_components['day_dd']]


dispatcher = {
    'day - integer': {
        'day - 2 digit': synthesize_day_integer_from_day_2_digit
    }
}
