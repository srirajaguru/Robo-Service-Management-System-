import os
import json
import urllib.request
import urllib.parse
import logging
from django.conf import settings
from notification.models import Notification

logger = logging.getLogger(__name__)


def clean_phone_number(phone: str) -> str:
    """Format phone number for WhatsApp with country code."""
    if not phone:
        return ""
    digits = "".join(ch for ch in str(phone) if ch.isdigit())
    if len(digits) == 10:
        return f"91{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return digits
    return digits


def inward_message(service) -> str:
    """Generate message text for Service Inward."""
    customer_name = service.customer.name if service.customer else "Valued Customer"
    service_id_str = str(service)
    device_info = f"{service.device_type} ({service.brand} {service.model})".strip()
    exp_date = service.expected_completion_date.strftime("%d-%b-%Y") if service.expected_completion_date else "To be notified"

    return (
        f"Dear {customer_name},\n\n"
        f"Your device has been received for service at ROBO DIGITAL COMPUTERS.\n\n"
        f"🔖 Service ID: {service_id_str}\n"
        f"💻 Device: {device_info}\n"
        f"⚠️ Complaint: {service.complaint}\n"
        f"📅 Expected Date: {exp_date}\n\n"
        f"We will notify you once the service diagnosis or completion is ready.\n\n"
        f"Thank you,\n"
        f"ROBO DIGITAL COMPUTERS\n"
        f"54A Govt Boys School Opposite, Trichy Road, Musiri\n"
        f"📞 8122227042 / 8122227074"
    )


def completion_message(service) -> str:
    """Generate message text for Service Completion."""
    customer_name = service.customer.name if service.customer else "Valued Customer"
    service_id_str = str(service)
    device_info = f"{service.device_type} ({service.brand} {service.model})".strip()
    total_amt = service.total_amount
    balance_amt = service.balance_amount

    return (
        f"Dear {customer_name},\n\n"
        f"✅ Your device service is now COMPLETED at ROBO DIGITAL COMPUTERS!\n\n"
        f"🔖 Service ID: {service_id_str}\n"
        f"💻 Device: {device_info}\n"
        f"💰 Total Amount: ₹{total_amt}\n"
        f"💳 Balance Due: ₹{balance_amt}\n\n"
        f"Your device is ready for collection at our shop.\n\n"
        f"Thank you for choosing us,\n"
        f"ROBO DIGITAL COMPUTERS\n"
        f"54A Govt Boys School Opposite, Trichy Road, Musiri\n"
        f"📞 8122227042 / 8122227074"
    )


def payment_message(service, payment) -> str:
    """Generate message text for Payment confirmation."""
    customer_name = service.customer.name if service.customer else "Valued Customer"
    return (
        f"Dear {customer_name},\n\n"
        f"💵 Payment of ₹{payment.amount} received for Service {service} via {payment.payment_method}.\n"
        f"Remaining Balance: ₹{service.balance_amount}\n\n"
        f"Thank you,\n"
        f"ROBO DIGITAL COMPUTERS"
    )


def generate_whatsapp_web_url(phone: str, message: str) -> str:
    """Generate direct wa.me link for manual WhatsApp sending."""
    clean_phone = clean_phone_number(phone)
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"


def send_whatsapp_notification(service, notification_type: str, message: str, staff_profile=None):
    """
    Send WhatsApp notification using WhatsApp Cloud API.
    Falls back gracefully to simulated logging if API credentials are not provided.
    Never throws unhandled exceptions that interrupt user actions.
    """
    customer = getattr(service, "customer", None)
    phone = getattr(customer, "phone_number", "")
    clean_phone = clean_phone_number(phone)

    token = os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
    api_url = os.getenv("WHATSAPP_API_URL", "https://graph.facebook.com/v18.0").rstrip("/")

    status = "Pending"
    response_log = ""

    if not clean_phone:
        status = "Failed"
        response_log = "Error: Customer phone number is missing or invalid."
    elif token and phone_number_id:
        # Live WhatsApp Cloud API call
        endpoint = f"{api_url}/{phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_phone,
            "type": "text",
            "text": {"preview_url": False, "body": message}
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                resp_data = response.read().decode("utf-8")
                status = "Sent"
                response_log = f"Status {response.status}: {resp_data}"
        except Exception as exc:
            status = "Failed"
            response_log = f"API Error: {str(exc)}"
            logger.error("WhatsApp API request failed: %s", exc)
    else:
        # Development / Simulation mode
        status = "Simulated"
        response_log = "Simulated: WhatsApp credentials not set in .env. Message recorded for review."

    # Record notification in database
    notification = Notification.objects.create(
        service=service,
        customer=customer,
        notification_type=notification_type,
        phone_number=clean_phone or phone,
        message=message,
        status=status,
        response_log=response_log,
        sent_by=staff_profile
    )
    return notification
