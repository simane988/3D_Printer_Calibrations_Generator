import json
import os
import sys

sys.path.append('..')

from gcode_program import GCodeProgram


def generate_json():
    data = """{
        "bed_size_x" : 235,
        "bed_size_y" :  235,
        "z_offset" :  0.0,
        "is_center_zero" :  "False",
        "is_autocalibrate" :  "False",
        "layer_width" : 0.4,
        "first_layer_width" :  0.6,
        "layer_height" :  0.2,
        "layer_speed" :  60,
        "first_layer_speed" :  30,
        "travel_speed" :  150,
        "linear_advance" : "",
        "preheat_bed" :  60,
        "fan_speed" :  100,
        "file_name" : "Test.gcode",

        "start_hotend_temp" : 230,
        "end_hotend_temp" : 200,
        "num_of_segments" : 7,
        "segment_height" : 5
    }
    """
    nf = open("new_config.json", "w")
    nf.write(data)
    nf.close()


def choose_json():
    pass


def generate_gcode(conf, out_path):
    square_commands = [
        {"X": 12.5, "Y": 12.5, "F": 1800},
        {"X": -12.5, "F": 1800},
        {"Y": -12.5, "F": 1800},
        {"X": 12.5, "F": 1800},
        {"Y": 12.5, "F": 1800}
    ]

    gcp = GCodeProgram(
        bed_size_x=conf["bed_size_x"],
        bed_size_y=conf["bed_size_y"],
        z_offset=conf["z_offset"],
        is_center_zero=bool(conf["is_center_zero"]),
        is_autocalibrate=bool(conf["is_autocalibrate"]),
        layer_width=conf["layer_width"],
        first_layer_width=conf["first_layer_width"],
        layer_height=conf["layer_height"],
        layer_speed=conf["layer_speed"],
        first_layer_speed=conf["first_layer_speed"],
        travel_speed=conf["travel_speed"],
        linear_advance=conf["linear_advance"],
        preheat_hotend=conf["start_hotend_temp"],
        preheat_bed=conf["preheat_bed"],
        fan_speed=conf["fan_speed"],
        file_name=out_path
    )
    gcp.before_start()

    if gcp.is_center_zero:
        offset_x = 0
        offset_y = 0
    else:
        offset_x = gcp.bed_size_x / 2
        offset_y = gcp.bed_size_y / 2

    layers_in_segment = int(conf["segment_height"] / gcp.layer_height)

    cur_temp = gcp.preheat_hotend
    delta_temp = (conf["end_hotend_temp"] - conf["start_hotend_temp"])/(conf["num_of_segments"] - 1)

    cur_z_pos = 0
    for segment in range(conf["num_of_segments"]):
        for layer in range(layers_in_segment):
            gcp.linear_move(Z=cur_z_pos)
            for i in square_commands:
                if i.get("X") and i.get("Y"):
                    gcp.linear_move(X=i["X"], Y=i["Y"], F=i["F"])
                elif i.get("X"):
                    gcp.linear_move(X=i["X"], F=i["F"])
                elif i.get("Y"):
                    gcp.linear_move(Y=i["Y"], F=i["F"])
            cur_z_pos += gcp.layer_height
            cur_z_pos = round(cur_z_pos, 3)
        for i in square_commands:
            if i.get("X") and i.get("Y"):
                gcp.linear_move(X=i["X"]+gcp.layer_width*0.5*i["X"]/abs(i["X"]), Y=i["Y"]+gcp.layer_width*0.5*i["Y"]/abs(i["Y"]), F=i["F"])
            elif i.get("X"):
                gcp.linear_move(X=i["X"]+gcp.layer_width*0.5*i["X"]/abs(i["X"]), F=i["F"])
            elif i.get("Y"):
                gcp.linear_move(Y=i["Y"]+gcp.layer_width*0.5*i["Y"]/abs(i["Y"]), F=i["F"])

        cur_temp += delta_temp
        gcp.set_temp(hotend_temp=round(cur_temp, 1))

    gcp.after_end()


def main(args):
    if len(args) == 1:
        print("Программе для работы требуются передаваемые флаги, для справки используйте \"-h\"")
        return

    if args[1] in ("-h", "--help"):
        print("""У программы два режима:\n
        1. python/python3 temp_calibration.py -n
        Создание нового файла конфигурации, он будет создан в той же директории с названием \"new_config.json\"\n
        2. python/python3 temp_calibration.py -c [файл конфигурации] -o [название выходного файла]
        Генерация G-code-а, который будет сохранён в файл с заданным именем.
        """)
        return

    if args[1] in ("-n", "--newconfig"):
        generate_json()
        return

    if "-c" in args and "-o" in args and len(args) == 5:
        args.index("-c")
        if os.path.isfile(args[args.index("-c") + 1]):
            conf_file = open(args[args.index("-c") + 1])
            conf = json.load(conf_file)
            conf_file.close()
            out_path = args[args.index("-o") + 1]
            try:
                out = open(out_path, "w", encoding="utf8")
            except FileNotFoundError:
                print("Невозможно создать выходной файл. Допущена ошибка в пути.")
                return
            except PermissionError:
                print("Невозможно создать выходной файл. Недостаточно прав.")
                return
            except Exception as err:
                print(err)
                return

            generate_gcode(conf, out_path)

        else:
            print("trouble")

        return

    print("Что-то пошло не так, посмотрите справку \"-h\".")


if __name__ == "__main__":
    main(sys.argv)
