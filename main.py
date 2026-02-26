import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def fetch_api_data(api_key):
    # This URL is an example; replace with your actual Sutherland API endpoint
    api_url = "https://api.sutherland.global/v1/threats/cves" 
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json() # Assuming the API returns a list of CVEs
    except Exception as e:
        print(f"API Error: {e}")
        return []

def send_threat_report():
    sender_email = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")
    api_key = os.environ.get("SUTHERLAND_API_KEY")

    # --- DYNAMIC DATA FETCHING ---
    cve_data = fetch_api_data(api_key)
    
    # Build the table rows dynamically
    table_rows = ""
    for item in cve_data:
        table_rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{item.get('id', 'N/A')}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{item.get('platform', 'N/A')}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{item.get('status', 'N/A')}</td>
        </tr>
        """
    # --- END DYNAMIC DATA ---

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Executive Global Cyber Threat Summary"
    msg["From"] = f"Cyber Intelligence Team <{sender_email}>"
    msg["To"] = sender_email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #1a73e8;">Executive Global Cyber Threat Summary</h2>
        <p><strong>Status:</strong> Premium Access Active</p>
        <hr>
        <h3>Critical Vulnerabilities Under Active Exploitation</h3>
        <table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">
          <tr style="background-color: #e8f0fe;">
            <th style="padding: 8px; border: 1px solid #ddd;">Identifier</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Platform</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Current Status</th>
          </tr>
          {table_rows if table_rows else "<tr><td colspan='3'>No new vulnerabilities reported.</td></tr>"}
        </table>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, sender_email, msg.as_string())
        print("Dynamic report sent!")
    except Exception as e:
        print(f"Mail Error: {e}")

if __name__ == "__main__":
    send_threat_report()
