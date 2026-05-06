import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dotenv import load_dotenv

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM", "rezerwacje@skyport.pl"),
    MAIL_PORT = int(os.getenv("MAIL_PORT", 2525)),
    MAIL_SERVER = os.getenv("MAIL_SERVER", "sandbox.smtp.mailtrap.io"),
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def wyslij_potwierdzenie_rezerwacji(email_odbiorcy: str, imie: str, pnr: str, numer_lotu: str, skad: str, dokad: str, data: str, kwota: float):

    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #1a365d;">✈️ SkyPort - Potwierdzenie Rezerwacji</h2>
        <p>Witaj <strong>{imie}</strong>,</p>
        <p>Dziękujemy za dokonanie płatności. Twoja rezerwacja została potwierdzona!</p>
        
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 6px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #2d3748;">Szczegóły Twojego lotu:</h3>
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin-bottom: 10px;">🎫 <strong>Numer Rezerwacji (PNR):</strong> <span style="font-size: 18px; color: #ecc94b; font-weight: bold;">{pnr}</span></li>
                <li style="margin-bottom: 10px;">🛫 <strong>Lot:</strong> {numer_lotu}</li>
                <li style="margin-bottom: 10px;">📍 <strong>Trasa:</strong> {skad} ➔ {dokad}</li>
                <li style="margin-bottom: 10px;">📅 <strong>Data wylotu:</strong> {data}</li>
            </ul>
        </div>
        
        <p>Prosimy o przybycie na lotnisko co najmniej 2 godziny przed planowanym odlotem w celu odprawy.</p>
        <p>Życzymy udanej podróży!<br><em>Zespół SkyPort</em></p>
    </div>
    """


    message = MessageSchema(
        subject=f"Potwierdzenie płatności za lot {numer_lotu} (PNR: {pnr})",
        recipients=[email_odbiorcy],
        body=html_content,
        subtype=MessageType.html
    )


    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"E-mail z potwierdzeniem wysłany do {email_odbiorcy} (PNR: {pnr})")