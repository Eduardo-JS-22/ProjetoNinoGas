# ProjetoNinoGas
Projeto criado para o desenvolvimento de um aplicativo de controle de cobranças para a revenda de gás "Nino Gás".

Instalar Python 3.12.4 da internet e adicionar no diretório C:\python312 e marcar opção path durante a instalação: https://www.python.org/downloads/windows/

Abrir o terminal na pasta do python e instalar:
Instalar o pyqt5: pip install pyqt5
Instalar o pyinstaller: pip install pyinstaller

Criar aplicativo:
Rodar o comando no terminal do projeto: pyinstaller --windowed Controle_de_Cobranças.py
Copiar para a pasta dist/Controle_de_Cobranças: banco_de_dados_nino_gas.db, Controle_de_Cobranças.py, logo_X0P_icon.ico e logo.png
Cria um atalho na área de tarefas e altera o nome e o ícone

P.S. o updatedb.py serve para excluir todos os dados do banco de dados e zerar a sequencia do id das tabelas. USE COM MODERAÇÃO