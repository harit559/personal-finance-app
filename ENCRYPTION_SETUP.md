# 🔐 Database Encryption Setup Guide

Your personal finance app now supports **AES-256 encryption** using SQLCipher to protect your financial data.

## What This Protects

✅ **Complete database encryption** - The entire `finance.db` file is encrypted  
✅ **Military-grade security** - 256-bit AES encryption (same used by banks)  
✅ **Transparent operation** - After setup, the app works normally  
✅ **Protection at rest** - Even if someone gets your `.db` file, they can't read it without the encryption key

## Setup Instructions

### Step 1: Install SQLCipher

First, install the encryption library:

```bash
pip install -r requirements.txt
```

This will install `sqlcipher3` which provides the encryption functionality.

### Step 2: Run the Migration Script

If you have an existing database with data, run this script to encrypt it:

```bash
python encrypt_database.py
```

This script will:
- ✅ Create a backup of your current database
- ✅ Create a new encrypted database
- ✅ Copy all your data to the encrypted version
- ✅ Replace the old database with the encrypted one

**Note:** The backup file will be named `finance_backup_YYYYMMDD_HHMMSS.db` - keep it safe!

### Step 3: Start Your App

```bash
python app.py
```

Or use your startup script:

```bash
./start.sh
```

That's it! Your database is now encrypted.

## 🔑 About Your Encryption Key

### Where is it?

Your encryption key is stored in `config.py`:

```python
DB_ENCRYPTION_KEY = 'my-secure-encryption-key-2026'
```

### Changing the Key (Recommended!)

For better security, you should change this to your own unique key:

1. **Option 1: Edit config.py directly**
   - Open `config.py`
   - Change the `DB_ENCRYPTION_KEY` value to something unique
   - Make it long and random!

2. **Option 2: Use environment variable (More Secure)**
   - Create a `.env` file (copy from `.env.example`)
   - Set your key: `DB_ENCRYPTION_KEY=your-super-secret-key-here`
   - The app will use this instead of the default in `config.py`

### ⚠️ IMPORTANT WARNINGS

1. **Never lose your encryption key!**
   - Without the key, your data is **permanently unrecoverable**
   - Write it down and store it somewhere safe
   - Consider keeping a copy in a password manager

2. **Don't commit your key to Git**
   - The `.gitignore` file prevents `.env` from being committed
   - Never push your actual encryption key to GitHub or any public repo

3. **If you change the key**
   - You'll need to re-encrypt your database with the new key
   - Or decrypt with old key and re-encrypt with new key

## Testing Encryption

To verify your database is encrypted:

1. Close your app
2. Try opening `finance.db` with a regular SQLite browser (like DB Browser for SQLite)
3. You should see an error like "file is encrypted or is not a database"
4. This means it's working! ✅

## Backup Strategy

Since your database is now encrypted:

1. **Regular backups**: Copy `finance.db` regularly
2. **Keep the encryption key separate**: Don't store it with the backup
3. **Test your backups**: Occasionally verify you can restore from backup

## Security Best Practices

1. ✅ Use a strong, unique encryption key
2. ✅ Enable FileVault on your Mac for full disk encryption
3. ✅ Keep your encryption key in a password manager
4. ✅ Make regular backups
5. ✅ Never commit your `.env` file or encryption key to version control
6. ✅ Use a different encryption key than the default in this guide

## How It Works

- **SQLCipher** encrypts every page of the database file
- Uses **AES-256** encryption in CBC mode
- Each time the app connects to the database, it provides the encryption key
- Without the correct key, the database file looks like random data

## Troubleshooting

### "file is encrypted or is not a database"

This error when starting the app means:
- Your database is encrypted, but the key doesn't match
- Check your encryption key in `config.py` or `.env`

### "no such table: user"

This usually means:
- The encryption key is wrong, OR
- The database needs to be created

Try deleting `finance.db` and running `python app.py` again.

### Need to start over?

If something goes wrong:
1. Stop the app
2. Delete `finance.db`
3. Restore from your backup: `cp finance_backup_*.db finance.db`
4. Or run the migration script again

---

🎉 **Congratulations!** Your financial data is now protected with military-grade encryption!
