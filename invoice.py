from simple_term_menu import TerminalMenu
import os, subprocess
import chevron
import datetime
import calendar

def main():
    template_dir = "./templates"
    result_dir = "./result"

    # # USER INPUT

    # choose customer invoice template
    templates = os.listdir(template_dir);
    terminal_menu = TerminalMenu(templates)
    input_customer_template = terminal_menu.show()

    # enter hourly rate
    input_hourly_rate = input("Enter hourly rate at " + templates[input_customer_template] + ": ")
    try:
        input_hourly_rate = float(input_hourly_rate)
    except ValueError:
        print("Hourly rate must be an integer or float value. Exiting.");
        exit(-1);

    # choose month
    date_options = ["last month", "actual month", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];
    terminal_menu = TerminalMenu(date_options)
    input_month = terminal_menu.show()
    if date_options[input_month] != 'last month' and date_options[input_month] != 'actual month':
        input_year = input(date_options[input_month] + " of what year?: ")
        try:
            input_year = int(input_year)
            year=input_year
            month=input_month-1
        except ValueError:
            print("Year must be an integer value. Exiting.");
            exit(-1);
    elif date_options[input_month] == 'last month':
            today = datetime.date.today()
            first_day_of_actual_month = today.replace(day=1)
            lastmonth = first_day_of_actual_month - datetime.timedelta(days=1)
            year = lastmonth.year
            month = lastmonth.month
    elif date_options[input_month] == 'actual month':
        today = datetime.date.today()
        year = today.year
        month = today.month
    first_day_of_the_month_date = datetime.datetime(year, month, 1, 12, 00, 00)
    last_day_of_the_month_date = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 12, 00, 00)

    # enter hours worked
    input_hours_worked = input("How many hours did you work for " + templates[input_customer_template] + " in " + last_day_of_the_month_date.strftime("%b %Y") + "?: ")
    try:
        input_hours_worked = float(input_hours_worked)
    except ValueError:
        print("Hourly rate must be an integer or float value. Exiting.");
        exit(-1);

    # # CALCULATIONS
    mustache_subtotal = input_hourly_rate * input_hours_worked
    mustache_taxes = mustache_subtotal / 5
    mustache_total = mustache_subtotal + mustache_taxes
    mustache_date = last_day_of_the_month_date.strftime("%d.%m.%Y")
    mustache_time_period_from_to = first_day_of_the_month_date.strftime("%d.%m.%Y") + " - " + last_day_of_the_month_date.strftime("%d.%m.%Y");
    mustache_invoice_id = last_day_of_the_month_date.strftime("%Y%m%d") + "-" + templates[input_customer_template]
    print(mustache_invoice_id)
    mustache_rate = input_hourly_rate
    mustache_hours = input_hours_worked

    chosen_template = templates[input_customer_template];
    chosen_template_dir = template_dir + "/" + chosen_template
    chosen_template_file = chosen_template_dir + "/Invoice.tex"
    rendered_template_file = result_dir + "/" + mustache_invoice_id

    # str(mustache_subtotal)
    with open(chosen_template_file, 'r') as f:
        result = chevron.render(f, {
                                'mustache_subtotal': str(mustache_subtotal),
                                'mustache_taxes': str(mustache_taxes),
                                'mustache_total': str(mustache_total),
                                'mustache_date': str(mustache_date),
                                'mustache_time_period_from_to': str(mustache_time_period_from_to),
                                'mustache_invoice_id': str(mustache_invoice_id),
                                'mustache_rate': str(mustache_rate),
                                'mustache_hours': str(mustache_hours)})
        with open(rendered_template_file, "wt") as w:
            w.write(result)

    # create file and clean up
    subprocess.call(["pdflatex", "-output-directory", "../../" + result_dir, mustache_invoice_id], cwd=chosen_template_dir, stdout=open(os.devnull, 'wb'))
    os.remove(rendered_template_file)
    os.remove(rendered_template_file + ".out")
    os.remove(rendered_template_file + ".log")
    os.remove(rendered_template_file + ".aux")

if __name__ == "__main__":
    main()