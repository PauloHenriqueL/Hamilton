# Hamilton - Sistema de Gestão para Clínicas de Psicologia 🧠

O **Hamilton** é uma aplicação web desenvolvida para automatizar a gestão administrativa e clínica de consultórios de psicologia. O sistema facilita o controle de pacientes, agendamentos e faturamento, unindo segurança de dados com uma interface funcional.

Funcionalidades Principais
* Gestão Clínica de Pacientes: Cadastro completo com histórico de sessões, evolução clínica e proteção de dados sensíveis.

* Controle de Agendamentos e Horários: Gestão dinâmica de calendários para múltiplos terapeutas, evitando conflitos de horários e otimizando a agenda da clínica.

* Módulo Fiscal e Financeiro: Emissão de notas fiscais, gestão de pagamentos, faturamento de sessões e relatórios automáticos de fluxo de caixa.

* Dashboards de Performance: Painéis de controle visual para acompanhamento em tempo real do faturamento, taxa de ocupação e resultado da clínica.

* Sistema de Supervisão: Módulo específico para terapeutas em treinamento, permitindo o acompanhamento técnico e pedagógico por supervisores.

* Painel Administrativo: Interface intuitiva para controle de permissões e gestão de usuário

## 🛠️ Tecnologias Utilizadas

* **Backend:** [Django](https://www.djangoproject.com/) (Python)
* **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/) (Hospedado via Neon DB)
* **Infraestrutura:** [Render](https://render.com/) (Deployment e Hosting)
* **Integrações:** APIs REST para comunicação entre módulos.

## 🏗️ Arquitetura do Projeto

O projeto segue o padrão **MVT (Model-View-Template)** do Django, com foco em:
1.  **Normalização de Dados:** Banco de dados estruturado para garantir performance em operações transacionais.
2.  **Segurança:** Implementação de middlewares de autenticação e proteção de dados sensíveis dos pacientes.
3.  **Escalabilidade:** Configurado para rodar em ambientes de nuvem (PaaS) com variáveis de ambiente protegidas.
