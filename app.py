# ##############################################################################
# [Descrição]:
#   Script que cria um arquivo de calendário (.ics) com todos os feriados do ano corrente (baseado nos feriados de Recife-PE).
#   Uma vez o arquivo gerado, importe manualmente no seu Google Calendar
#     OBS: Ele só adiciona os feriados que não caem no sábado ou domingo.
#     OBS2: O script também adiciona o carnaval e Semana Santa\o/
#
# [Uso]:
#   ./app.py
# ##############################################################################

import controller

# ============================================
# Função que adiciona todos os feriados que tem data dinâmica
# ============================================
def dinamic_holidays(year):
  pascoa_date = controller.calculate_pascoa(year)

  # Adicionando o Carnaval
  carnaval_event = controller.add_carnaval(pascoa_date)

  # Adicionando a Semana Santa
  semana_santa_event = controller.add_semana_santa(pascoa_date)

  events_list.append(carnaval_event)
  events_list.append(semana_santa_event)

# ============================================
# Função que adiciona todos os feriados que tem data fixa.
# ============================================
def static_holidays(year):
    holidays_list = []

    # 1 de Janeiro
    holidays_list.append({"mes": 1, "dia": 1, "summary": "Ano Novo"})

    # 6 de Março
    holidays_list.append({"mes": 3, "dia": 6, "summary": "Carta Magna"})

    # 21 de Abril
    holidays_list.append({"mes": 4, "dia": 21, "summary": "Tiradentes"})

    # 1 de Maio
    holidays_list.append({"mes": 5, "dia": 1, "summary": "Dia do Trabalhador"})

    # 24 de Junho
    holidays_list.append({"mes": 6, "dia": 24, "summary": "São João"})

    # 16 de Julho
    holidays_list.append({"mes": 7, "dia": 16, "summary": "Nossa Senhora do Carmo"})

    # 7 de Setembro
    holidays_list.append({"mes": 9, "dia": 7, "summary": "Independência do Brasil"})

    # 12 de Outubro - Nossa Senhroa Aparecida
    holidays_list.append({"mes": 10, "dia": 12, "summary": "Dia das Crianças"})

    # 2 de Novembro
    holidays_list.append({"mes": 11, "dia": 2, "summary": "Finados"})

    # 15 de Novembro
    holidays_list.append({"mes": 11, "dia": 15,"summary": "Proclamação da República"})

    # 8 de Dezembro
    holidays_list.append({"mes": 12, "dia": 8,"summary": "Nossa Senhora da Conceição"})

    # 25 de Dezembro
    holidays_list.append({"mes": 12, "dia": 25, "summary": "Natal"})

    # adicionando todos os feriados d euma vez
    for index in range(len(holidays_list)):
      mes = holidays_list[index]["mes"]
      dia = holidays_list[index]["dia"]
      summary = holidays_list[index]["summary"]

      holiday_event = controller.add_feriado(year, mes, dia, summary)
      if holiday_event != None:
        events_list.append(holiday_event)


# ============================================
# Função Main
# ============================================
def main():

    print(" ========= Addind holidays =========")
    year = controller.get_year()

    # # ================ Feriados Dinâmicos ================
    dinamic_holidays(year)

    # # ================ Feriados Estáticos ================
    static_holidays(year)

    calendar = controller.create_calendar(events_list)

    print(" ========= saving .ics file =========")
    controller.save_file(calendar)

if __name__ == '__main__':

    events_list = []
    main()
