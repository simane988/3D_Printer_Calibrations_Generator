class GCodeProgram:

    def __init__(
            self,
            bed_size_x=235,
            bed_size_y=235,
            z_offset=0.0,
            is_center_zero=False,
            is_autocalibrate=False,
            layer_width=0.4,
            first_layer_width=0.6,
            layer_height=0.2,
            layer_speed=60,
            first_layer_speed=30,
            travel_speed=150,
            linear_advance="",
            preheat_hotend=210,
            preheat_bed=60,
            fan_speed=0,
            file_name="Test.gcode",
    ):
        """
        Конструктор класса, который принимает множество параметров.
        Параметры используются для начальной настройки печати.

        :param float bed_size_x: Размер стола по X в мм (100-1000мм)
        :param float bed_size_y: Размер стола по Y в мм (100-1000мм)
        :param float z_offset: Отступ по Z в мм
        :param bool is_center_zero: Начало координат в центре стола
        :param bool is_autocalibrate: Автокалибровка стола
        :param float layer_width: Ширина линии в мм
        :param float first_layer_width: Ширина линии первого слоя в мм
        :param float layer_height: Толщина слоя в мм
        :param float layer_speed: Скорость печати
        :param float first_layer_speed: Скорость печати первого слоя
        :param float travel_speed: Скорость перемещения
        :param str linear_advance: Коэффициент Linear (Pressure) Advance
        :param int preheat_hotend: Температура прогрева хотенда
        :param int preheat_bed: Температура прогрева стола
        :param float fan_speed: Основная скорость вентилятора
        :param str file_name: Название итогового G-Code файла
        """
        self.file = None

        try:
            if bed_size_x < 100 or bed_size_x > 1000:
                raise ValueError("Размер стола по X (bed_size_x) не может быть меньше 100 мм и больше 1000 мм.")
            self.bed_size_x = float(bed_size_x)
        except TypeError:
            raise TypeError(f"bed_size_x должен быть типа float, а не {type(bed_size_x)}.") from None

        try:
            if bed_size_y < 100 or bed_size_y > 1000:
                raise ValueError("Размер стола по Y (bed_size_y) не может быть меньше 100 мм и больше 1000 мм.")
            self.bed_size_y = float(bed_size_y)
        except TypeError:
            raise TypeError(f"bed_size_y должен быть типа float, а не {type(bed_size_y)}.") from None

        try:
            if abs(z_offset) > layer_height:
                raise ValueError("Модуль z_offset не может быть больше высоты слоя (layer_height)")
            self.z_offset = float(z_offset)
        except TypeError:
            raise TypeError(f"z_offset должен быть типа float, а не {type(z_offset)}.") from None

        if isinstance(is_center_zero, bool):
            self.is_center_zero = bool(is_center_zero)
        else:
            raise TypeError(f"is_center_zero должен быть типа bool, а не {type(is_center_zero)}.") from None

        if isinstance(is_autocalibrate, bool):
            self.is_autocalibrate = bool(is_autocalibrate)
        else:
            raise TypeError(f"is_autocalibrate должен быть типа bool, а не {type(is_autocalibrate)}.") from None

        try:
            if layer_width < 0.1 or layer_width > 2:
                raise ValueError("Ширина линии (layer_width) не может быть меньше 0.1 мм и больше 2 мм.")
            self.layer_width = float(layer_width)
        except TypeError:
            raise TypeError(f"layer_width должен быть типа float, а не {type(layer_width)}.") from None

        try:
            if first_layer_width < 0.1 or first_layer_width > 2:
                raise ValueError("Ширина линии первого слоя (first_layer_width) не может быть меньше 0.1 мм и больше 2 мм.")
            self.first_layer_width = float(first_layer_width)
        except TypeError:
            raise TypeError(f"first_layer_width должен быть типа float, а не {type(first_layer_width)}.") from None

        try:
            if layer_height < 0.05 or layer_height > self.layer_width*0.75:
                raise ValueError("Высота слоя (layer_height) не может быть меньше 0.05 мм и больше 75% от ширины линии (layer_width).")
            self.layer_height = float(layer_height)
        except TypeError:
            raise TypeError(f"layer_height должен быть типа float, а не {type(layer_height)}.") from None

        try:
            if layer_speed < 10 or layer_speed > 1000:
                raise ValueError("Скорость печати (layer_speed) не может быть меньше 10 мм/с и больше 1000 мм/с.")
            self.layer_speed = float(layer_speed)
        except TypeError:
            raise TypeError(f"layer_speed должен быть типа float, а не {type(layer_speed)}.") from None

        try:
            if first_layer_speed < 10 or first_layer_speed > 1000:
                raise ValueError("Скорость печати первого слоя (first_layer_speed) не может быть меньше 10 мм/с и больше 1000 мм/с.")
            self.first_layer_speed = float(first_layer_speed)
        except TypeError:
            raise TypeError(f"first_layer_speed должен быть типа float, а не {type(first_layer_speed)}.") from None

        try:
            if travel_speed < 10 or travel_speed > 1000:
                raise ValueError("Скорость перемещений (travel_speed) не может быть меньше 10 мм/с и больше 1000 мм/с.")
            self.travel_speed = float(travel_speed)
        except TypeError:
            raise TypeError(f"travel_speed должен быть типа float, а не {type(travel_speed)}.") from None

        try:
            self.linear_advance = str(linear_advance)
        except TypeError:
            raise TypeError(f"linear_advance должен быть типа str, а не {type(linear_advance)}.") from None

        try:
            if preheat_hotend < 150 or preheat_hotend > 350:
                raise ValueError("Температура хотенда (preheat_hotend) не может быть меньше 150°C и больше 350°C.")
            self.preheat_hotend = int(preheat_hotend)
        except TypeError:
            raise TypeError(f"preheat_hotend должен быть типа int, а не {type(preheat_hotend)}.") from None

        try:
            if preheat_bed < 0 or preheat_bed > 150:
                raise ValueError("Температура стола (preheat_bed) не может быть меньше 0°C и больше 150°C.")
            self.preheat_bed = int(preheat_bed)
        except TypeError:
            raise TypeError(f"preheat_bed должен быть типа int, а не {type(preheat_bed)}.") from None

        try:
            if fan_speed < 0 or fan_speed > 100:
                raise ValueError("Начальная скорость вентилятора (fan_speed) не может быть меньше 0% и больше 100%.")
            self.fan_speed = float(fan_speed)
        except TypeError:
            raise TypeError(f"fan_speed должен быть типа float, а не {type(fan_speed)}.") from None

        try:
            self.file_name = str(file_name)
        except TypeError:
            raise TypeError(f"file_name должен быть типа str, а не {type(file_name)}.") from None

    def before_start(self):
        """
        Создаёт файл и генерирует G-Code, который будет выполняться перед основной частью.
        Тут происходит прогрев элементов, настройка начальных параметров.
        """
        self.file = open(f"{self.file_name}", "w", encoding="utf-8")
        self.file.write(f"; generated by simane988 calibrations generator\n"
                        f"; Written by Korobeynikov Semen http://github.com/simane988\n"
                        f"{self.linear_advance}\n"
                        f"M190 S{self.preheat_bed}\n"
                        f"M109 S{self.preheat_hotend}\n"
                        f"G28\n"
                        f"G92 E0\n"
                        f"G90\n"
                        f"M82\n"
                        f"M106 S{int(255/100*self.fan_speed)}\n"
                        f"; start of gcode\n")

    def after_end(self):
        """
        Выключает нагрев всех элементов, паркует голову и снимает "защиту парковки".
        Также закрывает файл с G-Code-ом.
        """
        self.file.write(f"; end of gcode\n"
                        f"M104 S0\n"
                        f"M140 S0\n"
                        f"M106 S0\n"
                        f"G28\n"
                        f"M84\n")
        self.file.close()

    def set_temp(self,
                 hotend_temp=None,
                 bed_temp=None,
                 is_hotend_wait=False,
                 is_bed_wait=True
                 ):
        """
        Устанавливает новые значения температуры экструдера и стола.

        :param float hotend_temp: Новая температура экструдера
        :param float bed_temp: Новая температура стола
        :param bool is_hotend_wait: Нужно ли ждать нагрева экструдера
        :param bool is_bed_wait: Нужно ли ждать нагрева стола
        """
        if bed_temp:
            if 0 <= bed_temp <= 150:
                if is_bed_wait:
                    self.file.write(f"M190 S{bed_temp}\n")
                else:
                    self.file.write(f"M140 S{bed_temp}\n")
            else:
                raise ValueError("Температура стола (bed_temp) не может быть меньше 0°C и больше 150°C.")

        if hotend_temp:
            if 150 <= hotend_temp <= 350:
                if is_hotend_wait:
                    self.file.write(f"M109 S{hotend_temp}\n")
                else:
                    self.file.write(f"M104 S{hotend_temp}\n")
            else:
                raise ValueError("Температура хотенда (hotend_temp) не может быть меньше 150°C и больше 350°C.")

    def set_fan_speed(self, fan_speed):
        """
        Устанавливает новое значение скорости вентилятора.
        :param float fan_speed: Новая скорость вентилятора
        """
        try:
            if fan_speed < 0 or fan_speed > 100:
                raise ValueError(
                    "Начальная скорость вентилятора (fan_speed) не может быть меньше 0% и больше 100%.")
            self.file.write(f"M106 S{fan_speed}")
        except TypeError:
            raise TypeError(f"fan_speed должен быть типа float, а не {type(fan_speed)}.") from None

    # noinspection PyPep8Naming
    def linear_move(self,
                    X: float = None,
                    Y: float = None,
                    Z: float = None,
                    E: float = None,
                    F: float = None):
        """

        :param X: Перемещение по X
        :param Y: Перемещение по Y
        :param Z: Перемещение по Z
        :param E: Кол-во выдавленного филамента
        :param F: Скорость экструзии
        """
        command = "G1"
        if X is not None:
            command += f" X{X}"
        if Y is not None:
            command += f" Y{Y}"
        if Z is not None:
            command += f" Z{Z}"
        if E is not None:
            command += f" E{E}"
        if F is not None:
            command += f" F{F}"
        command += "\n"
        self.file.write(command)


if __name__ == "__main__":
    gcodep = GCodeProgram(
        bed_size_x=235,
        bed_size_y=235,
        z_offset=0.0,
        is_center_zero=False,
        is_autocalibrate=False,
        layer_width=0.4,
        first_layer_width=0.6,
        layer_height=0.2,
        layer_speed=60,
        first_layer_speed=30,
        travel_speed=150,
        linear_advance="",
        preheat_hotend=210,
        preheat_bed=60,
        fan_speed=10,
        file_name="Test.gcode",
    )
    gcodep.before_start()
    gcodep.linear_move(X=10, Y=20, E=10)
    gcodep.after_end()
