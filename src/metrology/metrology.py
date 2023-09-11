

class MeasurementData:
    def __init__(self, value:float, error:float, unit:str) -> None:
        self.value = value
        self.error = error
        self.unit = unit

    def __str__(self):
        return "MeasurementData {}".format(str(self.__dict__))


def is_str_measurement(measurement_as_str:str) -> bool:
    return measurement_as_str.find("+/-") or measurement_as_str.find("±")    


def convert_str_to_measurement(measurement_as_str:str, unit:str = "") -> MeasurementData:
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

    if (len(info) < 2):
        raise ValueError("Given str could not be splitted correctly")
    
    return MeasurementData(str(info[0]), str(info[1]), unit)
