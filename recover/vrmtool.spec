# -*- mode: python -*-

block_cipher = None


#a = Analysis(['vrmtool.py', 'polaris10.py', 'exeio.py', 'smu_7_1_3.py', 'gfx80.py'],
a = Analysis(['vrmtool.py'],
             pathex=['C:\\Users\\Peter Banane\\Desktop\\python\\VRMtool'],
             binaries=None,
             datas=[('Exeio.dll', '.'),
                       ('EIO.dll', '.'),
                       ('IOMap.sys', '.'),
                       ('IOMap64.sys', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='vrmtool',
          debug=False,
          strip=False,
          upx=True,
          console=True )
