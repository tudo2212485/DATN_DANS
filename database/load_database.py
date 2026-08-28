import sys
import os
import psycopg2

# Đảm bảo UTF-8 trên Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def init_postgres():
    db_user = os.getenv("PGUSER", "postgres")
    db_pass = os.getenv("PGPASSWORD", "postgres")
    db_host = os.getenv("PGHOST", "localhost")
    db_port = os.getenv("PGPORT", "5432")

    print(f"[*] Đang kết nối tới PostgreSQL ({db_host}:{db_port}) bằng user '{db_user}'...")

    # 1. Kết nối database mặc định 'postgres' để kiểm tra và tạo 'agroforecast_db'
    try:
        conn = psycopg2.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            dbname="postgres"
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'agroforecast_db';")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE agroforecast_db ENCODING 'UTF8';")
            print("[+] Đã tạo mới cơ sở dữ liệu 'agroforecast_db' thành công!")
        else:
            print("[✓] Cơ sở dữ liệu 'agroforecast_db' đã tồn tại sẵn.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[!] Lỗi kết nối PostgreSQL bước 1: {e}")
        return False

    # 2. Kết nối vào 'agroforecast_db' và thực thi 'init.sql'
    try:
        conn_app = psycopg2.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            dbname="agroforecast_db"
        )
        cur_app = conn_app.cursor()

        sql_path = os.path.join(os.path.dirname(__file__), "init.sql")
        print(f"[*] Đang nạp file '{sql_path}' vào 'agroforecast_db'...")
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_content = f.read()

        cur_app.execute(sql_content)
        conn_app.commit()
        print("[+] Đã nạp toàn bộ cấu trúc bảng và Seed Data vào 'agroforecast_db' thành công!")

        # 3. Kiểm tra số lượng bản ghi
        cur_app.execute("SELECT COUNT(*) FROM commodities;")
        c_count = cur_app.fetchone()[0]
        cur_app.execute("SELECT COUNT(*) FROM price_history;")
        p_count = cur_app.fetchone()[0]
        cur_app.execute("SELECT COUNT(*) FROM forecasts;")
        f_count = cur_app.fetchone()[0]
        cur_app.execute("SELECT COUNT(*) FROM alert_rules;")
        a_count = cur_app.fetchone()[0]

        print(f"\n[📊 XÁC THỰC DỮ LIỆU ĐÃ NẠP]:")
        print(f" - Số loại nông sản (commodities): {c_count}")
        print(f" - Số bản ghi lịch sử giá (price_history): {p_count}")
        print(f" - Số bản ghi dự báo (forecasts): {f_count}")
        print(f" - Số quy tắc cảnh báo (alert_rules): {a_count}")

        cur_app.close()
        conn_app.close()
        return True
    except Exception as e:
        print(f"[!] Lỗi khi nạp init.sql vào database: {e}")
        return False

if __name__ == "__main__":
    success = init_postgres()
    if not success:
        sys.exit(1)
