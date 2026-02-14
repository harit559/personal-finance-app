# 📧 Email Setup Guide - Gmail SMTP

**Quick guide to set up password reset emails using Gmail**

---

## 🎯 What You Need

- Gmail account (you probably have one!)
- 5 minutes

---

## 📋 Step-by-Step Setup

### Step 1: Enable 2-Factor Authentication

Gmail requires 2FA to use app passwords.

1. **Go to:** https://myaccount.google.com/security
2. **Find** "2-Step Verification"
3. **Click** "Get Started"
4. **Follow** the prompts to enable 2FA
5. **Verify** with your phone

**Already have 2FA?** Skip to Step 2!

---

### Step 2: Generate App Password

1. **Go to:** https://myaccount.google.com/apppasswords
   - Or Google Account → Security → 2-Step Verification → App passwords

2. **Select:**
   - App: "Mail"
   - Device: "Other (Custom name)"
   - Name: "Harit Finance"

3. **Click** "Generate"

4. **Copy** the 16-character password (looks like: `abcd efgh ijkl mnop`)

5. **Save it** somewhere safe!

---

### Step 3: Create `.env` File

1. **Go to** your project folder:
   ```bash
   cd /Users/harit/Projects/personal_finance_app
   ```

2. **Create** `.env` file (if it doesn't exist):
   ```bash
   touch .env
   ```

3. **Add** these lines to `.env`:
   ```bash
   # Email Configuration (Gmail SMTP)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your.email@gmail.com
   MAIL_PASSWORD=abcd efgh ijkl mnop
   MAIL_DEFAULT_SENDER=your.email@gmail.com
   ```

4. **Replace:**
   - `your.email@gmail.com` → Your actual Gmail address
   - `abcd efgh ijkl mnop` → The app password you copied (remove spaces!)

**Example:**
```bash
MAIL_USERNAME=harit.finance@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
MAIL_DEFAULT_SENDER=harit.finance@gmail.com
```

---

### Step 4: Test It!

1. **Restart your app:**
   ```bash
   # Stop app if running (Ctrl+C)
   poetry run python app.py
   ```

2. **Open:** http://localhost:5001

3. **Test password reset:**
   - Go to login page
   - Click "Forgot password?"
   - Enter your email
   - Check your inbox!

4. **Check email:**
   - Should arrive within 30 seconds
   - Subject: "Reset Your Password - Harit Finance"
   - Click the reset link
   - Enter new password
   - Done!

---

## ✅ Success Checklist

- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App password generated
- [ ] `.env` file created with email config
- [ ] App restarted
- [ ] Tested password reset
- [ ] Email received successfully
- [ ] Reset link works

---

## 🐛 Troubleshooting

### "Error sending email: (535, b'5.7.8 Username and Password not accepted')"

**Causes:**
1. Wrong email or password in `.env`
2. App password not generated
3. 2FA not enabled

**Fix:**
1. Check `.env` file has correct email
2. Check password has NO SPACES (use: `abcdefghijklmnop`, not `abcd efgh ijkl mnop`)
3. Make sure you're using APP PASSWORD, not your Gmail password
4. Verify 2FA is enabled
5. Generate a new app password

---

### "Error sending email: Connection refused"

**Fix:**
1. Check `MAIL_SERVER=smtp.gmail.com` (not gmail.com)
2. Check `MAIL_PORT=587`
3. Check internet connection
4. Check firewall allows SMTP (port 587)

---

### "Email not arriving"

**Check:**
1. Spam folder
2. Console for error messages
3. Gmail settings (allow less secure apps - though app password should bypass this)
4. Try sending to different email address

---

### "App Password option not available"

**Fix:**
1. Make sure 2FA is enabled first
2. Wait a few minutes after enabling 2FA
3. Try this direct link: https://security.google.com/settings/security/apppasswords
4. If still not available, your organization might block it (use different Gmail)

---

## 🔒 Security Tips

### ✅ DO:
- Use app passwords (not your real Gmail password)
- Keep `.env` file secret (already in `.gitignore`)
- Use different Gmail for the app (optional but recommended)
- Generate new app password if compromised
- Revoke old app passwords you're not using

### ❌ DON'T:
- Share your app password
- Commit `.env` file to git
- Use your personal Gmail password
- Share your `.env` file
- Post app password in screenshots/logs

---

## 📊 Email Limits

**Gmail SMTP Limits:**
- **500 emails/day** - More than enough!
- **Sending limit per hour** - ~100 emails
- **Recipients per email** - 1 (password resets only go to 1 person)

**For your app:**
- Password resets: 1 email per request
- If 10 users reset password: 10 emails
- You can do 500 password resets per day!

---

## 🔄 Using Different Email for App

**Recommended:** Create separate Gmail for your app

**Why?**
- Security: If app is compromised, personal Gmail is safe
- Organization: App emails separate from personal
- Professional: Use business-like name (e.g., `harit.finance.app@gmail.com`)
- Clean inbox: App sending logs don't clutter your personal inbox

**Steps:**
1. Create new Gmail: `harit.finance.app@gmail.com`
2. Enable 2FA on new account
3. Generate app password
4. Use new email in `.env` file

---

## 📝 `.env` File Complete Example

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///finance.db

# Email Configuration (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=harit.finance.app@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
MAIL_DEFAULT_SENDER=harit.finance.app@gmail.com
```

---

## 🎓 How It Works

1. **User forgets password** → Clicks "Forgot password?"
2. **Enters email** → Submits form
3. **Backend generates token** → Secure random 32-character token
4. **Saves token** → Stored in database with 1-hour expiration
5. **Sends email** → Via Gmail SMTP
6. **User receives email** → With reset link
7. **Clicks link** → Goes to reset password page
8. **Enters new password** → Saved to database
9. **Token cleared** → One-time use only
10. **Success!** → User can log in with new password

**Security features:**
- ✅ Token expires in 1 hour
- ✅ Token is random and unpredictable
- ✅ Token is single-use
- ✅ Password is hashed before saving
- ✅ Old password is completely replaced

---

## 🚀 Next Steps

### For Development:
- ✅ Keep using Gmail SMTP
- ✅ Works great for testing
- ✅ 500 emails/day is plenty

### For Production (Later):
- 📧 Switch to SendGrid for professional emails
- 📖 See: `PRODUCTION_OPTIMIZATION.md` → "Migrating Email from Gmail to SendGrid"
- ⏰ Do this before deploying to Render.com

---

## ❓ FAQ

**Q: Do I need a paid Gmail account?**  
A: No! Free Gmail works perfectly.

**Q: Will this affect my personal Gmail?**  
A: No, app passwords are separate. You can revoke them anytime.

**Q: How many app passwords can I create?**  
A: Unlimited! Create one per app/device.

**Q: Can I use this on Render.com?**  
A: Yes! Add the same environment variables to Render.

**Q: What if I delete the app password?**  
A: Password reset will stop working. Just generate a new one and update `.env`.

**Q: Is this secure?**  
A: Yes! App passwords are designed for this use case.

---

## 🎉 You're Done!

Password reset is now working with Gmail SMTP!

**Test it:**
1. Go to: http://localhost:5001/auth/forgot-password
2. Enter your email
3. Check inbox
4. Click link
5. Reset password
6. Success!

---

**Need help?** Check troubleshooting section above or see `PRODUCTION_OPTIMIZATION.md` for SendGrid migration guide.
