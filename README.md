# TCC - Gerenciador de Peladas

Este projeto é um sistema web para gerenciamento de peladas (jogos de futebol amador), permitindo criar partidas, cadastrar jogadores, editar atributos e sortear times de forma equilibrada.

## Funcionalidades
- Cadastro e login de usuários
- Criação, edição e exclusão de peladas
- Cadastro, edição e remoção de jogadores em cada pelada
- Atributos individuais para cada jogador (ataque, defesa, velocidade, passe, controle)
- Seleção de jogadores para sorteio
- Sorteio automático de times equilibrados usando otimização matemática
- Interface web amigável

## Estrutura do Projeto
```
fut_app/
  pelada/
    models.py           # Modelos do domínio (Pelada, ParticipantePelada)
    repository/         # Repositórios de acesso a dados
    service/            # Serviços com regras de negócio
    views.py            # Views (controladores) Django
    templates/          # Templates HTML
    static/             # Arquivos estáticos (CSS, JS)
  usuarios/             # App de autenticação e usuários
  manage.py             # Gerenciador Django
requirements.txt        # Dependências do projeto
```

## Arquitetura
O projeto segue uma arquitetura em camadas, inspirada na arquitetura hexagonal (Ports & Adapters):
- **Modelos**: entidades do domínio
- **Repositórios**: abstraem o acesso a dados
- **Serviços**: concentram regras de negócio
- **Views**: controladores que recebem requisições e orquestram as operações
- **Templates/Static**: camada de apresentação

Essa separação facilita manutenção, testes e evolução do sistema.

## Tecnologias Utilizadas
- Python 3
- Django
- pandas
- PuLP (otimização)
- HTML, CSS, JavaScript

## Como rodar localmente
1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```
4. Crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```
5. Rode o servidor:
   ```bash
   python manage.py runserver
   ```
6. Acesse em [http://localhost:8000](http://localhost:8000)


## Autor
Desenvolvido por Alessandro D'Angelo para Trabalho de Conclusão de Curso (TCC).

---
Sinta-se à vontade para contribuir ou sugerir melhorias!