import os.path
import sys


def generate_json():
    pass


def choose_json():
    pass


def main(args):
    if len(args) == 1:
        print("Программе для работы требуются передаваемые флаги, для справки используйте \'-h\'")
        return
    if args[1] in ('-h', '--help'):
        print("Help text")
    if args[1] in ('-cd', '--configdir'):
        try:
            if os.path.isdir(os.path.join(*(args[2].split('\\')))):
                config_path = args[2]
                print(f"Назначена новая директория с файлами конфигурации: {config_path}")
            else:
                print(f"Указанный путь не существует. {args[2]}")
        except:
            print(f"Путь не указан или указан неправильно.")
            print(os.path.join(*(args[2].split('\\'))))
    if args[1] in ('-nc', '--newconfig'):
        pass
    if args[1] in ('-cf', '--configfile'):
        pass
    if args[1] in ('-o', '--output'):
        pass


if __name__ == "__main__":
    main(sys.argv)
