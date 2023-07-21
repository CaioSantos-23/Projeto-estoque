import sys
import os
from cx_Freeze import setup, Executable

# Informe aqui o nome do arquivo que contém a interface
target_file = "estoquepoo.py"

# Dependências adicionais, se necessário
build_exe_options = {
    "packages": ["tkinter", "pandas", "numpy"],
    "include_files": [("venv\\Lib\\python310.dll", "python310.dll"), "data/Estoque_com_codigo_de_barras.xlsx"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Utilize "Win32GUI" para ocultar a janela de console no Windows

# Configuração do executável
executables = [Executable(target_file, base=base)]

# Configuração do pacote
setup(
    name="Controle de Estoque",
    version="1.0",
    description="Programa para controle interno do estoque usando planilha com DB",
    options={"build_exe": build_exe_options},
    executables=executables
)
