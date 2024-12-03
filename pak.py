import os
import subprocess
import sys
from glob import glob

project_root = r'G:\Desktop\WordForest'  # 使用原始字符串
main_script = os.path.join(project_root, 'main.py')

# 设置要打包的资源文件夹
resources_folders = ['music', 'font', 'assets']  # 资源文件夹路径
resources = []

# 收集资源文件
for folder in resources_folders:
    resources.extend(glob(os.path.join(project_root, folder, '*')))
# 收集所有 JPG 文件
resources.extend(glob(os.path.join(project_root, '*.jpg')))

# 格式化数据
datas_str = ',\n    '.join([f"('{src}', '{os.path.basename(src)}')" for src in resources])

# 定义生成 .spec 文件
def create_spec_file():
    spec_content = f"""
# -*- mode: python -*-
block_cipher = None

a = Analysis(['{main_script}'],
             pathex=['{project_root}'],
             binaries=[],
             datas=[{datas_str}],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={{}},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='WordForest',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='WordForest')
"""
    # 保存 .spec 文件
    spec_file = os.path.join(project_root, 'my_project.spec')
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print(f'Successfully created spec file: {spec_file}')

# 执行打包
if __name__ == '__main__':
    create_spec_file()
