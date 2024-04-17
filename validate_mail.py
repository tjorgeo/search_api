from ipaddress import IPv4Address, IPv6Address
from validate_email import validate_email
import dataTable
import pandas as pd


def mail_validation(df):

    for index,row in df.iterrows():
        is_valid = validate_email(
            email_address=row.email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=False,
            smtp_timeout=10,
            smtp_helo_host='my.host.name',
            smtp_from_address='my@from.addr.ess',
            smtp_skip_tls=False,
            smtp_tls_context=None,
            smtp_debug=False,
            address_types=frozenset([IPv4Address, IPv6Address]))
        if not is_valid:
            df = df.drop([index])
            print("Invalid Mail Adress: ", row.email)
    return df
            

def single_mail():
    is_valid = validate_email(
        email_address="klodianaseiti7@gmai.com",
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=True,
        smtp_timeout=10,
        smtp_helo_host='my.host.name',
        smtp_from_address='my@from.addr.ess',
        smtp_skip_tls=False,
        smtp_tls_context=None,
        smtp_debug=False,
        address_types=frozenset([IPv4Address, IPv6Address]))


    print(is_valid)

def main():
    single_mail()

if __name__ == "__main__":
    main()