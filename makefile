# Variável de ambiente com a URL do banco
# Exemplo: export DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
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
