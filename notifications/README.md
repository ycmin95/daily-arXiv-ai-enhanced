# 📧 Email Digest Notifications

This module sends daily email digests of arXiv papers filtered by keywords (e.g., "sign language").

## ✨ Features

- **Keyword Filtering**: Automatically filters papers matching your keywords
- **AI-Enhanced Summaries**: Includes all AI-generated summaries (TLDR, motivation, method, result, conclusion)
- **HTML Email**: Beautiful, formatted HTML emails with paper details
- **Flexible Configuration**: Works with Gmail, Outlook, or any SMTP server
- **Optional**: Fails gracefully if not configured

## 🔧 Setup

### Step 1: Configure GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

#### Required Secrets:
```yaml
SMTP_USER:          # Your email address (e.g., your.email@gmail.com)
SMTP_PASSWORD:      # Your email password or app-specific password
EMAIL_RECIPIENT:    # Where to send the digest (can be same as SMTP_USER)
```

#### Optional Secrets:
```yaml
SMTP_SERVER:        # SMTP server (default: smtp.gmail.com)
SMTP_PORT:          # SMTP port (default: 587)
EMAIL_FROM:         # From address (default: SMTP_USER)
```

### Step 2: Configure Keywords (Optional)

By default, the script searches for papers containing "sign language". To customize keywords:

1. **Option A**: Set via GitHub Variables (repository-level)
   - Go to Settings → Secrets and variables → Actions → Variables
   - Add variable: `EMAIL_KEYWORDS` = `sign language gesture recognition ASL`

2. **Option B**: Modify the workflow file (`.github/workflows/run.yml`)
   - Find the line: `EMAIL_KEYWORDS="${EMAIL_KEYWORDS:-sign language signing gesture recognition}"`
   - Change the default keywords as needed

### Step 3: Enable in Workflow

The email step is already added to the workflow. It will:
- ✅ Run automatically after AI enhancement
- ✅ Only send if new papers are found
- ✅ Skip gracefully if secrets are not configured

## 📧 Email Provider Setup

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Create a new app password for "Mail"
   - Use this password as `SMTP_PASSWORD`

**Configuration:**
```yaml
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SMTP_USER: your.email@gmail.com
SMTP_PASSWORD: [app-specific-password]
EMAIL_RECIPIENT: your.email@gmail.com
```

### Outlook/Office 365 Setup

1. Use your Microsoft account email
2. You may need to enable "Less secure app access" or use an app password

**Configuration:**
```yaml
SMTP_SERVER: smtp-mail.outlook.com
SMTP_PORT: 587
SMTP_USER: your.email@outlook.com
SMTP_PASSWORD: [your-password-or-app-password]
EMAIL_RECIPIENT: your.email@outlook.com
```

### Custom SMTP Server

For other providers (SendGrid, Mailgun, etc.):

```yaml
SMTP_SERVER: smtp.example.com
SMTP_PORT: 587  # or 465 for SSL
SMTP_USER: your-username
SMTP_PASSWORD: your-password
EMAIL_RECIPIENT: recipient@example.com
```

## 🎯 Customization

### Filtering Multiple Keywords

The script searches for papers matching **any** of the specified keywords:

```bash
# Single keyword
--keywords "sign language"

# Multiple keywords (OR logic)
--keywords "sign language" "ASL" "gesture recognition" "SLR"
```

### Custom Email Template

Edit `email_digest.py` → `format_email_html()` function to customize the email appearance.

### Testing Locally

```bash
# Activate virtual environment
source .venv/bin/activate

# Run email digest script
cd notifications
python email_digest.py \
  --data ../data/2024-01-15_AI_enhanced_Chinese.jsonl \
  --keywords "sign language" "ASL" \
  --to-email your.email@example.com \
  --date "2024-01-15"

# Set environment variables
export SMTP_USER="your.email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export EMAIL_RECIPIENT="your.email@gmail.com"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

## 📊 Email Content

Each email includes:

- **Header**: Date and paper count
- **Filtered Papers**: All papers matching keywords
- **For Each Paper**:
  - Title and authors
  - arXiv ID and categories
  - Links to abstract and PDF
  - **AI Summaries**:
    - TLDR (brief summary)
    - Motivation
    - Method
    - Result
    - Conclusion

## 🔍 How Filtering Works

The script searches for keywords in:
- Paper title
- Paper abstract/summary
- AI-generated TLDR
- AI-generated motivation
- AI-generated method

**Matching**: Case-insensitive, matches if any keyword appears in any of these fields.

## ⚠️ Troubleshooting

### Email Not Sending

1. **Check Secrets**: Verify all required secrets are set in GitHub
2. **Check Workflow Logs**: View the "Send Email Digest" step in Actions
3. **Test SMTP Credentials**: Try connecting manually with the credentials
4. **Check Firewall**: Ensure GitHub Actions can access SMTP servers

### Gmail "Less Secure Apps" Error

- Use an **App-Specific Password** instead of your regular password
- Enable 2-Factor Authentication first
- Generate password at: https://myaccount.google.com/apppasswords

### No Papers Found

- Check if papers were actually published that day
- Verify keywords match actual paper content
- Try broader keywords or check workflow logs for paper counts

## 🔒 Security Notes

- Never commit secrets to the repository
- Use GitHub Secrets for all sensitive information
- Consider using app-specific passwords instead of main passwords
- The email script only reads data files, never modifies them

## 📝 Example Email

```
Subject: Daily arXiv Digest: 3 Sign Language Papers (2024-01-15)

📚 Daily arXiv Digest
Sign Language Papers - 2024-01-15

Keywords: sign language
Papers Found: 3

[Paper 1: Title, Authors, Summary...]
[Paper 2: ...]
[Paper 3: ...]
```

## 🚀 Future Enhancements

Possible improvements:
- Support for multiple recipients
- Different email templates (plain text, Markdown)
- Configurable email frequency
- Email digests for different keyword sets
- Attachment of paper PDFs
- Integration with email services (SendGrid, Mailgun API)

---

For questions or issues, please open an issue on GitHub.

