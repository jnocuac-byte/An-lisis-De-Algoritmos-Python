# AnalisisAlgoritmos.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('AnalisisDeAlgoritmos', 'AnalisisDeAlgoritmos'),
        ('AnalisisDeAdO', 'AnalisisDeAdO'),
        ('theme.py', '.'),
        ('info_windows.py', '.'),
        ('main_menu.py', '.'),
    ],
    hiddenimports=[
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'numpy',
        'tkinter',
        'complexity_detector',
        'code_executor',
        'complexity_analyzer',
        'tutorial_helper',
        'tutorial_helper2',
        'ejemplos_python',
        'sorting_algorithms',
        'dataset_manager',
        'sorting_analyzer',
        'bar_comparison',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnalisisDeAlgoritmos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = sin consola, True = con consola (útil para debug)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un icono aquí: icon='icono.ico'
)