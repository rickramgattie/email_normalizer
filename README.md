# email_normalizer

This script normalizes email addresses based on a list of providers with known subaddressing or 'plus addressing' rules.

### Notes on RFC Compliance
+ The seperator sequence of the _local-part_ of an emai address is dependent on the implementation of the mail server [RFC 5233](https://tools.ietf.org/html/rfc5233).
+ There aren't any specific guidelines on the priority of comments vs. subaddressing in either [RFC 5233 - Sieve Email Filtering: Subaddress Extension](https://tools.ietf.org/html/rfc5233) or [RFC 5322 - Internet Message Format](https://tools.ietf.org/html/rfc5322#section-3.4). From what I have experienced, some servers (ex. gmail) will consider everything after the subaddress identifier (ex. in gmail's it is '+') a subaddress of the local.
+ Although [RFC 5321 - Simple Mail Transfer Protocol](https://tools.ietf.org/html/rfc5321#section-2.4) says that "The local-part of a mailbox MUST BE treated as case sensitive" most mail servers default to a case insensitive local.
+ Internationalized domains ought to be converted to [punycode](https://tools.ietf.org/html/rfc3492).
+ When `--validate_email` is used, the provided email is validated against [Django 3.1's](https://github.com/django/django/blob/stable/3.1.x/django/core/validators.py#L158-L165) email validator regex. This regex only allows a subset of valid email addresses according to the [RFC 3696 - Application Techniques for Checking and Transformation of Names](https://tools.ietf.org/html/rfc3696#section-3).

### Usage
```bash
usage: normalizer.py [-h] --email EMAIL [--case-insensitive-local]
                     [--aggressive-subaddressing-removal] [--internationalized_domain]
                     [--validate_email]
```
