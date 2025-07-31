import re


def getOtpCode(channel_code, smsContext):

    pattern = r'\d{6}'
    matches = re.findall(pattern, smsContext)
    otpCode = matches[0]

    try:
        if channel_code.find("BOM") > -1:
            otpCode = smsContext.split(" ")[9].strip(".")
    except:
        pass

    try:
        if channel_code.find("GTE") > -1:
            otpCode = smsContext.split(" ")[-3].strip(" ")
    except:
        pass

    return otpCode
