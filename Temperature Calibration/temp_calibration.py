def generate_json():
    json_sample = """
    {
        "bed_size_x" : "235",
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
        start_fan_speed=10,
        file_name="Test.gcode",
    }
"""

def choose_json():
    pass


def main():
    print("Создать новую конфигурацию?[д/н]")
    if str(input()) in ['Д', 'д', 'Y', 'y']:
        generate_json()
    else:
        choose_json()


if __name__ == "__main__":
    main()
