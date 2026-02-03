📱 Gestor de Despesas – Aplicação Mobile

Aplicação mobile de gestão de despesas pessoais, desenvolvida em Python com Flet, com Firebase como backend.
O projeto foi concebido com foco em organização financeira, boa arquitetura de software, validação de dados e experiência do utilizador.

A aplicação segue o padrão MVC (Model–View–Controller), garantindo uma separação clara de responsabilidades, código limpo, facilidade de manutenção e elevada escalabilidade.

🎯 Objetivo do Projeto

O objetivo principal desta aplicação é permitir ao utilizador:

  Controlar despesas de forma simples e organizada

  Acompanhar o saldo disponível em tempo real

  Consultar históricos e estatísticas mensais
  
Ter uma base sólida e escalável para futuras evoluções

Este projeto foi desenvolvido como Projeto Final, servindo também como demonstração prática de competências em desenvolvimento mobile, lógica de negócio e integração com serviços externos.

🏗️ Arquitetura

A aplicação segue o padrão MVC (Model–View–Controller):

  Controllers
  Responsáveis pela lógica da aplicação, validação de dados e comunicação entre a UI e os serviços.

  Services
  Encapsulam o acesso ao Firebase (Authentication e Firestore), garantindo isolamento da lógica de dados.

  Views
  Responsáveis exclusivamente pela interface gráfica, utilizando componentes reutilizáveis do Flet.

Esta abordagem torna o projeto:

  Mais organizado

  Mais fácil de testar

  Mais simples de escalar e manter
  

🔧 Tecnologias Utilizadas

  Python <img align="center" alt="Python" height="30" width="40"
src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">–> linguagem principal

  Flet <img align="center" alt="Flet" height="30" width="40"
src="https://raw.githubusercontent.com/flet-dev/flet/main/media/logo/flet-logo.svg">–> framework para UI mobile multiplataforma

  Firebase Authentication <img align="center" alt="Firebase" height="30" width="40"
src="https://raw.githubusercontent.com/devicons/devicon/master/icons/firebase/firebase-plain.svg">–> autenticação de utilizadores

  Firebase Firestore <img align="center" alt="Firebase" height="30" width="40"
src="https://raw.githubusercontent.com/devicons/devicon/master/icons/firebase/firebase-plain.svg">–> base de dados NoSQL

  MVC Pattern <img align="center" alt="MVC Architecture" height="30" width="40"
src="https://raw.githubusercontent.com/andrews1022/readme-icons/main/icons/mvc.svg">
–> arquitetura da aplicação
  

📱 Funcionalidades Principais

🔐 Autenticação de utilizador

  Registo

  Login

  Recuperação de palavra-passe
  

💰 Gestão de saldo

  Definição e atualização do saldo

  Cálculo automático após despesas

🧾 Registo de despesas

  Por categoria

  Categoria personalizada

  Validação de valores e datas

📜 Histórico de movimentos

  Visualização cronológica

  Eliminação de movimentos com rollback de saldo

📊 Estatísticas mensais

  Gráfico por categoria

  Total gasto por mês

  Histórico filtrado por mês/ano

👤 Perfil do utilizador

  Atualização de dados pessoais

  Seleção de avatar

  Eliminação de conta
  
  
🔐 Segurança

  Credenciais do Firebase protegidas por variáveis de ambiente

  .env e ficheiros sensíveis excluídos via .gitignore

  Separação clara entre lógica, dados e interface
  

🚀 Escalabilidade e Melhorias Futuras

A aplicação foi desenvolvida de forma escalável, permitindo facilmente:

  📤 Exportação de relatórios financeiros (PDF / Excel)

  📊 Gráficos avançados e comparativos

  🔄 Sincronização offline

  🎨 Melhorias no layout e responsividade

  📱 Publicação em Android / iOS
  

🧠 Principais Desafios

  Validação correta de dados introduzidos pelo utilizador

  Gestão consistente do saldo e rollback de operações

  Organização da arquitetura MVC

  Integração fluida entre UI e Firebase




<img width="1920" height="1080" alt="Blue and White Gradient Modern Project Presentation" src="https://github.com/user-attachments/assets/2dc3cc8a-68c4-4413-ba3e-6a0a9277360e" />

