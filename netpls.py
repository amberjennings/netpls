#!/usr/bin/env python3

#########################
# Amber Jennings ~ 2023 #
# github/amberjennings  #
#########################

import os
import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load variables from rb.cfg
def load_config():
    dir = os.path.dirname(__file__)
    cfg_file_path = os.path.join(dir, "rb.cfg")
    
    with open(cfg_file_path, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
        sender = cfg["sender"]
        recipient = cfg["recipient"]
        mailserver = cfg["mailserver"]
        email = cfg["email"]
        mailpass = cfg["mailpass"]
        port = cfg["port"]
        ssid = cfg["ssid"]
        wifi_password = cfg["wifi_password"]
        log_file = cfg["log_file"]

    return sender, recipient, mailserver, email, mailpass, port, ssid, wifi_password, log_file

# Send 3 pings to Google's DNS server, to check for connectivity
def check_connectivity():
    return os.system("ping -c 3 8.8.8.8 > /dev/null 2>&1") == 0

# Connect to wifi network
def connect_to_network(ssid, password):
    os.system(f"nmcli device wifi connect \"{ssid}\" password \"{password}\"")

# Send email when the network is reconnected
def send_email(mailserver, email, password, port):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Network was restarted"

    body = "SSIA"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(mailserver, port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, recipient, message.as_string())

        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Log output with timestamps
def log(message, log_file):
    timestamp = datetime.now().strftime("[%m-%d-%Y %T]")

    with open(log_file, "a") as log_file:
        if message and not message.startswith("---"): # Check for separator line
            log_file.write(f"{timestamp} {message}\n")
        else:
            log_file.write(f"{message}\n")

if __name__ == "__main__":
    # Import variables from load_config function
    sender, recipient, mailserver, email, mailpass, port, ssid, wifi_password, log_file = load_config()

    # Separator line
    log("---------------------", log_file)

    # If pings did not route to Google,
    if not check_connectivity():
        log(f"Error: No network connectivity. Attempting to connect to {ssid}...", log_file)
        # Try to connect
        if connect_to_network(ssid, wifi_password) != 0:
            log(f"Error: Failed to connect to {ssid}.", log_file)
            exit(1)
        else:
            log(f"Successfully connected to {ssid}.", log_file)
            # Send email
            email_sent = send_email(mailserver, email, mailpass, port)
            if email_sent:
                log("Email sent successfully!", log_file)
            else:
                log("Failed to send email.", log_file)
    else:
        log("Connectivity already available.", log_file)
