<h1>Projeto Controle de Cobranças Nino Gás</h1>

<p>Projeto desenvolvido e mantido por: <b>Eduardo José Schroeder</b></p>

<br><p>Essa descrição complementa a <a href="Outros Documentos/Apresentação Gerenciamento de Cobranças.pptx">Apresentação do Projeto</a> e o <a href="Outros Documentos/Manual Controle de Cobranças.pdf">Manual da Aplicação</a>.</p>

<br><p><b>Dados de Contato do Autor:</b></p>
<p><a href="https://www.mozilla.org/pt-BR/">Linkedin</a></p>
<p><a href="mailto:eduardoj.schroeder@gmail.com">E-Mail</a></p>

<p><b>Dados de Contato do Cliente</b></p>
<p><a href="https://www.facebook.com/profile.php?id=100047713645207">Facebook</a></p>

<br><h2>O Nino Gás</h2>
<p>Nino Gás, uma tradicional revenda de gás em Rio Negrinho, Santa Catarina, e afiliada à Supergasbras, se destaca como uma das maiores revendas da região. Em 2024, após a aquisição da concorrente Itagás, a empresa se deparou com um desafio: a gestão das vendas a prazo, prática comum da antiga proprietária. Diante de dificuldades no controle de cobranças, a Nino Gás optou por automatizar esse processo, buscando um software customizado que atendesse às suas necessidades específicas de gerenciamento de cobranças ativas.</p>

<br><h2>O Projeto</h2>
<p>Sistema desenvolvido para permitir o cadastramento de clientes que realizam compras a prazo e o registro das cobranças associadas a esses clientes. O controle das cobranças é realizado com base na data de vencimento, e as informações são enviadas aos entregadores de gás via WhatsApp. Após o pagamento das cobranças e sua baixa no sistema, os registros permanecem armazenados no histórico por um período de 2 anos, podendo ser filtrados por nome do cliente ou data de pagamento.</p>

<br><h2>Detalhes Tecnicos</h2>
<p>O sistema foi desenvolvido utilizando a linguagem Python para o back-end, enquanto a biblioteca de interface gráfica PyQt foi empregada no front-end. O armazenamento de dados é realizado com o banco de dados SQLite, e a criação do executável foi feita utilizando a biblioteca PyInstaller. Todo o processo de execução do aplicativo ocorre no computador Windows do cliente, não sendo necessário acesso à internet para sua operação.</p>

<h3>Tela Incial</h3>
<p>Tela inicial que lista as cobranças vencidas que ainda não foram pagas pelos clientes dentro da data de vencimento e possibilita um acesso rapido as funções de copiar cobranças para o WhatsApp ou outro aplicativo de mensagens.</p>
<img src="/Imagens/Captura de tela 2024-08-12 095617.png">

<h3>Tela de Clientes</h3>
<p>Tela que lista todos os clientes cadastrados no sistema, possibilita via botões adicionar novos clientes ou atualizar clientes atuais.</p>
<img src="/Imagens/Captura de tela 2024-08-12 095925.png">

<h3>Tela de Cobranças</h3>
<p>Tela que lista todas as cobranças ativas, que ainda não foram pagas pelos clientes, possibilita via botões copiar todas as cobranças, copiar apenas as cobranças vencidas, criar novas cobranças e encerrar cobranças pagas.</p>
<img src="/Imagens/Captura de tela 2024-08-12 100125.png">

<h3>Tela de Histórico</h3>
<p>Tela que lista todas as cobranças que foram pagas pelos clientes e dadas baixas no sistema, ficando arquivadas por um período de 2 anos, após a data, são excluidas automaticamente. Permite-se filtrar, via botões, pelo nome do cliente ou pela data de pagamento, em ambos, permite-se também copiar apenas as cobranças filtradas.</p>
<img src="/Imagens/Captura de tela 2024-08-12 100313.png">

<br><h2>Processo de Instalação</h2>
<p>Para realizar a instalação e execução da aplicação é necessário ter instalado:</p>
<b>Python</b>
<p>Baixe e instale o Python na versão 3.12.4 ou superior, adicionando ao diretório C:\python312 e marcar opção path durante a instalação, para simplificar a instalação.</p>
<b>PyQt5</b>
<p>Abrindo o terminal no diretório de instalação do Python e executado o comando: pip install pyqt5</p>
<b>PyInstaller</b>
<p>Abrindo o terminal no diretório de instalação do Python e executado o comando: pip install pyinstaller</p>
<p>Após instalado o Python e as dependências, será necessário copiar esse repositório, acessar o diretório e procurar pelo caminho "dist/Controle de Cobrancas" e copiar o arquivo .exe como atalho para o local desejado, podendo alterar o nome e ou o ícone.</p>
<p>P.S. o updatedb.py serve para excluir todos os dados do banco de dados e zerar a sequencia do id das tabelas. USE COM MODERAÇÃO</p>
