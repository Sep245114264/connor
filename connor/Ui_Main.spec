# -*- mode: python -*-

block_cipher = None


a = Analysis(['Ui_Main.py'],
             pathex=['G:\\PyQt5\\connor\\', 'G:\\PyQt5\\connor'],
             binaries=[],
             datas=[],
             hiddenimports=['animate', 'autoFormat', 'bookmark', 'label', 'lineEdit', 'orderProcess', 'register', 'trayIcon'],
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
          name='Ui_Main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
