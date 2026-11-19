
# RAG System for Online Shop

## Technology Stack

- Python
- SQLite
- SQLAlchemy 2.0
- Pydantic
- NumPy

## Database Design

The system uses SQLite as its database engine.

The database contains 11 core tables:

1. customers
2. user_credentials
3. categories
4. products
5. orders
6. order_items
7. shipments
8. chat_sessions
9. chat_messages
10. knowledge_documents
11. document_chunks

## Installation

Create virtual environment:

python -m venv .venv

Activate on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Environment Configuration

Copy .env.example to .env.

Configure Qwen API credentials when needed.

## Initialize Database

Run:

python -c "from backend.database.connection import create_tables; create_tables()"

## Insert Sample Data

Run:

python -m backend.database.seed_data

## Database Location

database/onlshop.db

## Important Notes

- SQLite does not require a database server.
- Foreign key constraints are enabled.
- UUID values are stored as strings.
- Embeddings are stored as JSON arrays.
- Vector similarity search will be implemented in the RAG module.
