import threading
import random
import time

class Bank:
    def __init__(self):
        self.balance = 0  # Баланс банка
        self.lock = threading.Lock()  # Объект блокировки

    def deposit(self):
        for _ in range(100):
            amount = random.randint(50, 500)  # Случайная сумма пополнения
            with self.lock:  # Блокируем доступ к балансу
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")

                # Если баланс >= 500 и замок не заблокирован, разблокируем его
                if self.balance >= 500 and self.lock.locked():
                    self.lock.release()

            time.sleep(0.001)  # Имитация скорости выполнения пополнения

    def take(self):
        for _ in range(100):
            amount = random.randint(50, 500)  # Случайная сумма снятия
            print(f"Запрос на {amount}")

            # Блокируем доступ к балансу
            with self.lock:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    self.lock.acquire()  # Блокируем поток

            time.sleep(0.001)  # Имитация скорости выполнения снятия

# Создание объекта класса Bank
bk = Bank()

# Создание потоков для методов deposit и take
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запуск потоков
th1.start()
th2.start()

# Ожидание завершения потоков
th1.join()
th2.join()

# Вывод итогового баланса
print(f'Итоговый баланс: {bk.balance}')
