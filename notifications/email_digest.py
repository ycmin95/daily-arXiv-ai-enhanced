#!/usr/bin/env python3
"""
Email Digest Notification Script
Filters papers by keywords and sends daily digest via email.
Supports multiple recipients with personalized keyword filters.
"""

import os
import json
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime


def parse_keywords(keyword_string: str) -> List[str]:
    """
    Parse keyword string, supporting semicolon and comma delimiters.
    Examples:
        'gesture; sign language' -> ['gesture', 'sign language']
        'hallucination, risk' -> ['hallucination', 'risk']
    """
    if not keyword_string:
        return []
    
    # Try semicolon first (higher priority)
    if ';' in keyword_string:
        keywords = [k.strip() for k in keyword_string.split(';')]
    else:
        # Fallback to comma
        keywords = [k.strip() for k in keyword_string.split(',')]
    
    return [k for k in keywords if k]


def filter_papers_by_keywords(data: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Filter papers that match any of the specified keywords.
    Supports both single words and multi-word phrases (e.g., "sign language").
    Searches in: title, summary, and AI-generated fields.
    """
    if not keywords:
        return []
    
    filtered_papers = []
    # Normalize keywords: preserve phrases, convert to lowercase
    keyword_lower = [k.lower().strip() for k in keywords if k.strip()]
    
    for paper in data:
        # Search text includes title, summary, and AI fields
        search_text = " ".join([
            paper.get("title", ""),
            paper.get("summary", ""),
            paper.get("AI", {}).get("tldr", ""),
            paper.get("AI", {}).get("motivation", ""),
            paper.get("AI", {}).get("method", ""),
        ]).lower()
        
        # Check if any keyword (phrase or word) matches in the search text
        # Using 'in' operator handles both single words and phrases correctly
        if any(keyword in search_text for keyword in keyword_lower):
            filtered_papers.append(paper)
    
    return filtered_papers


def format_paper_html(paper: Dict, index: int) -> str:
    """Format a single paper as HTML for email."""
    title = paper.get("title", "Untitled")
    authors = ", ".join(paper.get("authors", []))
    arxiv_id = paper.get("id", "")
    abs_url = paper.get("abs", f"https://arxiv.org/abs/{arxiv_id}")
    pdf_url = paper.get("pdf", f"https://arxiv.org/pdf/{arxiv_id}")
    
    ai_data = paper.get("AI", {})
    tldr = ai_data.get("tldr", "N/A")
    motivation = ai_data.get("motivation", "N/A")
    method = ai_data.get("method", "N/A")
    result = ai_data.get("result", "N/A")
    conclusion = ai_data.get("conclusion", "N/A")
    
    categories = ", ".join(paper.get("categories", []))
    
    return f"""
    <div style="margin-bottom: 30px; padding: 15px; border-left: 4px solid #a42c25; background-color: #f9f9f9;">
        <h3 style="margin-top: 0; color: #a42c25;">
            {index}. {title}
        </h3>
        <p style="margin: 5px 0; color: #666;">
            <strong>Authors:</strong> {authors}
        </p>
        <p style="margin: 5px 0; color: #666;">
            <strong>Categories:</strong> {categories}
        </p>
        <p style="margin: 5px 0; color: #666;">
            <strong>arXiv ID:</strong> {arxiv_id}
        </p>
        <div style="margin: 10px 0;">
            <a href="{abs_url}" style="margin-right: 10px; color: #a42c25; text-decoration: none;">📄 Abstract</a>
            <a href="{pdf_url}" style="color: #a42c25; text-decoration: none;">📥 PDF</a>
        </div>
        
        <div style="margin-top: 15px;">
            <h4 style="color: #333; margin-bottom: 5px;">TLDR</h4>
            <p style="margin: 0; color: #555;">{tldr}</p>
        </div>
        
        <div style="margin-top: 10px;">
            <h4 style="color: #333; margin-bottom: 5px;">Motivation</h4>
            <p style="margin: 0; color: #555;">{motivation}</p>
        </div>
        
        <div style="margin-top: 10px;">
            <h4 style="color: #333; margin-bottom: 5px;">Method</h4>
            <p style="margin: 0; color: #555;">{method}</p>
        </div>
        
        <div style="margin-top: 10px;">
            <h4 style="color: #333; margin-bottom: 5px;">Result</h4>
            <p style="margin: 0; color: #555;">{result}</p>
        </div>
        
        <div style="margin-top: 10px;">
            <h4 style="color: #333; margin-bottom: 5px;">Conclusion</h4>
            <p style="margin: 0; color: #555;">{conclusion}</p>
        </div>
    </div>
    """


def format_email_html(papers: List[Dict], date: str, keywords: List[str], recipient_email: str = "") -> str:
    """Format the complete email HTML."""
    keyword_str = ", ".join(keywords)
    paper_count = len(papers)
    
    papers_html = "\n".join([
        format_paper_html(paper, i + 1) 
        for i, paper in enumerate(papers)
    ])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #a42c25; color: white; padding: 20px; border-radius: 5px; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">📚 Daily arXiv Digest</h1>
                <p style="margin: 10px 0 0 0;">Your Personalized Paper Feed - {date}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <p><strong>Keywords:</strong> {keyword_str}</p>
                <p><strong>Papers Found:</strong> {paper_count}</p>
            </div>
            
            {papers_html if papers else "<p>No papers found matching your keywords today.</p>"}
            
            <div class="footer">
                <p>Generated by daily-arXiv-ai-enhanced</p>
                <p>This is an automated email digest. You can manage your email preferences in the GitHub Actions workflow.</p>
            </div>
        </div>
    </body>
    </html>
    """


def send_email_via_smtp(
    to_email: str,
    subject: str,
    html_content: str,
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    from_email: str = None
):
    """Send email via SMTP (Gmail, Outlook, custom SMTP)."""
    if from_email is None:
        from_email = smtp_user
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    # Create plain text version (fallback)
    text_content = "Please view this email in an HTML-capable email client."
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    server = None
    try:
        print(f"Connecting to SMTP server: {smtp_server}:{smtp_port}...", file=sys.stderr)
        
        # Port 465 uses SSL, port 587 uses STARTTLS
        if smtp_port == 465:
            # Use SSL connection for port 465
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
            print("Using SSL connection (port 465)", file=sys.stderr)
        else:
            # Use STARTTLS for port 587 and others
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            print("Connected, starting TLS...", file=sys.stderr)
            server.starttls()
            print("TLS started successfully", file=sys.stderr)
        
        # Set debug level for troubleshooting (uncomment to see SMTP conversation)
        # server.set_debuglevel(1)
        
        print(f"Logging in as {smtp_user}...", file=sys.stderr)
        server.login(smtp_user, smtp_password)
        print("Login successful", file=sys.stderr)
        
        print(f"Sending email to {to_email}...", file=sys.stderr)
        server.send_message(msg)
        print(f"✅ Email sent successfully to {to_email}", file=sys.stderr)
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}", file=sys.stderr)
        print("Please verify your SMTP_USER and SMTP_PASSWORD are correct.", file=sys.stderr)
        print("For Gmail, make sure you're using an App Password (not your regular password).", file=sys.stderr)
        return False
    except smtplib.SMTPConnectError as e:
        print(f"SMTP Connection Error: Could not connect to {smtp_server}:{smtp_port}", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        print("Please verify SMTP_SERVER and SMTP_PORT are correct.", file=sys.stderr)
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"SMTP Server Disconnected: {e}", file=sys.stderr)
        print("The server closed the connection unexpectedly.", file=sys.stderr)
        print("This might be due to:", file=sys.stderr)
        print("  - Incorrect SMTP port (try 587 for TLS or 465 for SSL)", file=sys.stderr)
        print("  - Authentication failure", file=sys.stderr)
        print("  - Server blocking the connection", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Failed to send email: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False
    finally:
        # Ensure connection is closed
        if server:
            try:
                server.quit()
            except:
                pass


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Send daily arXiv paper digest via email to multiple recipients with personalized keywords"
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to AI-enhanced JSONL file"
    )
    parser.add_argument(
        "--recipients-config",
        type=str,
        help='JSON string or file path with recipient configurations. '
             'Format: [{"email": "user@example.com", "keywords": "keyword1; keyword2"}]'
    )
    parser.add_argument(
        "--keywords",
        type=str,
        nargs="+",
        default=["sign language"],
        help="[Legacy] Keywords to filter papers. Use --recipients-config for multi-user support."
    )
    parser.add_argument(
        "--to-email",
        type=str,
        help="[Legacy] Recipient email address (overrides EMAIL_RECIPIENT env var)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date string for email (default: today)"
    )
    return parser.parse_args()


def load_recipients_config(args) -> List[Dict]:
    """
    Load recipient configurations from various sources.
    Returns list of dicts with 'email' and 'keywords' keys.
    """
    # Priority 1: --recipients-config argument
    if args.recipients_config:
        config_str = args.recipients_config
        
        # Check if it's a file path
        if os.path.isfile(config_str):
            print(f"Loading recipients config from file: {config_str}", file=sys.stderr)
            with open(config_str, 'r') as f:
                config_data = json.load(f)
        else:
            # Try to parse as JSON string
            print("Parsing recipients config from JSON string", file=sys.stderr)
            config_data = json.loads(config_str)
        
        # Validate and normalize config
        recipients = []
        for item in config_data:
            if 'email' not in item:
                print(f"Warning: Skipping config item without email: {item}", file=sys.stderr)
                continue
            
            # Parse keywords (support string or list)
            if isinstance(item.get('keywords'), str):
                keywords = parse_keywords(item['keywords'])
            elif isinstance(item.get('keywords'), list):
                keywords = item['keywords']
            else:
                keywords = []
            
            recipients.append({
                'email': item['email'],
                'keywords': keywords
            })
        
        print(f"Loaded {len(recipients)} recipient configurations", file=sys.stderr)
        return recipients
    
    # Priority 2: EMAIL_RECIPIENTS_CONFIG environment variable
    env_config = os.environ.get("EMAIL_RECIPIENTS_CONFIG")
    if env_config:
        print("Loading recipients config from EMAIL_RECIPIENTS_CONFIG env var", file=sys.stderr)
        try:
            config_data = json.loads(env_config)
            recipients = []
            for item in config_data:
                if 'email' not in item:
                    continue
                
                if isinstance(item.get('keywords'), str):
                    keywords = parse_keywords(item['keywords'])
                elif isinstance(item.get('keywords'), list):
                    keywords = item['keywords']
                else:
                    keywords = []
                
                recipients.append({
                    'email': item['email'],
                    'keywords': keywords
                })
            
            print(f"Loaded {len(recipients)} recipient configurations from env", file=sys.stderr)
            return recipients
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse EMAIL_RECIPIENTS_CONFIG: {e}", file=sys.stderr)
    
    # Priority 3: Legacy single recipient mode
    email_recipient = args.to_email or os.environ.get("EMAIL_RECIPIENT")
    if email_recipient:
        print("Using legacy single recipient mode", file=sys.stderr)
        keywords = [k.lower() for k in args.keywords]
        return [{
            'email': email_recipient,
            'keywords': keywords
        }]
    
    return []


def main():
    """Main function."""
    args = parse_args()
    
    # Get SMTP configuration from environment variables
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.163.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "465"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    email_from = os.environ.get("EMAIL_FROM", smtp_user)
    
    # Check required SMTP configuration
    if not smtp_user or not smtp_password:
        print("ERROR: SMTP_USER and SMTP_PASSWORD must be set", file=sys.stderr)
        sys.exit(1)
    
    # Load recipient configurations
    recipients = load_recipients_config(args)
    
    if not recipients:
        print("ERROR: No recipients configured. Use --recipients-config or EMAIL_RECIPIENTS_CONFIG", file=sys.stderr)
        print("For legacy mode, use --to-email or EMAIL_RECIPIENT", file=sys.stderr)
        sys.exit(1)
    
    # Get date
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    
    # Load paper data once
    print(f"Loading papers from {args.data}...", file=sys.stderr)
    papers = []
    with open(args.data, "r") as f:
        for line in f:
            papers.append(json.loads(line))
    
    print(f"Loaded {len(papers)} papers total", file=sys.stderr)
    print(f"Processing {len(recipients)} recipient(s)...", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # Send personalized emails to each recipient
    success_count = 0
    fail_count = 0
    
    for idx, recipient in enumerate(recipients, 1):
        recipient_email = recipient['email']
        keywords = recipient['keywords']
        
        print(f"\n[{idx}/{len(recipients)}] Processing: {recipient_email}", file=sys.stderr)
        print(f"  Keywords: {', '.join(keywords)}", file=sys.stderr)
        
        # Filter papers by this recipient's keywords
        filtered_papers = filter_papers_by_keywords(papers, keywords)
        print(f"  Found {len(filtered_papers)} matching papers", file=sys.stderr)
        
        # Format email with personalized content
        subject = f"Daily arXiv Digest: {len(filtered_papers)} Papers ({date_str})"
        html_content = format_email_html(filtered_papers, date_str, keywords, recipient_email)
        
        # Send email
        success = send_email_via_smtp(
            to_email=recipient_email,
            subject=subject,
            html_content=html_content,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            from_email=email_from
        )
        
        if success:
            success_count += 1
            print(f"  ✅ Success: Sent digest with {len(filtered_papers)} papers", file=sys.stderr)
        else:
            fail_count += 1
            print(f"  ❌ Failed: Could not send email", file=sys.stderr)
    
    # Summary
    print("=" * 60, file=sys.stderr)
    print(f"\n📊 Summary:", file=sys.stderr)
    print(f"  Total recipients: {len(recipients)}", file=sys.stderr)
    print(f"  Successful: {success_count}", file=sys.stderr)
    print(f"  Failed: {fail_count}", file=sys.stderr)
    
    if fail_count == 0:
        print("\n✅ All emails sent successfully!", file=sys.stderr)
        sys.exit(0)
    elif success_count > 0:
        print(f"\n⚠️  Partial success: {fail_count} email(s) failed", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n❌ All emails failed!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

