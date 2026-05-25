# 🎓 UniTrack v2

Sistema de controle de notas e frequência universitária com login multi-usuário.

## O que o app faz

- Cadastro de conta por usuário e senha
- Dados salvos no servidor, isolados por usuário
- Sessão persistente por 7 dias
- Cadastro de disciplinas com N1, N2 e N3
- Cálculo de média: `(N1 + N2 + N3) / 3`
- Média mínima para aprovação: 60
- Calculadora de quanto precisa tirar nas próximas avaliações
- Controle de faltas com presença mínima de 75%
- Regras de falta por carga horária:
  - 1 aula/semana = 2 créditos = até 8 faltas
  - 2 aulas/semana = 4 créditos = até 16 faltas
  - 3 aulas/semana = 6 créditos = até 18 faltas
- Exportar e importar backup em JSON

## Rodando localmente

### Pré-requisitos
- [Node.js](https://nodejs.org/) versão 18 ou superior

### Comandos

```bash
npm install
npm start
```

Acesse em **http://localhost:3000**

Para desenvolvimento com reload automático:
```bash
npm run dev
```

## Estrutura

```
UniTrack/
├── server.js
├── package.json
├── data/
│   └── db.json        ← criado automaticamente, não sobe pro GitHub
└── public/
    └── index.html
```

## Deploy em servidor (VPS)

```bash
npm install -g pm2
pm2 start server.js --name unitrack
pm2 save
pm2 startup
```

### Porta personalizada

```bash
PORT=8080 npm start
```

