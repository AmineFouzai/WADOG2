import os
import PyInstaller.__main__
def build(path):
    PyInstaller.__main__.run([
    '--onefile',
    # '--noconsole',
    '--icon=wadog.ico',
    os.path.join(path)
    ])