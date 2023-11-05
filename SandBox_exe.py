import cx_Freeze
from config import all_files

executables = [cx_Freeze.Executable('game.py',
                                    base='Win32GUI',
                                    icon='icon.ico',
                                    shortcut_dir='DesktopFolder',
                                    shortcut_name='SandBox')]

cx_Freeze.setup(
    name='SandBox', options={'build_exe': {'packages': ['pygame'],
                                           'include_files': all_files},
                             "bdist_msi": {'target_name': '2048.msi',
                                           'install_icon': 'images/icon.ico'}},
    executables=executables)
