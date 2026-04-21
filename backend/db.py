import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="db.fejiwqlhufkvxlgfiblb.supabase.co",
        database="postgres",
        user="postgres",
        password="pranav@8468898011",
        port=5432
    )