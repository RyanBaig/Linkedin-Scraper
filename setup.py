from cx_Freeze import setup, Executable

build_exe_options = {
    'packages': ['ttkbootstrap', 'requests', 'bs4', 'PIL'],
    'include_files': ["icons"]
}

setup(
    name='LinkedIn Scraper',
    version='1.0',
    description='LinkedIn Scraper by Ryan Baig.',
    options={'build_exe': build_exe_options},
    executables=[Executable('main.py')]
)
