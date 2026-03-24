# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['build_entry.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'ezdxf',
        'ezdxf.addons.drawing',
        'ezdxf.addons.drawing.svg',
        'ezdxf.addons.drawing.layout',
        'ezdxf.addons.drawing.config',
        'PIL',
        'PIL._imaging',
        'ezdxf_converter',
        'ezdxf_converter.cli',
        'ezdxf_converter.converter',
        'ezdxf_converter.utils',
        'ezdxf_converter.dwg_handler',
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
    name='ezdxf-convert',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
