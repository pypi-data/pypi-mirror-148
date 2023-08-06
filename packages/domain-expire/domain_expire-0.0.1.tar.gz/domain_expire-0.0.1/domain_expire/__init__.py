import ssl
import OpenSSL
import datetime
from pytz import timezone

SRC_TZ = 'UTC'
DST_TZ = 'Asia/Shanghai'


def load_ssl_date(dt_string, pattern='%Y%m%d%H%M%SZ'):
    """ convert ssl date from string to datetime obj """
    src_tz = timezone(SRC_TZ)
    dst_tz = timezone(DST_TZ)
    dt = src_tz.localize(datetime.datetime.strptime(dt_string, pattern))
    return dt.astimezone(tz=dst_tz)


def get_ssl_expiry_date(host, port=443):
    """ get notAfter data from server cert """
    cert = ssl.get_server_certificate((host, port))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert.encode())
    return x509.get_notAfter().decode()


def check_expire(domain, days=10):
    date_str = get_ssl_expiry_date(domain)
    dt = load_ssl_date(date_str)
    print(dt)
    if (dt - datetime.datetime.now(tz=timezone(DST_TZ))).days < days:
        return True
    return False


if __name__ == "__main__":
    check_expire('api.zhiyujiejing.com', days=5)
