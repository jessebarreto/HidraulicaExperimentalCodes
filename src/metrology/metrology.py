import typing
import math


class MeasurementData:
    def __init__(self, value: float, error: float, unit: str) -> None:
        self.value = value
        self.error = error
        self.unit = unit

    def __str__(self) -> str:
        return "{} ± {}".format(str(self.value), str(self.error))

    def relative_error(self) -> float:
        return self.error / self.value


class MeasurementRelationship:
    def __init__(
        self,
        unit: str,
        equation_fn: typing.Callable[[typing.List[float]], float],
        derivatives: typing.List[typing.Callable[[typing.List[float]], float]],
    ) -> None:
        self.equation_ = equation_fn
        self.derivatives_ = derivatives
        self.unit = unit

    def calculate(self, measurements: typing.List[MeasurementData]) -> MeasurementData:
        def most_significant_digit(x: float) -> float:
            return round(x, -int(math.floor(math.log10(abs(x)))))

        def error_propagation(
            values: typing.List[float],
            errors: typing.List[float],
            derivatives: typing.List[typing.Callable[[typing.List[float]], float]],
        ) -> float:
            if len(errors) != len(values) or len(errors) != len(derivatives):
                raise ValueError(
                    "Length of lists values, errors and derivatives are not equal"
                )

            error_propagated = 0.0
            for error, derivative in zip(errors, derivatives):
                term = (derivative(values) * error) ** 2
                error_propagated = error_propagated + term

            error_propagated = math.sqrt(error_propagated)
            return error_propagated

        if len(measurements) != len(self.derivatives_):
            raise ValueError("Invalid number of input measurements")

        values = []
        errors = []
        for measurement in measurements:
            values.append(measurement.value)
            errors.append(measurement.error)

        error = most_significant_digit(
            error_propagation(values, errors, self.derivatives_)
        )
        significant_digit = abs(math.floor(math.log10(error)))
        value = round(self.equation_(values), significant_digit)
        return MeasurementData(value, error, self.unit)


def is_str_measurement(measurement_as_str: str) -> bool:
    return measurement_as_str.find("+/-") or measurement_as_str.find("±")


def convert_str_to_measurement(
    measurement_as_str: str, unit: str = ""
) -> MeasurementData:
    if not is_str_measurement(measurement_as_str):
        raise ValueError("Given str is not a measurement")

    info = []
    if measurement_as_str.find("±") != -1:
        info = measurement_as_str.split("±")
    else:
        info = measurement_as_str.split("/")
        for index in range(0, len(info)):
            info[index] = info[index].strip(" +-")

    for index in range(0, len(info)):
        if info[index].find(","):
            info[index] = info[index].replace(",", ".")
            info[index] = info[index].strip("\"'")

    if len(info) < 2:
        raise ValueError("Given str could not be splitted correctly")

    return MeasurementData(float(info[0]), float(info[1]), unit)


def write_measurements_as_csv(
    measurements: typing.Dict[str, typing.List[MeasurementData]], csv_separator: str
) -> typing.List[str]:
    csv_data = []

    headers = []
    for key in measurements.keys():
        headers.append('"{}"'.format(key))
    csv_data.append(";".join(headers))

    n_rows = len(list(measurements.values())[0])
    for row_index in range(n_rows):
        row = []
        for key in measurements.keys():
            row.append('"{}"'.format(measurements[key][row_index].__str__()))
        csv_data.append(";".join(row))

    return csv_data
