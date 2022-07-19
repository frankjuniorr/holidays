import datetime
import math
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from icalendar import Calendar, Event

# ============================================
# Função que calcula a data da páscoa,
# segundo o algoritmo de
# Jean Baptiste Joseph Delambre (1749-1822)
# link: (http://www.ghiorzi.org/portug2.htm)
# ============================================
def calculate_pascoa(ano):
    pascoa_day = pascoa_month = a = b = c = d = e = f = g = h = i = k = l = m = p = q = None

    a = math.trunc(ano % 19)
    b = math.trunc(ano / 100)
    c = math.trunc(ano % 100)
    d = math.trunc(b / 4)
    e = math.trunc(b % 4)
    f = math.trunc((b + 8) / 25)
    g = math.trunc((b - f + 1) / 3)
    h = math.trunc((19*a + b - d - g + 15) % 30)
    i = math.trunc(c / 4)
    k = math.trunc(c % 4)
    l = math.trunc((32 + 2*e + 2*i - h - k) % 7)
    m = math.trunc((a + 11*h + 22*l) / 451)
    p = math.trunc((h + l - 7*m + 114) / 31)
    q = math.trunc((h + l - 7*m + 114) % 31)

    pascoa_day = q+1
    pascoa_month = p

    return datetime.date(ano, pascoa_month, pascoa_day)

# ============================================
# Função auxiliar que retorna o ano corrente
# ============================================
def get_year():
    DECEMBER = 12

    year = datetime.datetime.now().year

    # se eu rodar esse script no mês de dezembro, ele incrementa o 'ano'
    # e já adiciona os feriados do ano seguinte.
    month = datetime.datetime.now().month
    if month == DECEMBER:
      year = year + 1

    return year

# ============================================
# Função auxiliar que verifica se o feriado é
# diferente de sabado e domingo.
#
# return: dictionary - datas
# ============================================
def holiday_check(holiday_date):
  dates = start_date = end_date = None
  feriado_day = holiday_date.strftime("%A")

  # se não for sabado e domingo, adicione
  if feriado_day != 'Saturday' and feriado_day != 'Sunday':
    if feriado_day == 'Monday' or feriado_day == 'Wednesday' or feriado_day == 'Friday':

      start_date = holiday_date
      end_date = holiday_date

    # quinta-feira é feriado emendado
    elif feriado_day == 'Thursday':
      # esse "dia a mais" é necessaŕio, pq o "end-date" não é inclusive, é "exclusive" na Api do Google
      friday = holiday_date + datetime.timedelta(days=2)

      start_date = holiday_date
      end_date = friday

    # terça-feria é feriado emendado
    elif feriado_day == 'Tuesday':
      monday = holiday_date - datetime.timedelta(days=1)
      # esse "dia a mais" é necessaŕio, pq o "end-date" não é inclusive, é "exclusive" na Api do Google
      tuesday = holiday_date + datetime.timedelta(days=1)

      start_date = monday
      end_date = tuesday

  dates = {"start_date": start_date, "end_date": end_date}
  return dates

# ============================================
def get_environment_variables(env_var_name):
    """
    Get Environment Variables from system
    """
    EXIT_ERROR = 1
    env_var = None
    try:
        env_var = os.environ[env_var_name]
    except:
        print(f"Fill the {env_var_name} environment var fisrt")
        sys.exit(EXIT_ERROR)

    return env_var


# ============================================
# Create Event() object
# ============================================
def _create_event(holiday_date):
    event = Event()
    event.add('summary', holiday_date["summary"])
    event.add('dtstart', holiday_date["startDate"])
    event.add('dtend', holiday_date["endDate"])

    return event


# ============================================
# Create Calendar() object
# ============================================
def create_calendar(events_list):
    calendar = Calendar()

    for event in events_list:
      calendar.add_component(event)

    return calendar

# ============================================
# Create a list with Event() objects
# ============================================
def create_events_list(holidays_list):
    events_list = []
    for event in holidays_list:
        event = _create_event(event)
        events_list.append(event)

    return events_list

# ============================================
# Create .ics file
# ============================================
def save_file(calendar):
    year = get_year()
    file_name = f"holidays_{year}.ics"

    with open(file_name, 'wb') as file:
        file.write(calendar.to_ical())


# ============================================
# Função que adiciona a data do carnaval
# ============================================
def add_carnaval(pascoa_date):
    carnaval_inicio = pascoa_date - datetime.timedelta(days=51)
    carnaval_fim = carnaval_inicio + datetime.timedelta(days=6)

    holiday_date = {
        "summary": "[FERIADO] Carnaval",
        "startDate": carnaval_inicio,
        "endDate": carnaval_fim,
    }

    return holiday_date

# ============================================
# Função que adiciona a data da Semana Santa
# ============================================
def add_semana_santa(pascoa_date):
    # a 'pascoa_date' sempre cai no domingo,
    # logo, o feriado é sempre na sexta antes, por isso é -2 dias
    semana_santa = pascoa_date - datetime.timedelta(days=2)

    holiday_date = {
    "summary": "[FERIADO] Semana Santa",
    "startDate": semana_santa,
    "endDate": semana_santa,
    }

    return holiday_date


# ============================================
# Função genérica que adiciona qualquer feriado
# ============================================
def add_holiday(ano, mes, dia, summary):

  feriado = datetime.date(ano, mes, dia)
  holiday_dates = holiday_check(feriado)

  if holiday_dates["start_date"] != None:
    holiday_date = {
        "summary": f"[FERIADO] {summary}",
        "startDate": holiday_dates["start_date"],
        "endDate": holiday_dates["end_date"],
    }

    return holiday_date

# ============================================
# Função que envia o email, baseado em alguns valores em variáveis de ambiente.
# Recebendo o 'total_holidays' como parãmetro para incrementar no body do email.
# ============================================
def send_email(total_holidays):
    year = get_year()
    server = 'smtp.gmail.com'
    port = 587

    email_from = get_environment_variables("EMAIL_FROM")
    email_to = get_environment_variables("EMAIL_TO")
    email_password = get_environment_variables("EMAIL_APP_PASSWORD")

    email_subject = f"All Holidays {year}"
    body = f"""
    <html>
        <body>
            <p>
            Hello,<br>
            Here is all holidays of <b>{year}</b><br>
            Total Holidays: <b>{total_holidays}</b><br><br>

            For more information, see the <a href="https://github.com/frankjuniorr/holidays">source code</a>
            </p>
        </body>
        </html>
    """

    message = MIMEMultipart()
    message["Subject"] = email_subject
    message["From"] = email_from
    message["To"] = email_to

    message.add_header("Content-Type", "text/html")
    message.attach(MIMEText(body, "html"))

    file_name = f"holidays_{year}.ics"
    with open(file_name, "rb") as file:
        attachment = MIMEApplication(file.read(), Name=file_name)

    attachment['Content-Disposition'] = f'attachment; filename="{file_name}"'
    message.attach(attachment)

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(email_from, email_password)

    smtp.sendmail(email_from, email_to, message.as_string().encode('utf-8'))
    smtp.close()
    print("Email sent")


