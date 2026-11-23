
"""
Лабораторна робота № 11. Модуль 1.
Об'єктно-орієнтована модель апаратного стека викликів.
Інкапсуляція (@property), наслідування та перевантаження dunder-методів.
Освітній компонент: Програмування на Python.
Варіант 20.
"""

from typing import List


class HardwareStack:
    """
    Базовий клас апаратного стека адрес повернення.
    """

    def __init__(self, stack_id: str, capacity: int,
                 initial_addresses: List[int] = None):

        self.__stack_id: str = str(stack_id)
        self.__capacity: int = 0
        self.__stack_buffer: List[int] = []

        # Ініціалізація через сетер для перевірки допустимої ємності
        self.capacity = capacity

        if initial_addresses:
            for address in initial_addresses:
                self.push(address)

    @property
    def stack_id(self) -> str:
        """Повертає ідентифікатор апаратного стека."""
        return self.__stack_id

    @property
    def capacity(self) -> int:
        """Повертає максимальну кількість слотів стека."""
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        """Перевіряє допустиму ємність стека."""
        if type(value) is not int:
            raise TypeError("Ємність стека повинна бути цілим числом.")

        if value <= 0:
            raise ValueError("Ємність стека повинна бути додатною.")

        if value < len(self.__stack_buffer):
            raise ValueError("Нова ємність менша за поточну глибину стека.")

        self.__capacity = value

    @property
    def depth(self) -> int:
        """Повертає поточну глибину стека."""
        return len(self.__stack_buffer)

    @property
    def sp(self) -> int:
        """Повертає індекс вершини стека (Stack Pointer)."""
        return len(self.__stack_buffer) - 1

    @property
    def free_slots(self) -> int:
        """Обчислює кількість вільних слотів стека."""
        return self.__capacity - len(self.__stack_buffer)

    def push(self, address: int) -> None:
        """Додає адресу повернення на вершину стека."""
        if type(address) is not int:
            raise TypeError("Адреса повернення повинна бути цілим числом.")

        if self.depth >= self.capacity:
            raise OverflowError("Переповнення апаратного стека.")

        self.__stack_buffer.append(address)

    def pop(self) -> int:
        """Вилучає адресу з вершини стека."""
        if not self.__stack_buffer:
            raise IndexError("Стек порожній.")

        return self.__stack_buffer.pop()

    # --- Перевантаження протоколу послідовностей ---

    def __len__(self) -> int:
        """Повертає поточну глибину стека."""
        return len(self.__stack_buffer)

    def __getitem__(self, index: int) -> int:
        """Забезпечує індексацію адрес стека."""
        return self.__stack_buffer[index]

    # --- Перевантаження методів представлення ---

    def __repr__(self) -> str:
        """Офіційне представлення об'єкта."""
        return (
            f"HardwareStack(stack_id='{self.__stack_id}', "
            f"capacity={self.__capacity}, "
            f"initial_addresses={self.__stack_buffer!r})"
        )

    def __str__(self) -> str:
        """Форматоване представлення апаратного стека."""
        return (
            f"STACK [{self.__stack_id}] | "
            f"Глибина: {self.depth} | SP: {self.sp} | "
            f"Вільних слотів: {self.free_slots}"
        )

    # --- Перевантаження операторів порівняння ---

    def __eq__(self, other: object) -> bool:
        """Порівняння стеків за ідентифікатором та ємністю."""
        if not isinstance(other, HardwareStack):
            return NotImplemented

        return (
            self.stack_id == other.stack_id
            and self.capacity == other.capacity
        )

    def __lt__(self, other: "HardwareStack") -> bool:
        """Порівняння за кількістю вільних слотів."""
        if not isinstance(other, HardwareStack):
            return NotImplemented

        return self.free_slots < other.free_slots

    # --- Перевантаження оператора додавання (+) ---

    def __add__(self, other: "HardwareStack") -> "HardwareStack":
        """
        Об'єднує два адресні стеки у новий стек,
        збільшуючи його сумарну глибину.
        """
        if not isinstance(other, HardwareStack):
            return NotImplemented

        combined_id = f"{self.stack_id}+{other.stack_id}"
        combined_capacity = self.capacity + other.capacity

        combined_addresses = (
            [self[i] for i in range(len(self))]
            + [other[i] for i in range(len(other))]
        )

        return HardwareStack(
            stack_id=combined_id,
            capacity=combined_capacity,
            initial_addresses=combined_addresses
        )


class ShadowStack(HardwareStack):
    """Похідний клас тіньового стека для контролю адрес викликів."""

   
    def __init__(self, stack_id: str, capacity: int,
                 initial_addresses: List[int] = None):

        # Ініціалізація контрольного буфера перед викликом super()
        self.__shadow_buffer: List[int] = []

        # Делегування ініціалізації базовому класу
        super().__init__(stack_id, capacity, initial_addresses)

    def push(self, address: int) -> None:
        """Додає адресу до основного і тіньового стеків."""
        super().push(address)
        self.__shadow_buffer.append(address)

    def pop(self) -> int:
        """Перевіряє контрольну копію та вилучає адресу."""
        if not self.validate_shadow():
            raise ValueError("Порушення цілісності тіньового стека.")

        address = super().pop()
        self.__shadow_buffer.pop()
        return address

    def validate_shadow(self) -> bool:
        """Перевіряє відповідність основного та тіньового стеків."""
        main_addresses = [self[i] for i in range(len(self))]
        return main_addresses == self.__shadow_buffer

    @property
    def shadow_depth(self) -> int:
        """Повертає глибину контрольного тіньового стека."""
        return len(self.__shadow_buffer)

    def __repr__(self) -> str:
        """Перевизначений технічний вигляд тіньового стека."""
        return (
            f"ShadowStack(stack_id='{self.stack_id}', "
            f"capacity={self.capacity}, "
            f"shadow_depth={self.shadow_depth})"
        )

    def __str__(self) -> str:
        """Перевизначене представлення з контрольними параметрами."""
        base_info = super().__str__()
        return (
            f"{base_info} | "
            f"Shadow: {self.shadow_depth} | "
            f"Контроль: {'OK' if self.validate_shadow() else 'ERROR'}"
        )
