from typing import List


class Record:
    """
    Класс для представления записей о доходах и расходах.
    """

    def __init__(self, date: str, category: str, amount: float, description: str):
        """
        Создает новую запись.

        Args:
            date (str): Дата записи в формате 'ГГГГ-ММ-ДД'.
            category (str): Категория записи (Доход/Расход).
            amount (float): Сумма записи.
            description (str): Описание записи.
        """
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class Wallet:
    """
    Класс для управления личным финансовым кошельком.
    """

    def __init__(self, filename: str):
        """
        Инициализирует кошелек.

        Args:
            filename (str): Имя файла для хранения записей.
        """
        self.filename = filename
        self.records: List[Record] = []

    def load_records(self):
        """
        Загружает записи из файла в кошелек.
        """
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines), 5):  # каждая запись состоит из 5 строк
                    date = lines[i].strip().split(': ')[1]
                    category = lines[i+1].strip().split(': ')[1]
                    amount = float(lines[i+2].strip().split(': ')[1])
                    description = lines[i+3].strip().split(': ')[1]
                    record = Record(date, category, amount, description)
                    self.records.append(record)
            print("Записи успешно загружены.")
        except FileNotFoundError:
            print("Файл с записями не найден.")
        except Exception as e:
            print("Ошибка при загрузке записей:", e)

    def save_records(self):
        """
        Сохраняет записи из кошелька в файл.
        """
        try:
            with open(self.filename, 'w') as file:
                for record in self.records:
                    file.write(f"Дата: {record.date}\n")
                    file.write(f"Категория: {record.category}\n")
                    file.write(f"Сумма: {record.amount}\n")
                    file.write(f"Описание: {record.description}\n")
                    file.write("\n")
            print("Записи успешно сохранены.")
        except Exception as e:
            print("Ошибка при сохранении записей:", e)

    def add_record(self, record: Record):
        """
        Добавляет новую запись в кошелек.

        Args:
            record (Record): Новая запись для добавления.
        """
        try:
            self.records.append(record)
            print("Запись успешно добавлена.")
        except Exception as e:
            print("Ошибка при добавлении записи:", e)

    def edit_record(self, index: int, new_record: Record):
        """
        Редактирует существующую запись в кошельке.

        Args:
            index (int): Индекс записи для редактирования.
            new_record (Record): Новая версия записи.
        """
        try:
            self.records[index] = new_record
            print("Запись успешно отредактирована.")
        except IndexError:
            print("Неверный индекс записи.")
        except Exception as e:
            print("Ошибка при редактировании записи:", e)

    def search_records(self, category=None, date=None, amount=None):
        """
        Ищет записи в кошельке по заданным критериям.

        Args:
            category (str): Категория записи для поиска (Доход/Расход).
            date (str): Дата записи для поиска в формате 'ГГГГ-ММ-ДД'.
            amount (float): Сумма записи для поиска.

        Returns:
            list: Список найденных записей.
        """
        try:
            results = []
            for record in self.records:
                if (category is None or record.category == category) and \
                   (date is None or record.date == date) and \
                   (amount is None or record.amount == amount):
                    results.append(record)
            return results
        except Exception as e:
            print("Ошибка при поиске записей:", e)
            return []

    def calculate_balance(self):
        """
        Вычисляет текущий баланс кошелька.

        Returns:
            float: Текущий баланс.
        """
        total_income = sum(record.amount for record in self.records if record.category == "Доход")
        total_expense = sum(record.amount for record in self.records if record.category == "Расход")
        balance = total_income - total_expense
        return balance

    def display_balance(self):
        """
        Выводит текущий баланс кошелька на экран.
        """
        balance = self.calculate_balance()
        print(f"Текущий баланс: {balance}")


def main():
    """
    Основная функция программы для взаимодействия с пользователем.
    """
    wallet = Wallet("records.txt")
    wallet.load_records()

    while True:
        print("1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            wallet.display_balance()
        elif choice == "2":
            date = input("Введите дату: ")
            category = input("Введите категорию (Доход/Расход): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            record = Record(date, category, amount, description)
            wallet.add_record(record)
        elif choice == "3":
            index = int(input("Введите индекс записи для редактирования: "))
            if index < len(wallet.records) and index >= 0:
                date = input("Введите новую дату: ")
                category = input("Введите новую категорию (Доход/Расход): ")
                amount = float(input("Введите новую сумму: "))
                description = input("Введите новое описание: ")
                new_record = Record(date, category, amount, description)
                wallet.edit_record(index, new_record)
            else:
                print("Неверный индекс записи.")
        elif choice == "4":
            category = input("Введите категорию для поиска (Доход/Расход): ")
            date = input("Введите дату для поиска (формат: ГГГГ-ММ-ДД): ")
            amount = float(input("Введите сумму для поиска: "))  # Если не нужно, оставьте пустым или введите любое значение
            results = wallet.search_records(category, date, amount)
            if results:
                print("Результаты поиска:")
                for i, record in enumerate(results):
                    print(f"Запись {i + 1}:")
                    print(f"Дата: {record.date}")
                    print(f"Категория: {record.category}")
                    print(f"Сумма: {record.amount}")
                    print(f"Описание: {record.description}")
                    print()
            else:
                print("Записей по указанным критериям не найдено.")
        elif choice == "5":
            wallet.save_records()
            print("Программа завершена.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()