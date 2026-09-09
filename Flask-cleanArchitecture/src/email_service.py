import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_reset_otp(to_email: str, otp: str) -> bool:

    host = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com"
    )

    port = int(
        os.getenv("SMTP_PORT", "587")
    )

    username = os.getenv(
        "SMTP_USERNAME"
    )

    password = os.getenv(
        "SMTP_PASSWORD"
    )

    if not username or not password:

        print(
            "EMAIL ERROR: "
            "SMTP_USERNAME/SMTP_PASSWORD "
            "are not configured"
        )

        return False

    message = MIMEMultipart("alternative")

    message["Subject"] = (
        "FilmSpace - Password Reset Code"
    )

    message["From"] = username
    message["To"] = to_email

    html = f"""
    <div style="
        font-family:Arial,sans-serif;
        max-width:600px;
        margin:auto;
        background:#fff;
        border:1px solid #eee;
        border-radius:12px;
        overflow:hidden;
    ">

      <div style="
          background:#26283b;
          padding:24px;
          text-align:center;
      ">
        <h1 style="
            margin:0;
            color:#fff;
            font-size:28px;
        ">
          Film<span style="color:#ff1584">
            Space
          </span>
        </h1>
      </div>

      <div style="padding:36px 32px">

        <h2 style="color:#26283b">
          Password Reset Request
        </h2>

        <p style="color:#6f7284;line-height:1.6">
          We received a request to reset
          your FilmSpace password.
        </p>

        <p style="color:#6f7284;line-height:1.6">
          Use the verification code below:
        </p>

        <div style="
            text-align:center;
            margin:30px 0;
        ">

          <span style="
              display:inline-block;
              background:#fff1f8;
              border:1px dashed #ff1584;
              border-radius:10px;
              padding:16px 28px;
              font-size:30px;
              font-weight:700;
              letter-spacing:8px;
              color:#26283b;
          ">
            {otp}
          </span>

        </div>

        <p style="color:#6f7284">
          This code will expire in
          <strong>5 minutes</strong>.
        </p>

        <p style="color:#6f7284">
          If you did not request this,
          you can ignore this email.
        </p>

      </div>

    </div>
    """

    text = (
        f"Your FilmSpace password reset "
        f"code is: {otp}. "
        f"This code expires in 5 minutes."
    )

    message.attach(
        MIMEText(
            text,
            "plain",
            "utf-8"
        )
    )

    message.attach(
        MIMEText(
            html,
            "html",
            "utf-8"
        )
    )

    print("SMTP HOST:", host)
    print("SMTP PORT:", port)
    print("SMTP USER:", username)
    print("SMTP PASSWORD LENGTH:", len(password))

    try:

        with smtplib.SMTP(
            host,
            port,
            timeout=15
        ) as server:

            server.starttls()

            server.login(
                username,
                password
            )

            server.sendmail(
                username,
                [to_email],
                message.as_string()
            )

        return True

    except Exception as exc:

        print(
            "EMAIL ERROR:",
            repr(exc)
        )

        return False