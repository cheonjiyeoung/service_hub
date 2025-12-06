# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('./assets/icon.png', 'assets'),
        ('./assets/icon_pyinstaller.png', 'assets'),
    ],
    hiddenimports=[
    'ui.dialogs.add_service_dialog',
    'ui.dialogs.service_menu_dialog',
    'ui.system_tray',
    'ui.main_window',
    'core.service_profile',
    'core.event_bus',
    'css.css',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)

