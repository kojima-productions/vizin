# vizin
Vizin é uma aplicação web de gerenciamento de condominio, com o objetivo de aproximar a comunicação entre a gestão condominial, moradores e funcionários, além de facilitar processos do cotidiano por meio de uma plataforma centralizada.

## Objetivos
A aplicação busca atender necessidades comuns como: 
- Cadastro de veiculos e vagas de garagem;
- Controle e registro de visitantes;
- Realização de reclamações e solicitações;
- Agendamento de áreas de lazer;
- Acesso ao quadro de funcionários disponiveis no dia;
- Visualizar boletos referentes a mensalidades e rateios;
- Acompanhar avisos e comunicados publicados pela administração;
- Receber notificação sobre encomendas recebidas;

## Motivações
Oferecer praticidade, organização e maior transparência na administração do condominio.

## Tecnologias
Para o desenvolvimento utilizaremos:
| Ferramenta | Versão |
| :---: | :---: |
| Python | 3.13.5 |
| Django | 6.0.4 |
| Supabase | --  |

## Executando o projeto

Para executar o projeto é necessário:
- Inserir arquivo .env na raiz do projeto django 'vizin/', junto a manage.py e os demais diretórios referentes ao django.
- Instalar os pacotes necessários com `pip install -r requirements.txt`
- Executar o projeto com `python manage.py runserver` 

**OBS:** Como o supabase é construido em cima da estrutura do postgresql, para o funcionamento correto das funcionalidades referentes ao CRUD é preciso ter o postgresql 18.4 instalado
