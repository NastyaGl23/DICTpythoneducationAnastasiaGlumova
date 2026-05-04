import math
import argparse
import sys


class CreditProcessor:
    def __init__(self, cli_args):
        self.mode = cli_args.type
        self.credit_principal = cli_args.principal
        self.monthly_pay = cli_args.payment
        self.total_periods = cli_args.periods
        self.yearly_interest = cli_args.interest

        # Валидация наличия и корректности процентной ставки
        if self.yearly_interest is None or self.yearly_interest <= 0:
            print("Ошибка: параметры указаны неверно.")
            sys.exit()

        # Месячная процентная ставка в долях
        self.ratio_interest = self.yearly_interest / (12 * 100)

    def _print_overpayment(self, total_paid, initial_loan):
        """Вычисляет и выводит итоговую переплату."""
        print(f"Переплата по кредиту: {int(total_paid - initial_loan)}")

    def run_annuity_calculation(self):
        """Расчет суммы ежемесячного платежа."""
        power_val = (1 + self.ratio_interest) ** self.total_periods
        calculated_payment = self.credit_principal * (self.ratio_interest * power_val) / (power_val - 1)
        calculated_payment = math.ceil(calculated_payment)
        print(f"Ваш ежемесячный аннуитетный платеж составит {calculated_payment}.")
        self._print_overpayment(calculated_payment * self.total_periods, self.credit_principal)

    def run_principal_calculation(self):
        """Расчет максимально возможной суммы займа."""
        power_val = (1 + self.ratio_interest) ** self.total_periods
        base_loan = self.monthly_pay / ((self.ratio_interest * power_val) / (power_val - 1))
        base_loan = math.floor(base_loan)
        print(f"Основная сумма займа: {base_loan}.")
        self._print_overpayment(self.monthly_pay * self.total_periods, base_loan)

    def run_duration_calculation(self):
        """Расчет времени, необходимого для погашения долга."""
        arg_value = self.monthly_pay / (self.monthly_pay - self.ratio_interest * self.credit_principal)
        months_needed = math.ceil(math.log(arg_value, 1 + self.ratio_interest))

        yr_count, mon_count = divmod(months_needed, 12)
        time_segments = []
        if yr_count > 0:
            time_segments.append(f"{yr_count} {'год' if yr_count == 1 else 'года' if 2 <= yr_count <= 4 else 'лет'}")
        if mon_count > 0:
            time_segments.append(f"{mon_count} {'месяц' if mon_count == 1 else 'месяца' if 2 <= mon_count <= 4 else 'месяцев'}")

        print(f"Срок выплаты составит {' и '.join(time_segments)}.")
        self._print_overpayment(self.monthly_pay * months_needed, self.credit_principal)

    def run_diff_calculation(self):
        """Расчет дифференцированных платежей по месяцам."""
        accumulated_sum = 0
        for current_m in range(1, self.total_periods + 1):
            already_paid = self.credit_principal * (current_m - 1) / self.total_periods
            monthly_installment = (self.credit_principal / self.total_periods) + self.ratio_interest * (self.credit_principal - already_paid)
            monthly_installment = math.ceil(monthly_installment)
            accumulated_sum += monthly_installment
            print(f"Месяц {current_m}: платеж — {monthly_installment}")

        self._print_overpayment(accumulated_sum, self.credit_principal)

    def validate_params(self):
        """Проверка логической связности и корректности входных данных."""
        all_metrics = [self.credit_principal, self.monthly_pay, self.total_periods, self.yearly_interest]
        # Значения не могут быть отрицательными
        if any(m is not None and m < 0 for m in all_metrics):
            return False

        # Дифференцированные платежи несовместимы с фиксированным ежемесячным взносом
        if self.mode == "diff" and self.monthly_pay is not None:
            return False

        # Должно быть заполнено минимум 2 числовых параметра (помимо ставки и типа)
        required_fields = [self.credit_principal, self.monthly_pay, self.total_periods]
        if sum(1 for f in required_fields if f is not None) < 2:
            return False

        return True

    def execute(self):
        """Запуск соответствующего алгоритма расчета."""
        if not self.validate_params():
            print("Ошибка: параметры указаны неверно.")
            return

        if self.mode == "annuity":
            if self.monthly_pay is None:
                self.run_annuity_calculation()
            elif self.credit_principal is None:
                self.run_principal_calculation()
            elif self.total_periods is None:
                self.run_duration_calculation()
        elif self.mode == "diff":
            self.run_diff_calculation()
        else:
            print("Ошибка: тип расчета не определен.")


if __name__ == "__main__":
    cmd_parser = argparse.ArgumentParser(description="Финансовый калькулятор")

    cmd_parser.add_argument("--type", choices=["annuity", "diff"], help="Тип платежа")
    cmd_parser.add_argument("--principal", type=float, help="Тело кредита")
    cmd_parser.add_argument("--payment", type=float, help="Ежемесячный взнос")
    cmd_parser.add_argument("--periods", type=int, help="Срок в месяцах")
    cmd_parser.add_argument("--interest", type=float, help="Процентная ставка (годовая)")

    args_provided = cmd_parser.parse_args()
    engine = CreditProcessor(args_provided)
    engine.execute()