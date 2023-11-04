import os


def get_files():
    all_files = []
    files = os.listdir()
    for file in files:
        if (file.endswith('.py') or
            file.endswith('.ttf') or
                file.endswith('.png')) and file != 'SandBox.py':
            all_files.append(file)
    print(all_files)
    return all_files


print(get_files())
