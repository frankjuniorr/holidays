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

  holidays_list.append(carnaval_event)
  holidays_list.append(semana_santa_event)

# ============================================
# Função que adiciona todos os feriados que tem data fixa.
# ============================================
def static_holidays(year):
    static_holidays_list = []

    # 1 de Janeiro
    static_holidays_list.append({"month": 1, "day": 1, "summary": "Ano Novo"})

    # 6 de Março
    static_holidays_list.append({"month": 3, "day": 6, "summary": "Carta Magna"})

    # 21 de Abril
    static_holidays_list.append({"month": 4, "day": 21, "summary": "Tiradentes"})

    # 1 de Maio
    static_holidays_list.append({"month": 5, "day": 1, "summary": "day do Trabalhador"})

    # 24 de Junho
    static_holidays_list.append({"month": 6, "day": 24, "summary": "São João"})

    # 16 de Julho
    static_holidays_list.append({"month": 7, "day": 16, "summary": "Nossa Senhora do Carmo"})

    # 7 de Setembro
    static_holidays_list.append({"month": 9, "day": 7, "summary": "Independência do Brasil"})

    # 12 de Outubro - Nossa Senhroa Aparecida
    static_holidays_list.append({"month": 10, "day": 12, "summary": "day das Crianças"})

    # 2 de Novembro
    static_holidays_list.append({"month": 11, "day": 2, "summary": "Finados"})

    # 15 de Novembro
    static_holidays_list.append({"month": 11, "day": 15,"summary": "Proclamação da República"})

    # 8 de Dezembro
    static_holidays_list.append({"month": 12, "day": 8,"summary": "Nossa Senhora da Conceição"})

    # 25 de Dezembro
    static_holidays_list.append({"month": 12, "day": 25, "summary": "Natal"})

    # adicionando todos os feriados d euma vez
    for index in range(len(static_holidays_list)):
      month = static_holidays_list[index]["month"]
      day = static_holidays_list[index]["day"]
      summary = static_holidays_list[index]["summary"]

      holiday_event = controller.add_holiday(year, month, day, summary)
      if holiday_event != None:
        holidays_list.append(holiday_event)


# ============================================
# Função Main
# ============================================
def main():

    print("Buildind holidays")
    year = controller.get_year()

    # ================ Feriados Dinâmicos ================
    dinamic_holidays(year)

    # ================ Feriados Estáticos ================
    static_holidays(year)

    events_list = controller.create_events_list(holidays_list)
    calendar = controller.create_calendar(events_list)

    print("Saving .ics file")
    controller.save_file(calendar)

    print("Sendind Email")
    total_holidays = len(holidays_list)
    controller.send_email(total_holidays)

if __name__ == '__main__':

    holidays_list = []
    main()
