# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['service_hub_gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('./assets/icon.png', 'assets'),
        ('./assets/pyinstaller_icon.png', 'assets'),
    ],
    hiddenimports=[
    'ui.dialogs.add_service_dialog',
    'ui.dialogs.service_menu_dialog',
    'ui.system_tray',
    'ui.service_profile',
    'core.event_bus',
    'css.css',
    'service_hub_ipc.utils'
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
    name='service_hub_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="./assets/pyinstaller_icon.png",
)

