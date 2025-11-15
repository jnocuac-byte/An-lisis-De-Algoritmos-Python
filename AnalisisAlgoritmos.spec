# AnalisisAlgoritmos.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # 1. Ajuste de DATAS (Asumiendo que 'AnalisisDeAlgoritmos' y 'AnalisisDeAdO'
    # son carpetas que contienen todos tus módulos y datos)
    datas=[
        # Se asume que estos son directorios. Si son módulos de Python, deberían ir a 'hiddenimports'.
        ('AnalisisDeAlgoritmos', 'AnalisisDeAlgoritmos'), 
        ('AnalisisDeAdO', 'AnalisisDeAdO'),
        
        # Estas referencias a archivos individuales probablemente no son necesarias 
        # si están en las carpetas de arriba o si PyInstaller los encuentra
        ('theme.py', '.'), 
        ('info_windows.py', '.'),
        ('main_menu.py', '.'),
    ],
    hiddenimports=[
        # ... (Tu lista de hiddenimports es correcta y extensa)
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
    name='AdA25',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # console=False indica que es una app con interfaz gráfica (sin ventana negra)
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 2. CAMBIO CLAVE: Agrega la ruta del icono aquí. Debe ser un archivo .ICO
    icon='Puzle.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AdA25',
)