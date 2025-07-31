import hashlib


def generate_md5(string):
    md5_code = hashlib.md5(string.encode("utf-8")).hexdigest()
    return md5_code