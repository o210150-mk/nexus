# myapp/tasks.py (or utils.py)

import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_in_thread(msg):
    """Function to send the message in a new thread."""
    try:
        msg.send(fail_silently=False)
    except Exception as e:
        # Log the error here instead of crashing the main thread
        print(f"Error sending email asynchronously: {e}") 

def send_otp_email_async(gmail, otp):
    """
    Renders the content and initiates a non-blocking thread for sending.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [gmail]

    # 1. Render the HTML content locally (This is fast)
    html_content = render_to_string('mail.html', {'username': gmail, 'otp': otp})
    text_content = strip_tags(html_content)
    
    # 2. Create the message object
    msg = EmailMultiAlternatives('Password Reset', text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    
    # 3. Start a new thread to send the email (Non-blocking)
    thread = threading.Thread(target=send_email_in_thread, args=(msg,))
    thread.start()