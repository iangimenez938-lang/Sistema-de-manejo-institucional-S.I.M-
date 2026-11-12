# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app-content/launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('app-content', 'app-content'), ('version.json', '.')],
    hiddenimports=['webbrowser', 'tkinter.filedialog', 'matematica.matematica_app', 'quimica.quimica_app', 'historia.historia_app', 'lengua.lengua_app', 'configuracion.opciones_app', 'creditos_app'],
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
    [],
    exclude_binaries=True,
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='launcher',
)
