# -*- mode: python ; coding: utf-8 -*-

edge_detection_a = Analysis(
    ['edge_detection.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
edge_detection_pyz = PYZ(edge_detection_a.pure)

edge_detection_exe = EXE(
    edge_detection_pyz,
    edge_detection_a.scripts,
    [],
    exclude_binaries=True,
    name='edge_detection',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


gray_value_transform_a = Analysis(
    ['gray_value_transform.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
gray_value_transform_pyz = PYZ(gray_value_transform_a.pure)

gray_value_transform_exe = EXE(
    gray_value_transform_pyz,
    gray_value_transform_a.scripts,
    [],
    exclude_binaries=True,
    name='gray_value_transform',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


img_enhanecement_a = Analysis(
    ['img_enhanecement.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
img_enhanecement_pyz = PYZ(img_enhanecement_a.pure)

img_enhanecement_exe = EXE(
    img_enhanecement_pyz,
    img_enhanecement_a.scripts,
    [],
    exclude_binaries=True,
    name='img_enhanecement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


img_filtering_a = Analysis(
    ['img_filtering.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
img_filtering_pyz = PYZ(img_filtering_a.pure)

img_filtering_exe = EXE(
    img_filtering_pyz,
    img_filtering_a.scripts,
    [],
    exclude_binaries=True,
    name='img_filtering',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


line_circle_fitting_a = Analysis(
    ['line_circle_fitting.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
line_circle_fitting_pyz = PYZ(line_circle_fitting_a.pure)

line_circle_fitting_exe = EXE(
    line_circle_fitting_pyz,
    line_circle_fitting_a.scripts,
    [],
    exclude_binaries=True,
    name='line_circle_fitting',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


morpology_transform_a = Analysis(
    ['morpology_transform.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
morpology_transform_pyz = PYZ(morpology_transform_a.pure)

morpology_transform_exe = EXE(
    morpology_transform_pyz,
    morpology_transform_a.scripts,
    [],
    exclude_binaries=True,
    name='morpology_transform',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
        edge_detection_exe,
        edge_detection_a.binaries,
        edge_detection_a.datas,
        gray_value_transform_exe,
        gray_value_transform_a.binaries,
        gray_value_transform_a.datas,
        img_enhanecement_exe,
        img_enhanecement_a.binaries,
        img_enhanecement_a.datas,
        img_filtering_exe,
        img_filtering_a.binaries,
        img_filtering_a.datas,
        line_circle_fitting_exe,
        line_circle_fitting_a.binaries,
        line_circle_fitting_a.datas,
        morpology_transform_exe,
        morpology_transform_a.binaries,
        morpology_transform_a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='pycv2024',
    )
