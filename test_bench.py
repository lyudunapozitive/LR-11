
"""
Лабораторна робота № 11. Модуль 2.
Тестовий стенд перевірки поліморфізму, інкапсуляції та dunder-операторів.
Освітній компонент: Програмування на Python.
Варіант 20.
"""

import sys
import time
from hardware_entities import HardwareStack, ShadowStack


def run_oop_testbench() -> None:
    """Виконує функціональне тестування об'єктно-орієнтованої моделі."""
    header_sep = "=" * 90
    sub_sep = "-" * 90

    print(header_sep)
    print(f"{'ТЕСТОВИЙ СТЕНД АПАРАТНОГО ТА ТІНЬОВОГО СТЕКІВ':^90}")
    print(header_sep)

    # 1. Створення об'єктів базового та похідного класів
    stack1 = HardwareStack(
        stack_id="STACK-01",
        capacity=8,
        initial_addresses=[4096, 4100, 4104]
    )

    stack2 = HardwareStack(
        stack_id="STACK-02",
        capacity=6,
        initial_addresses=[8192, 8196]
    )

    shadow_stack = ShadowStack(
        stack_id="SHADOW-01",
        capacity=7,
        initial_addresses=[12288, 12292]
    )

    # 2. Демонстрація рядкового відображення (__str__ та __repr__)
    print(f"{'1. СТРОКОВЕ ВІДОБРАЖЕННЯ ОБ\'ЄКТІВ (__str__ та __repr__)':^90}")
    print(sub_sep)
    print(f"  print(stack1):       {stack1}")
    print(f"  print(stack2):       {stack2}")
    print(f"  print(shadow_stack): {shadow_stack}")
    print(f"  repr(shadow_stack):  {repr(shadow_stack)}")
    print(sub_sep)

    # 3. Перевірка інкапсуляції та властивостей (@property)
    print(f"{'2. ІНКАПСУЛЯЦІЯ ТА ВАЛІДАЦІЯ ВЛАСТИВОСТЕЙ (@property)':^90}")
    print(sub_sep)

    print(f"  Початкова ємність stack1: {stack1.capacity} слотів")
    stack1.capacity = 10
    print(f"  Оновлена ємність stack1: {stack1.capacity} слотів")

    try:
        stack1.capacity = 2
    except ValueError as err:
        print(f"  [ЗАХИСТ СЕТЕРА ПРАЦЮЄ]: {err}")

    print(sub_sep)

    # 4. Протокол послідовностей (__len__ та __getitem__)
    print(f"{'3. ПРОТОКОЛ ПОСЛІДОВНОСТЕЙ (__len__, __getitem__)':^90}")
    print(sub_sep)

    print(f"  Глибина stack1 (len): {len(stack1)}")
    print(f"  Покажчик вершини SP:  {stack1.sp}")
    print(f"  Адреса stack1[0]:     {stack1[0]}")
    print(f"  Адреса stack1[-1]:    {stack1[-1]}")
    print(f"  Адреси стека:         {[stack1[i] for i in range(len(stack1))]}")
    print(sub_sep)

    # 5. Перевантаження оператора додавання (__add__)
    print(f"{'4. ПЕРЕВАНТАЖЕННЯ АРИФМЕТИКИ (__add__)':^90}")
    print(sub_sep)

    combined_stack = stack1 + stack2

    print(f"  Результат stack1 + stack2:")
    print(f"  {combined_stack}")
    print(f"  Сумарна глибина: {len(combined_stack)} адрес")
    print(sub_sep)

    # 6. Перевантаження операторів порівняння (__eq__, __lt__)
    print(f"{'5. ОПЕРАТОРИ ПОРІВНЯННЯ (__eq__, __lt__)':^90}")
    print(sub_sep)

    print(f"  Вільних слотів stack1: {stack1.free_slots}")
    print(f"  Вільних слотів stack2: {stack2.free_slots}")

    print(f"  stack1 == stack2 ? {stack1 == stack2}")
    print(f"  stack1 < stack2 ?  {stack1 < stack2}")
    print(f"  stack2 < stack1 ?  {stack2 < stack1}")
    print(sub_sep)

    # 7. Перевірка похідного класу ShadowStack
    print(f"{'6. УСПАДКУВАННЯ ТА КОНТРОЛЬ ТІНЬОВОГО СТЕКА':^90}")
    print(sub_sep)

    print(f"  Початковий стан: {shadow_stack}")
    print(f"  Контроль цілісності: {shadow_stack.validate_shadow()}")

    shadow_stack.push(12300)
    print(f"  Після додавання адреси: {shadow_stack}")

    removed_address = shadow_stack.pop()
    print(f"  Вилучена адреса: {removed_address}")
    print(f"  Після вилучення: {shadow_stack}")
    print(f"  Контроль цілісності: {shadow_stack.validate_shadow()}")
    print(sub_sep)

    # 8. Поліморфне сортування об'єктів
    stack_cluster = [stack1, stack2, shadow_stack]

    print(f"{'7. ПОЛІМОРФНЕ СОРТУВАННЯ СТЕКІВ (за кількістю вільних слотів)':^90}")
    print(sub_sep)

    sorted_cluster = sorted(stack_cluster)

    for idx, node in enumerate(sorted_cluster, start=1):
        print(f"  Ранг {idx}: {node}")

    print(header_sep + "\n")


def main() -> None:
    """Головна точка входу лабораторної роботи."""
    t_start = time.perf_counter()
    run_oop_testbench()
    t_elapsed = time.perf_counter() - t_start

    print(f"Час виконання об'єктно-орієнтованого тестування: {t_elapsed * 1000:.3f} мс\n")


if __name__ == "__main__":
    main()
