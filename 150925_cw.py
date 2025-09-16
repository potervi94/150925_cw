# -*- coding: utf-8 -*-
#  Завдання 1
#     Використовуючи чергу створіть клас FastFoodQueue для 
#     організації роботи черг у фасфуді. Є 4 каси, новий клієнт стає 
#     в ту, де найменше людей. Коли клієнт зробив замовлення, 
#     його добавляють в чергу на отримання. Має зберігатися час, 
#     коли людина зробила замовлення, та коли отримала 
#     замовлення. Інформація про час обслуговування має 
#     зберігатись у окремому списку 
#     Атрибути: 
#      queues – список з 4-ма чергами до кас 
#      order_queue – черга клієнтів на отримання замовлення 
#      service_duration_history – список з часом обслуговування 
#     клієнтів 
#     Методи: 
#      add(client) – додає клієнта в найкоротшу чергу 
#      serve(idx) – обслуговуємо клієнта з черги за індексом. 
#     Треба додати клієнта в order_queue разом з часом коли 
#     зроблено замовлення 
#      make_order() – видає готове замовлення клієнту та 
#     обраховує скільки часу очікував клієнт. Це число треба 
#     добавити в service_duration_history 
#      show_statistics() – виводить мінімальний, максимальний 
#     та середній час обслуговування клієнтів 
import time
import statistics
from collections import deque


class FastFoodQueue:
    """
    Черги у фастфуді:
      - 4 черги до кас (queues)
      - order_queue: черга на отримання замовлення (кортежі: (client, order_time))
      - service_duration_history: список тривалостей очікування між замовленням та видачею
    """

    def __init__(self):
        # 4 черги до кас
        self.queues = [deque() for _ in range(4)]
        # Черга на отримання замовлення: (клієнт, час_замовлення)
        self.order_queue = deque()
        # Історія тривалостей обслуговування (в секундах)
        self.service_duration_history = []

    def add(self, client):
        """
        Додає клієнта у найкоротшу з 4-х черг.
        """
        shortest_idx = min(range(4), key=lambda i: len(self.queues[i]))
        self.queues[shortest_idx].append(client)

    def serve(self, idx: int):
        """
        Обслуговує клієнта з черги за індексом (0..3):
        клієнта переносять до order_queue разом із часом оформлення замовлення.
        Повертає ім'я/ідентифікатор клієнта або None, якщо черга порожня.
        """
        if not (0 <= idx < 4):
            raise IndexError("Невірний індекс черги. Має бути в діапазоні 0..3.")
        if not self.queues[idx]:
            return None
        client = self.queues[idx].popleft()
        order_time = time.time()
        self.order_queue.append((client, order_time))
        return client

    def make_order(self):
        """
        Видає готове замовлення першому в order_queue і рахує тривалість очікування.
        Додає тривалість до service_duration_history.
        Повертає (client, duration) або (None, None), якщо order_queue порожня.
        """
        if not self.order_queue:
            return None, None
        client, order_time = self.order_queue.popleft()
        receive_time = time.time()
        duration = receive_time - order_time
        self.service_duration_history.append(duration)
        return client, duration

    def show_statistics(self):
        """
        Виводить мінімальний, максимальний та середній час обслуговування.
        Якщо статистики ще немає — друкує відповідне повідомлення.
        """
        if not self.service_duration_history:
            print("Статистика відсутня (ще не було виданих замовлень).")
            return
        mn = min(self.service_duration_history)
        mx = max(self.service_duration_history)
        avg = statistics.mean(self.service_duration_history)
        print(f"Мінімальний час: {mn:.2f} с")
        print(f"Максимальний час: {mx:.2f} с")
        print(f"Середній час: {avg:.2f} с")


# Завдання 2
#     Використовуючи черги з пріоритетом створіть програму
#     для симуляції роботи аеропорту. Кожен пасажир має пройти
#     через 3 етапи: реєстрація, контроль безпеки, посадка.
#     Відповідно аеропорт складається з 3-ох зон, кожна з яких має
#     свою чергу. Коли Пасажир пройшов одну зону, то переходить
#     в наступну.
#     Пасажири з вищим пріоритетом обслуговуються першими
#     Клас Zone – зона
#     Атрибути:
#      name – назва(реєстрація, контроль безпеки або посадка)
#      passengers – черга пасажирів
#     Методи:
#      add(passenger) – додає пацієнта в чергу з пріоритетом
#      serve_passenger() – обслуговуємо наступного пасажира
#     та повертає його
#     Клас Airport – аеропорт
#     Атрибути:
#      zones – словник із зонами, ключем є назва зони
#      passengers – список пасажирів, які успішно пройшли 3
#     зони
#     Методи:
#      add(passenger) – додає пасажира в чергу на реєстрацію
#      serve_registration() – обслуговує клієнта з черги
#     реєстрації та переводить на котроль безпеки
#      serve_security_control() – обслуговує клієнта з черги
#     контролю безпеки та переводить на посадку
#      serve_boarding() – обслуговує клієнта з черги посадки та
#     переводить в passengers
#      show_statistics() – вивести кількість пасажирів у кожній
#     зоні та скільки успішно все пройшли
#     Для цього скористайтесь класом Passenger
#     Атрибути:
#      name – ім’я
#      priority – пріоритет
# TASK 2
import heapq
from itertools import count

class Passenger:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority


class Zone:
    def __init__(self, name: str):
        self.name = name
        # Пріоритетна черга: (-priority, order, passenger)
        self._heap = []
        self._order = count()

    def add(self, passenger: "Passenger"):
        # Вищий пріоритет -> обслуговується раніше (через -priority)
        heapq.heappush(self._heap, (-passenger.priority, next(self._order), passenger))

    def serve_passenger(self):
        if not self._heap:
            return None
        _, _, passenger = heapq.heappop(self._heap)
        return passenger

    def __len__(self):
        return len(self._heap)


class Airport:
    def __init__(self):
        # Створюємо зони
        self.zones = {
            "registration": Zone("реєстрація"),
            "security": Zone("контроль безпеки"),
            "boarding": Zone("посадка"),
        }
        # Пасажири, які пройшли всі 3 зони
        self.passengers = []

    def add(self, passenger: "Passenger"):
        # Додаємо в чергу на реєстрацію
        self.zones["registration"].add(passenger)

    def serve_registration(self):
        p = self.zones["registration"].serve_passenger()
        if p is not None:
            self.zones["security"].add(p)
        return p

    def serve_security_control(self):
        p = self.zones["security"].serve_passenger()
        if p is not None:
            self.zones["boarding"].add(p)
        return p

    def serve_boarding(self):
        p = self.zones["boarding"].serve_passenger()
        if p is not None:
            self.passengers.append(p)
        return p

    def show_statistics(self):
        print("Статистика по аеропорту:")
        for key in ("registration", "security", "boarding"):
            zone = self.zones[key]
            print(f"- У зоні '{zone.name}': {len(zone)} пасажир(ів)")
        print(f"- Успішно пройшли всі етапи: {len(self.passengers)}")

# Завдання 3
# Створіть дочірні класи від Zone та перевизначте метод
# serve_passenger() щоб він повертав пару: пасажир та True/False
# в залежності від успішності перевірки.
# Перевірки:
#  реєстрація – наявність білету(у багажі)
#  безпека – відсутність небезпечних предметів у багажі:
# ніж, зброя, вибухівка
#  посадка – перевірка не потрібна
# Для цього скористайтесь класом Passenger
# Атрибути:
#  name – ім’я
#  priority – пріоритет
#  baggage – список з предметами в багажі
class Passenger(Passenger):
    def __init__(self, name, priority, baggage=None):
        self.name = name
        self.priority = priority
        self.baggage = baggage if baggage is not None else []

class RegistrationZone(Zone):
    def __init__(self):
        super().__init__("реєстрація")

    def serve_passenger(self):
        if not self._heap:
            return None, False
        _, _, passenger = heapq.heappop(self._heap)
        ok = "ticket" in (item.lower() for item in passenger.baggage)
        return passenger, ok

class SecurityZone(Zone):
    DANGEROUS = {"ніж", "зброя", "вибухівка"}

    def __init__(self):
        super().__init__("контроль безпеки")

    def serve_passenger(self):
        if not self._heap:
            return None, False
        _, _, passenger = heapq.heappop(self._heap)
        baggage_lower = {item.lower() for item in passenger.baggage}
        ok = self.DANGEROUS.isdisjoint(baggage_lower)
        return passenger, ok

class BoardingZone(Zone):
    def __init__(self):
        super().__init__("посадка")

    def serve_passenger(self):
        if not self._heap:
            return None, False
        _, _, passenger = heapq.heappop(self._heap)
        # На посадці додаткової перевірки немає
        return passenger, True

class AirportTask3:
    def __init__(self):
        self.zones = {
            "registration": RegistrationZone(),
            "security": SecurityZone(),
            "boarding": BoardingZone(),
        }
        self.passengers = []          # ті, хто сів на борт
        self.failed = {"registration": [], "security": []}  # хто не пройшов перевірки

    def add(self, passenger: "Passenger"):
        self.zones["registration"].add(passenger)

    def serve_registration(self):
        passenger, ok = self.zones["registration"].serve_passenger()
        if passenger is not None and ok:
            self.zones["security"].add(passenger)
        elif passenger is not None and not ok:
            self.failed["registration"].append(passenger)
        return passenger, ok

    def serve_security_control(self):
        passenger, ok = self.zones["security"].serve_passenger()
        if passenger is not None and ok:
            self.zones["boarding"].add(passenger)
        elif passenger is not None and not ok:
            self.failed["security"].append(passenger)
        return passenger, ok

    def serve_boarding(self):
        passenger, ok = self.zones["boarding"].serve_passenger()
        if passenger is not None and ok:
            self.passengers.append(passenger)
        return passenger, ok

    def show_statistics(self):
        print("Статистика (Завдання 3):")
        for key in ("registration", "security", "boarding"):
            zone = self.zones[key]
            print(f"- У зоні '{zone.name}': {len(zone)} пасажир(ів)")
        print(f"- Посаджено на борт: {len(self.passengers)}")
        print(f"- Не пройшли реєстрацію: {len(self.failed['registration'])}")
        print(f"- Не пройшли безпеку: {len(self.failed['security'])}")


if __name__ == "__main__":
    # # TASK 1
    # # Тестування FastFoodQueue
    # fast_food = FastFoodQueue()
    # fast_food.add("Олег")
    # fast_food.add("Анна")
    # fast_food.add("Марія")
    # fast_food.add("Сергій")
    #
    # # Обслуговуємо з кас 0 та 1 (клієнти переходять у чергу на отримання)
    # fast_food.serve(0)
    # fast_food.serve(1)
    #
    # # Емулюємо час приготування та отримання замовлень
    # time.sleep(2)
    # client1, duration1 = fast_food.make_order()
    # print(f"Видано замовлення клієнту: {client1}, час очікування: {duration1:.2f} с")
    #
    # time.sleep(3)
    # client2, duration2 = fast_food.make_order()
    # print(f"Видано замовлення клієнту: {client2}, час очікування: {duration2:.2f} с")
    #
    # # Показуємо статистику
    # fast_food.show_statistics()
    # # TASK 2
    # # Тестування
    # airport = Airport()
    # passengers = [
    #     Passenger("Олег", 3),
    #     Passenger("Анна", 1),
    #     Passenger("Марія", 4),
    #     Passenger("Сергій", 2)
    # ]
    #
    # for p in passengers:
    #     airport.add(p)
    #
    # airport.serve_registration()
    # airport.serve_registration()
    # airport.serve_security_control()
    # airport.serve_boarding()
    #
    # airport.show_statistics()
    # TASK3
      # Використання
    passenger1 = Passenger("Alice", 2, ["ticket", "phone"])
    passenger2 = Passenger("Bob", 1, ["ticket", "ніж"])
    passenger3 = Passenger("Charlie", 3, ["ticket"])
    passenger4 = Passenger("David", 4, ["ticket", "laptop"])
    passenger5 = Passenger("Eva", 2, ["bottle", "ніж"])
    passenger6 = Passenger("Frank", 3, ["book"])
    passenger7 = Passenger("Grace", 1, ["ticket", "вибухівка"])
    passenger8 = Passenger("Hannah", 5, ["phone", "tablet"])
    passenger9 = Passenger("Ivy", 2, ["ticket", "earphones"])
    passenger10 = Passenger("Jack", 1, ["ticket", "зброя"])

    # Створюємо аеропорт
    airport = Airport()

    # Додаємо пасажирів до реєстрації
    airport.add(passenger1)
    airport.add(passenger2)
    airport.add(passenger3)
    airport.add(passenger4)
    airport.add(passenger5)
    airport.add(passenger6)
    airport.add(passenger7)
    airport.add(passenger8)
    airport.add(passenger9)
    airport.add(passenger10)

    # Проходимо етапи для кожного пасажира
    for _ in range(10):
        airport.serve_registration()
        airport.serve_security_control()
        airport.serve_boarding()

    # Показуємо статистику
    airport.show_statistics()
