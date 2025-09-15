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


if __name__ == "__main__":
    # Тестування FastFoodQueue
    fast_food = FastFoodQueue()
    fast_food.add("Олег")
    fast_food.add("Анна")
    fast_food.add("Марія")
    fast_food.add("Сергій")

    # Обслуговуємо з кас 0 та 1 (клієнти переходять у чергу на отримання)
    fast_food.serve(0)
    fast_food.serve(1)

    # Емулюємо час приготування та отримання замовлень
    time.sleep(2)
    client1, duration1 = fast_food.make_order()
    print(f"Видано замовлення клієнту: {client1}, час очікування: {duration1:.2f} с")

    time.sleep(3)
    client2, duration2 = fast_food.make_order()
    print(f"Видано замовлення клієнту: {client2}, час очікування: {duration2:.2f} с")

    # Показуємо статистику
    fast_food.show_statistics()
