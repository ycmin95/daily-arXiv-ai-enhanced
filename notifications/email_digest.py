#!/usr/bin/env python3
"""
Email Digest Notification Script
Filters papers by keywords and sends daily digest via email.
"""

import os
import json
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime


def filter_papers_by_keywords(data: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Filter papers that match any of the specified keywords.
    Searches in: title, summary, and AI-generated fields.
    """
    if not keywords:
        return []
    
    filtered_papers = []
    keyword_lower = [k.lower() for k in keywords]
    
    for paper in data:
        # Search text includes title, summary, and AI fields
        search_text = " ".join([
            paper.get("title", ""),
            paper.get("summary", ""),
            paper.get("AI", {}).get("tldr", ""),
            paper.get("AI", {}).get("motivation", ""),
            paper.get("AI", {}).get("method", ""),
        ]).lower()
        
        # Check if any keyword matches
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


def format_email_html(papers: List[Dict], date: str, keywords: List[str]) -> str:
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
                <p style="margin: 10px 0 0 0;">Sign Language Papers - {date}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <p><strong>Keywords:</strong> {keyword_str}</p>
                <p><strong>Papers Found:</strong> {paper_count}</p>
            </div>
            
            {papers_html if papers else "<p>No papers found matching the keywords today.</p>"}
            
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
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"Email sent successfully to {to_email}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Send daily arXiv paper digest via email"
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to AI-enhanced JSONL file"
    )
    parser.add_argument(
        "--keywords",
        type=str,
        nargs="+",
        default=["sign language"],
        help="Keywords to filter papers (default: 'sign language')"
    )
    parser.add_argument(
        "--to-email",
        type=str,
        help="Recipient email address (overrides EMAIL_RECIPIENT env var)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date string for email (default: today)"
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    # Get configuration from environment variables
    email_recipient = args.to_email or os.environ.get("EMAIL_RECIPIENT")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    email_from = os.environ.get("EMAIL_FROM", smtp_user)
    
    # Check required configuration
    if not email_recipient:
        print("ERROR: EMAIL_RECIPIENT not set or --to-email not provided", file=sys.stderr)
        sys.exit(1)
    
    if not smtp_user or not smtp_password:
        print("ERROR: SMTP_USER and SMTP_PASSWORD must be set", file=sys.stderr)
        sys.exit(1)
    
    # Get date
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    
    # Load paper data
    print(f"Loading papers from {args.data}...", file=sys.stderr)
    papers = []
    with open(args.data, "r") as f:
        for line in f:
            papers.append(json.loads(line))
    
    print(f"Loaded {len(papers)} papers", file=sys.stderr)
    
    # Filter papers by keywords
    keywords = [k.lower() for k in args.keywords]
    filtered_papers = filter_papers_by_keywords(papers, keywords)
    
    print(f"Found {len(filtered_papers)} papers matching keywords: {', '.join(keywords)}", file=sys.stderr)
    
    # Format email
    subject = f"Daily arXiv Digest: {len(filtered_papers)} Sign Language Papers ({date_str})"
    html_content = format_email_html(filtered_papers, date_str, args.keywords)
    
    # Send email
    success = send_email_via_smtp(
        to_email=email_recipient,
        subject=subject,
        html_content=html_content,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        from_email=email_from
    )
    
    if success:
        print(f"Successfully sent digest with {len(filtered_papers)} papers", file=sys.stderr)
        sys.exit(0)
    else:
        print("Failed to send email", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

