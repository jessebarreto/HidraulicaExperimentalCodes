
import utils.data_parser as parser
import metrology.metrology as metrology

EXPERIMENT_DATA_FILEPATH = "data/dados_atividade_1_vertedores.csv"
EXPERIMENT_AUXDATA_FILEPATH = "data/dados_atividade_1_largura_do_canal.csv"

OUTPUT_FILEPATH = "data/resultados_atividade_1.csv"

# Retorna velocidade do escoamento
# Args
def eq_velocidade_escoamento(variaveis:list) -> float:
    """Calcula a velocidade de escoamento
    
    :param m: Nmr de rotacoes do molinete por tempo (adimensional)
    :return velocidade do escoamento (m/s)
    """
    m = variaveis[0]
    if m < 6.47:
        return 0.0562 * m + 0.038
    else:
        return 0.0545 * m + 0.049
    
def der_velocidade_escoamento_m(variaveis:list) -> float:
    m = variaveis[0]
    if m < 6.47:
        return 0.0562
    else:
        return 0.0545


def eq_velocidade_rotacoes_molinete(variaves:list) -> float:
    nmr_rotacoes = variaves[0]
    tempo = variaves[1]
    return nmr_rotacoes / tempo

def der_velocidade_rotacoes_molinete_nmr(variaves:list) -> float:
    #  nmr_rotacoes = variaves[0]
    tempo = variaves[1]
    return 1 / tempo

def der_velocidade_rotacoes_molinete_tempo(variaves:list) -> float:
    nmr_rotacoes = variaves[0]
    tempo = variaves[1]
    return -nmr_rotacoes / tempo**2


def prepare_measurements(measurements:dict, key:str, unit:str) -> None:
    if key not in measurements:
        return
    
    for index in range(0,len(measurements[key])):
            measurements[key][index] = metrology.convert_str_to_measurement(measurements[key][index], unit)
        

def calculate_variable(variable_name:str, measurement_names:list, measurements:dict, calculator:metrology.MeasurementRelationship) -> None:
    measurements[variable_name] = []
    for i in range(0, len(measurements[measurement_names[0]])):
        list_input_measurement = []
        for measurement_name in measurement_names:
            list_input_measurement.append(measurements[measurement_name][i])
        measurements[variable_name].append(calculator.calculate(list_input_measurement))


def main():
    cota_fundo_do_canal = metrology.MeasurementData(-0.095, 0.005, "cm")
    cota_soleira_vertedor = metrology.MeasurementData(15.095, 0.005, "cm")
    nmr_helice_molinete = 1
    mmr_molinete = 14538

    rows = parser.parse_data(EXPERIMENT_DATA_FILEPATH)

    measurements = parser.convert_csv_to_measurements_as_str(rows)
    prepare_measurements(measurements, "COTA SEÇÃO MOLINETE (mm)", "mm")
    prepare_measurements(measurements, "COTA SEÇÃO  VERTEDOR (mm)", "mm")
    prepare_measurements(measurements, "NR. ROTAÇÕES MOLINETE", "")
    prepare_measurements(measurements, "TEMPO (S)", "s")

    # Item a)
    vel_rot_molinete_calculator = metrology.MeasurementRelationship("rps", eq_velocidade_rotacoes_molinete, [der_velocidade_rotacoes_molinete_nmr, der_velocidade_rotacoes_molinete_tempo])
    calculate_variable("VELOCIDADE ROTAÇÕES MOLINETE (RPS)", ["NR. ROTAÇÕES MOLINETE", "TEMPO (S)"], measurements, vel_rot_molinete_calculator)

    # Item b)
    vel_escoamento_calculator = metrology.MeasurementRelationship("m/s", eq_velocidade_escoamento, [der_velocidade_escoamento_m])
    calculate_variable("VELOCIDADE ESCOAMENTO (m/s)", ["VELOCIDADE ROTAÇÕES MOLINETE (RPS)"], measurements, vel_escoamento_calculator)

    # Save everything in a csv
    parser.write_data(OUTPUT_FILEPATH, metrology.write_measurements_as_csv(measurements, ";"))

if __name__ == "__main__":
    main()