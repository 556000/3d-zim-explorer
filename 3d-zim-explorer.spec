# -*- mode: python ; coding: utf-8 -*-
"""
3D ZIM Explorer PyInstaller spec
Build: pyinstaller 3d-zim-explorer.spec
Output: dist/3D-ZIM-Explorer/3D-ZIM-Explorer.exe
"""

import os, sys, glob

block_cipher = None

# Project root (where this spec file lives)
ROOT = os.path.abspath(SPECPATH)

# Static files to bundle
# Note: PyInstaller datas (src, dst) — if dst is 'filename', it creates a subdir.
# Use '.' to place files directly in _internal/
static_files = [
    ('index.html', '.'),
    ('three.min.js', '.'),
    ('OrbitControls.js', '.'),
]

datas = [(os.path.join(ROOT, src), dst) for src, dst in static_files]

# No data/ directory needed — users select ZIM file via web UI

# libzim native DLLs
site_packages = os.path.join(
    os.path.dirname(sys.executable), 'Lib', 'site-packages'
)

# Required DLLs for libzim
dll_names = [
    'zim-9.dll',
    'icudt74.dll',
    'icuin74.dll',
    'icuio74.dll',
    'icutu74.dll',
    'icuuc74.dll',
]

for dll in dll_names:
    dll_path = os.path.join(site_packages, dll)
    if os.path.exists(dll_path):
        datas.append((dll_path, '.'))
    else:
        print(f"WARNING: {dll} not found at {dll_path}")

# libzim .pyd file
pyd_path = os.path.join(site_packages, 'libzim.cp312-win_amd64.pyd')
if os.path.exists(pyd_path):
    datas.append((pyd_path, '.'))
else:
    print(f"WARNING: libzim.pyd not found")

# zhconv data files (zhcdict.json)
zhconv_dir = os.path.join(site_packages, 'zhconv')
zhconv_data = os.path.join(zhconv_dir, 'zhcdict.json')
if os.path.exists(zhconv_data):
    datas.append((zhconv_data, 'zhconv'))
else:
    print(f"WARNING: zhconv/zhcdict.json not found at {zhconv_data}")

a = Analysis(
    [os.path.join(ROOT, 'server.py')],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'libzim',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'anyio._backends._asyncio',
        'bs4',
        'zhconv',
        'python_multipart',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'PIL',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'selenium',
        'pytest',
    ],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='3D-ZIM-Explorer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='3D-ZIM-Explorer',
)
