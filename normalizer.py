import argparse
import re

# Django Email Validator Regexes (https://github.com/django/django/blob/stable/3.1.x/django/core/validators.py#L158-L165)
local_regex = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
    re.IGNORECASE,
)
domain_regex = re.compile(
    r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z",
    re.IGNORECASE,
)


def is_valid_email(local, domain):
    return local_regex.match(local) and domain_regex.match(domain)


def strip_after(local, char):
    return local.split(char)[0]


def remove_char(local, char):
    return local.strip(char)


def apply_provider_specific_rules(local, domain):
    return {
        "gmail.com": remove_char(strip_after(local, "+"), "."),
        "google.com": remove_char(strip_after(local, "+"), "."),
        "googlemail.com": remove_char(strip_after(local, "+"), "."),
        "fastmail.com": strip_after(local, "+"),
        "fastmail.fm": strip_after(local, "+"),
        "hotmail.com": strip_after(local, "+"),
        "icloud.com": strip_after(local, "+"),
        "live.com": strip_after(local, "+"),
        "mac.com": strip_after(local, "+"),
        "mailfence.com": strip_after(local, "+"),
        "me.com": strip_after(local, "+"),
        "mx.yandex.net": strip_after(local, "+"),
        "outlook.com": strip_after(local, "+"),
        "protonmail.ch": strip_after(local, "+"),
        "protonmail.com": strip_after(local, "+"),
        "rackspace.com": strip_after(local, "+"),
        "rocketmail.com": strip_after(local, "+"),
        "runbox.com": strip_after(local, "+"),
        "yandex.ru": strip_after(local, "+"),
        "zoho.com": strip_after(local, "+"),
        "ca.yahoo.com": strip_after(local, "-"),
        "qc.yahoo.com": strip_after(local, "-"),
        "yahoo.ae": strip_after(local, "-"),
        "yahoo.at": strip_after(local, "-"),
        "yahoo.co.id": strip_after(local, "-"),
        "yahoo.co.il": strip_after(local, "-"),
        "yahoo.co.in": strip_after(local, "-"),
        "yahoo.co.jp": strip_after(local, "-"),
        "yahoo.co.nz": strip_after(local, "-"),
        "yahoo.co.th": strip_after(local, "-"),
        "yahoo.co.uk": strip_after(local, "-"),
        "yahoo.co.za": strip_after(local, "-"),
        "yahoo.com": strip_after(local, "-"),
        "yahoo.com.ar": strip_after(local, "-"),
        "yahoo.com.au": strip_after(local, "-"),
        "yahoo.com.br": strip_after(local, "-"),
        "yahoo.com.co": strip_after(local, "-"),
        "yahoo.com.hk": strip_after(local, "-"),
        "yahoo.com.hr": strip_after(local, "-"),
        "yahoo.com.mx": strip_after(local, "-"),
        "yahoo.com.my": strip_after(local, "-"),
        "yahoo.com.ph": strip_after(local, "-"),
        "yahoo.com.sg": strip_after(local, "-"),
        "yahoo.com.tr": strip_after(local, "-"),
        "yahoo.com.tw": strip_after(local, "-"),
        "yahoo.com.vn": strip_after(local, "-"),
        "yahoo.cz": strip_after(local, "-"),
        "yahoo.de": strip_after(local, "-"),
        "yahoo.dk": strip_after(local, "-"),
        "yahoo.es": strip_after(local, "-"),
        "yahoo.fi": strip_after(local, "-"),
        "yahoo.fr": strip_after(local, "-"),
        "yahoo.gr": strip_after(local, "-"),
        "yahoo.hu": strip_after(local, "-"),
        "yahoo.ie": strip_after(local, "-"),
        "yahoo.in": strip_after(local, "-"),
        "yahoo.it": strip_after(local, "-"),
        "yahoo.nl": strip_after(local, "-"),
        "yahoo.no": strip_after(local, "-"),
        "yahoo.pl": strip_after(local, "-"),
        "yahoo.pt": strip_after(local, "-"),
        "yahoo.ro": strip_after(local, "-"),
        "yahoo.ru": strip_after(local, "-"),
        "yahoo.se": strip_after(local, "-"),
    }.get(domain, local)


def normalize_email_address(
    email,
    case_insensitive_local_support=True,
    aggressive_subaddressing_removal=False,
    internationalized_domain_support=False,
    validate_email=True,
):

    if validate_email and internationalized_domain_support:
        raise ValueError(
            "'validate_email' and 'internationalized_domain_support' cannot both be True."
        )

    try:
        local, domain = email.split("@", 1)
    except:
        print(f"Could not split on '@'. Invalid email address: {email}")
        exit(1)

    if validate_email:
        if not is_valid_email(local, domain):
            raise ValueError(
                f"Did not pass Django 3.1's email regex. Invalid email address: {email}"
            )

    if case_insensitive_local_support:
        # casefold() for unicode lowercase support
        local = local.casefold()

    if internationalized_domain_support:
        domain = domain.encode("idna").decode("utf8")
    else:
        domain.lower()

    if aggressive_subaddressing_removal:
        local = strip_after("-", strip_after("+", local))
    else:
        local = apply_provider_specific_rules(local, domain)

    return local + "@" + domain


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize Email Address")

    parser.add_argument(
        "--email", required=True, help="Email address to be normalized."
    )
    parser.add_argument(
        "--case-insensitive-local",
        default=True,
        action="store_false",
        help="Although the RFC requires case-sensitive locals most mail servers are case insensitive. \
          If you need to the local to case sensitive, use '--case-insensitive-local=False'.",
    )
    parser.add_argument(
        "--aggressive-subaddressing-removal",
        default=False,
        action="store_true",
        help="The default is to only apply sub-addressing based on known provider specific rules. \
          Use '--aggressive-subaddressing-remova=True' to remove all characters after '+' and  '-' in the provided local.",
    )
    parser.add_argument(
        "--internationalized_domain",
        default=False,
        action="store_true",
        help="By default non-ASCII characters are not allowed in the domain. \
          Use '--internationalized-domain=True' if you need support for interntionalized domains.",
    )
    parser.add_argument(
        "--validate_email",
        default=True,
        action="store_false",
        help="Email address to be validated against a subset of RFC 5322 rules. \
          There may be RFC compliant addresses filtered out.",
    )

    args = parser.parse_args()

    print(
        normalize_email_address(
            args.email,
            args.case_insensitive_local,
            args.aggressive_subaddressing_removal,
            args.internationalized_domain,
            args.validate_email,
        )
    )
