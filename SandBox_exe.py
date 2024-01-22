import cx_Freeze


executables = [cx_Freeze.Executable('game.py',
                                    base='Win32GUI',
                                    icon='images/icon.ico',
                                    shortcut_dir='DesktopFolder',
                                    shortcut_name='SandBox')]

cx_Freeze.setup(
    name='SandBox', options={'build_exe': {'packages': ['pygame'],
                                           'include_files': [
                                               'images',
                                               'PixeloidMono-d94EV.ttf',
                                               'saves']},
                             "bdist_msi": {'target_name': '2048.msi',
                                           'install_icon': 'images/icon.ico'}},
    executables=executables)
