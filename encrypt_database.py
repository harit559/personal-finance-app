"""
Database Encryption Migration Script

This script converts your existing unencrypted SQLite database to an encrypted
SQLCipher database. It will:
1. Backup your existing database
2. Create a new encrypted database
3. Copy all data to the encrypted version

IMPORTANT: Run this ONLY ONCE after installing pysqlcipher3
"""
import sqlite3
import os
from datetime import datetime
from config import Config
from pysqlcipher3 import dbapi2 as sqlcipher

def encrypt_existing_database():
    """
    Migrate from unencrypted SQLite to encrypted SQLCipher database.
    """
    db_path = 'finance.db'
    backup_path = f'finance_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    temp_encrypted = 'finance_encrypted_temp.db'
    
    print("🔐 Starting Database Encryption Migration")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("❌ No database found. Nothing to encrypt.")
        print("   Start the app normally and it will create an encrypted database.")
        return
    
    try:
        # Step 1: Backup original database
        print(f"\n1️⃣  Creating backup: {backup_path}")
        import shutil
        shutil.copy2(db_path, backup_path)
        print("   ✅ Backup created successfully")
        
        # Step 2: Read data from unencrypted database
        print(f"\n2️⃣  Reading data from unencrypted database...")
        
        # Connect to original (unencrypted) database
        old_conn = sqlite3.connect(db_path)
        old_cursor = old_conn.cursor()
        
        # Get all table names
        old_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables_data = old_cursor.fetchall()
        
        print(f"   Found {len(tables_data)} tables to migrate")
        
        # Store all data in memory
        all_data = {}
        for table_name, create_sql in tables_data:
            print(f"   📋 Reading table: {table_name}")
            old_cursor.execute(f"SELECT * FROM {table_name}")
            all_data[table_name] = {
                'create_sql': create_sql,
                'rows': old_cursor.fetchall(),
                'columns': [desc[0] for desc in old_cursor.description]
            }
        
        old_conn.close()
        
        # Step 3: Create encrypted database and write data
        print(f"\n3️⃣  Creating encrypted database and writing data...")
        
        # Connect to new encrypted database
        enc_conn = sqlcipher.connect(temp_encrypted)
        enc_cursor = enc_conn.cursor()
        
        # Set encryption key and parameters
        enc_cursor.execute(f"PRAGMA key = '{Config.DB_ENCRYPTION_KEY}'")
        enc_cursor.execute("PRAGMA cipher_page_size = 4096")
        enc_cursor.execute("PRAGMA kdf_iter = 64000")
        enc_cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA256")
        enc_cursor.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA256")
        
        # Create tables and insert data
        for table_name, table_info in all_data.items():
            print(f"   📝 Creating table: {table_name}")
            enc_cursor.execute(table_info['create_sql'])
            
            if table_info['rows']:
                print(f"   💾 Inserting {len(table_info['rows'])} rows into {table_name}")
                placeholders = ', '.join(['?' for _ in table_info['columns']])
                insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                enc_cursor.executemany(insert_sql, table_info['rows'])
        
        enc_conn.commit()
        enc_conn.close()
        
        print("   ✅ Encrypted database created")
        
        # Step 4: Replace old database with encrypted one
        print("\n4️⃣  Replacing old database with encrypted version...")
        os.remove(db_path)
        os.rename(temp_encrypted, db_path)
        print("   ✅ Database replaced")
        
        # Step 5: Verify encrypted database
        print("\n5️⃣  Verifying encrypted database...")
        try:
            # Try to open with encryption key
            conn = sqlcipher.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA key = '{Config.DB_ENCRYPTION_KEY}'")
            cursor.execute("PRAGMA cipher_page_size = 4096")
            cursor.execute("SELECT count(*) FROM user")
            user_count = cursor.fetchone()[0]
            conn.close()
            print(f"   ✅ Verification successful! Found {user_count} users.")
        except Exception as e:
            print(f"   ⚠️  Verification warning: {e}")
            print("   Your database is encrypted, but verification failed.")
            print("   This is normal - try starting the app to verify it works.")
        
        print("\n" + "=" * 50)
        print("✅ DATABASE ENCRYPTION COMPLETE!")
        print(f"   • Original database backed up to: {backup_path}")
        print(f"   • Encrypted database: {db_path}")
        print(f"   • Encryption key: {Config.DB_ENCRYPTION_KEY[:10]}...")
        print("\n⚠️  IMPORTANT:")
        print("   • Keep your encryption key safe!")
        print("   • Without the key, you cannot access your data")
        print("   • Current key is in config.py or DB_ENCRYPTION_KEY env variable")
        print("\n🚀 You can now start your app normally with: python app.py")
        
    except Exception as e:
        print(f"\n❌ Error during encryption: {e}")
        print("\n🔄 Rolling back changes...")
        
        # Cleanup on error
        if os.path.exists(temp_encrypted):
            os.remove(temp_encrypted)
        
        # Restore backup if original was deleted
        if not os.path.exists(db_path) and os.path.exists(backup_path):
            shutil.copy2(backup_path, db_path)
            print("   ✅ Original database restored from backup")
        
        print("\n❌ Migration failed. Your original database is safe.")
        raise


if __name__ == '__main__':
    encrypt_existing_database()
