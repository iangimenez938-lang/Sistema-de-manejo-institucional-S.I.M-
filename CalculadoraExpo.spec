# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app-content/launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app-content', 'app-content'),
        ('version.json', '.'),
    ],
    hiddenimports=[
        'webbrowser',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.colorchooser',
        'tkinter.font',
        'tkinter.messagebox',
        'tkinter.ttk',
        'matematica.matematica_app',
        'quimica.quimica_app',
        'historia.historia_app',
        'lengua.lengua_app',
        'configuracion.opciones_app',
        'creditos_app',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CalculadoraExpo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
