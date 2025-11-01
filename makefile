
DB_URL ?= $(DATABASE_URL)

# Gera uma nova migration automaticamente (passar mensagem: make migration m="create users table")
migration:
	@if [ -z "$(m)" ]; then \
		echo "Informe uma mensagem: make migration m=\"mensagem\""; \
		exit 1; \
	fi
	@echo "Gerando migration: $(m)"
	@DATABASE_URL=$(DB_URL) python3 -m alembic revision --autogenerate -m "$(m)"

# Aplica todas as migrations até a última (head)
upgrade:
	@echo "Aplicando migrations até head..."
	@DATABASE_URL=$(DB_URL) python3 -m alembic upgrade head

# Faz downgrade (ex: make downgrade rev=-1)
downgrade:
	@if [ -z "$(rev)" ]; then \
		echo "Informe a revisão: make downgrade rev=-1"; \
		exit 1; \
	fi
	@echo "Fazendo downgrade até $(rev)..."
	@DATABASE_URL=$(DB_URL) python3 -m alembic downgrade $(rev)

# Mostra histórico de migrations
history:
	@DATABASE_URL=$(DB_URL) python3 -m alembic history --verbose

# Verifica o estado atual do banco
current:
	@DATABASE_URL=$(DB_URL) python3 -m alembic current

# ===========================================
# COMANDOS PARA DADOS DE TESTE E SERVIDOR
# ===========================================

# Insere dados de teste no banco
seed-test:
	@echo "🌱 Inserindo dados de teste..."
	@./venv/bin/python manage_test_data.py seed

# Remove dados de teste do banco
clear-test:
	@echo "🧹 Removendo dados de teste..."
	@./venv/bin/python manage_test_data.py clear

# Reset completo dos dados de teste (limpar + inserir)
reset-test:
	@echo "🔄 Resetando dados de teste..."
	@./venv/bin/python manage_test_data.py reset

# Inicia o servidor de desenvolvimento
dev:
	@echo "🚀 Iniciando servidor de desenvolvimento..."
	@./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Comando principal: reseta dados de teste e inicia o servidor
start: reset-test dev
