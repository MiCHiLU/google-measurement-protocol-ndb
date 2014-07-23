import gettext
import re
import uuid

from . import iso4217

_ = gettext.gettext

class ValidationError(Exception):
    """An error while validating data."""
    pass

def is_boolean(value):
    return value in (0, 1)

def is_integer(value):
    return isinstance(value, int) and 0 <= value

def is_currency(value):
    return isinstance(value, (int, float)) and 0 <= value

# see:
# http://stackoverflow.com/questions/2497294/regular-expression-to-validate-a-google-analytics-ua-number
# http://stackoverflow.com/questions/20411767/how-to-validate-google-analytics-tracking-id-using-a-javascript-function
tid_regex = re.compile(r"^(UA|YT|MO)-\d{4,10}-\d{1,4}$")

def is_tid(value):
    """
    >>> assert not is_tid(None)
    >>> assert not is_tid("UA-XXXX-Y")
    >>> assert is_tid("UA-1234-5")
    """
    return isinstance(value, str) and bool(tid_regex.match(value))

def validate_tid(value):
    if not is_tid(value):
        raise ValidationError(_("Enter a valid 'tid' (Tracking ID / Web Property ID)."))

def is_aip(value):
    """
    >>> assert is_aip("")
    >>> assert is_aip(0)
    >>> assert is_aip(1)
    >>> assert not is_aip(None)
    """
    return value in ("", 0, 1)

def validate_aip(value):
    if not is_aip(value):
        raise ValidationError(_("Enter a valid 'aip' (Anonymize IP)."))

is_qt = is_integer

def validate_qt(value):
    if not is_qt(value):
        raise ValidationError(_("Enter a valid 'qt' (Queue Time)."))

cid_regex = re.compile(r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$", re.IGNORECASE)

def is_cid(value):
    """
    >>> assert is_cid("35009a79-1a05-49d7-b876-2b884d0f825b")
    >>> assert not is_cid("35009a791a0549d7b8762b884d0f825b")
    >>> assert not is_cid(None)
    """
    try:
        u = uuid.UUID(value)
    except Exception:
        return False
    else:
        if bool(cid_regex.match(value)):
            return u.version == 4
        else:
            return False

def validate_cid(value):
    if not is_cid(value):
        raise ValidationError(_("Enter a valid 'cid' (Client ID)."))

def is_sc(value):
    """
    >>> assert is_sc("start")
    >>> assert is_sc("end")
    >>> assert not is_sc(None)
    """
    return value in ("start", "end")

def validate_sc(value):
    if not is_sc(value):
        raise ValidationError(_("Enter a valid 'sc' (Session Control)."))

# see:
# https://github.com/django/django/blob/master/django/core/validators.py
ipv4_regex = re.compile(r"^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$")

# see:
# http://home.deds.nl/~aeron/regex/
ipv6_regex = re.compile(r"^(((?=.*(::))(?!.*\3.+\3))\3?|[\dA-F]{1,4}:)([\dA-F]{1,4}(\3|:\b)|\2){5}(([\dA-F]{1,4}(\3|:\b|$)|\2){2}|(((2[0-4]|1\d|[1-9])?\d|25[0-5])\.?\b){4})\Z", re.IGNORECASE)

def is_uip(value):
    """
    >>> assert is_uip("1.2.3.4")
    >>> assert is_uip("2607:f0d0:1002:51::4")
    >>> assert is_uip("2607:f0d0:1002:0051:0000:0000:0000:0004")
    >>> assert not is_uip(None)
    """
    return isinstance(value, str) and (bool(ipv4_regex.match(value)) or bool(ipv6_regex.match(value)))

def validate_uip(value):
    if not is_uip(value):
        raise ValidationError(_("Enter a valid 'uip' (IP Override)."))

# see:
# https://github.com/django/django/blob/master/django/core/validators.py
url_regex = re.compile(
    r'^(?:[a-z0-9\.\-]*)://'  # scheme is validated separately
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$'
, re.IGNORECASE)

def is_dr(value):
    """
    >>> assert is_dr("http://example.com")
    >>> assert not is_dr(None)
    """
    return isinstance(value, str) and bool(url_regex.match(value)) and len(value) <= 2048

def validate_dr(value):
    if not is_dr(value):
        raise ValidationError(_("Enter a valid 'dr' (Document Referrer)."))

def is_cn(value):
    """
    >>> assert is_cn("(direct)")
    >>> assert not is_cn(None)
    """
    return isinstance(value, str) and len(value) <= 100

def validate_cn(value):
    if not is_cn(value):
        raise ValidationError(_("Enter a valid 'cn' (Campaign Name)."))

def is_cs(value):
    """
    >>> assert is_cs("(direct)")
    >>> assert not is_cs(None)
    """
    return isinstance(value, str) and len(value) <= 100

def validate_cs(value):
    if not is_cs(value):
        raise ValidationError(_("Enter a valid 'cs' (Campaign Source)."))

def is_cm(value):
    """
    >>> assert is_cm("organic")
    >>> assert not is_cm(None)
    """
    return isinstance(value, str) and len(value) <= 50

def validate_cm(value):
    if not is_cm(value):
        raise ValidationError(_("Enter a valid 'cm' (Campaign Medium)."))

def is_ck(value):
    """
    >>> assert is_ck("Blue Shoes")
    >>> assert not is_ck(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_ck(value):
    if not is_ck(value):
        raise ValidationError(_("Enter a valid 'ck' (Campaign Keyword)."))

def is_cc(value):
    """
    >>> assert is_cc("content")
    >>> assert not is_cc(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_cc(value):
    if not is_cc(value):
        raise ValidationError(_("Enter a valid 'cc' (Campaign Content)."))

def is_ci(value):
    """
    >>> assert is_ci("ID")
    >>> assert not is_ci(None)
    """
    return isinstance(value, str) and len(value) <= 100

def validate_ci(value):
    if not is_ci(value):
        raise ValidationError(_("Enter a valid 'ci' (Campaign ID)."))

def is_sr(value):
    """
    >>> assert is_sr("800x600")
    >>> assert not is_sr(None)
    """
    return isinstance(value, str) and len(value) <= 20

def validate_sr(value):
    if not is_sr(value):
        raise ValidationError(_("Enter a valid 'sr' (Screen Resolution)."))

def is_vp(value):
    """
    >>> assert is_vp("123x456")
    >>> assert not is_vp(None)
    """
    return isinstance(value, str) and len(value) <= 20

def validate_vp(value):
    if not is_vp(value):
        raise ValidationError(_("Enter a valid 'vp' (Viewport size)."))

def is_de(value):
    """
    >>> assert is_de("UTF-8")
    >>> assert not is_de(None)
    """
    return isinstance(value, str) and len(value) <= 20

def validate_de(value):
    if not is_de(value):
        raise ValidationError(_("Enter a valid 'de' (Document Encoding)."))

def is_sd(value):
    """
    >>> assert is_sd("24-bits")
    >>> assert not is_sd(None)
    """
    return isinstance(value, str) and len(value) <= 20

def validate_sd(value):
    if not is_sd(value):
        raise ValidationError(_("Enter a valid 'sd' (Screen Colors)."))

def is_ul(value):
    """
    >>> assert is_ul("en-us")
    >>> assert not is_ul(None)
    """
    return isinstance(value, str) and len(value) <= 20

def validate_ul(value):
    if not is_ul(value):
        raise ValidationError(_("Enter a valid 'ul' (User Language)."))

is_je = is_boolean

def validate_je(value):
    if not is_je(value):
        raise ValidationError(_("Enter a valid 'je' (Java Enabled)."))

def is_fl(value):
    """
    >>> assert is_fl("10 1 r103")
    >>> assert not is_fl(None)
    """
    return isinstance(value, str) and len(value) <= 20

def validate_fl(value):
    if not is_fl(value):
        raise ValidationError(_("Enter a valid 'fl' (Flash Version)."))

def is_t(value):
    """
    >>> assert is_t("pageview")
    >>> assert not is_t(None)
    """
    return value in ("pageview", "screenview", "event", "transaction", "item", "social", "exception", "timing")

def validate_t(value):
    if not is_t(value):
        raise ValidationError(_("Enter a valid 't' (Hit type)."))

is_ni = is_boolean

def validate_ni(value):
    if not is_ni(value):
        raise ValidationError(_("Enter a valid 'ni' (Non-Interaction Hit)."))

def is_dl(value):
    """
    >>> assert is_dl("http://foo.com/home?a=b")
    >>> assert not is_dl(None)
    """
    return isinstance(value, str) and bool(url_regex.match(value)) and len(value) <= 2048

def validate_dl(value):
    if not is_dl(value):
        raise ValidationError(_("Enter a valid 'dl' (Document location URL)."))

host_regex = re.compile(
    r'^'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'$'
, re.IGNORECASE)

def is_dh(value):
    """
    >>> assert is_dh("foo.com")
    >>> assert not is_dh(None)
    """
    return isinstance(value, str) and bool(host_regex.match(value)) and len(value) <= 100

def validate_dh(value):
    if not is_dh(value):
        raise ValidationError(_("Enter a valid 'dh' (Document Host Name)."))

path_regex = re.compile(
    r'^'
    r'(?:/?|[/?]\S+)'
    r'$'
)

def is_dp(value):
    """
    >>> assert is_dp("/foo")
    >>> assert not is_dp(None)
    """
    return isinstance(value, str) and bool(path_regex.match(value)) and len(value) <= 2048

def validate_dp(value):
    if not is_dp(value):
        raise ValidationError(_("Enter a valid 'dp' (Document Path)."))

def is_dt(value):
    """
    >>> assert is_dt("Settings")
    >>> assert not is_dt(None)
    """
    return isinstance(value, str) and len(value) <= 1500

def validate_dt(value):
    if not is_dt(value):
        raise ValidationError(_("Enter a valid 'dt' (Document Title)."))

def is_cd(value):
    """
    >>> assert is_cd("High Scores")
    >>> assert not is_cd(None)
    """
    return isinstance(value, str) and len(value) <= 2048

def validate_cd(value):
    if not is_cd(value):
        raise ValidationError(_("Enter a valid 'cd' (Screen Name)."))

def is_an(value):
    """
    >>> assert is_an("My App")
    >>> assert not is_an(None)
    """
    return isinstance(value, str) and len(value) <= 100

def validate_an(value):
    if not is_an(value):
        raise ValidationError(_("Enter a valid 'an' (Application Name)."))

def is_aid(value):
    """
    >>> assert is_aid("com.company.app")
    >>> assert not is_aid(None)
    """
    return isinstance(value, str) and len(value) <= 150

def validate_aid(value):
    if not is_aid(value):
        raise ValidationError(_("Enter a valid 'aid' (Application ID)."))

def is_av(value):
    """
    >>> assert is_av("1.2")
    >>> assert not is_av(None)
    """
    return isinstance(value, str) and len(value) <= 100

def validate_av(value):
    if not is_av(value):
        raise ValidationError(_("Enter a valid 'av' (Application Version)."))

def is_aiid(value):
    """
    >>> assert is_aiid("com.platform.vending")
    >>> assert not is_aiid(None)
    """
    return isinstance(value, str) and len(value) <= 150

def validate_aiid(value):
    if not is_aiid(value):
        raise ValidationError(_("Enter a valid 'aiid' (Application Installer ID)."))

def is_ec(value):
    """
    >>> assert is_ec("Category")
    >>> assert not is_ec(None)
    """
    return isinstance(value, str) and len(value) <= 150

def validate_ec(value):
    if not is_ec(value):
        raise ValidationError(_("Enter a valid 'ec' (Event Category)."))

def is_ea(value):
    """
    >>> assert is_ea("Action")
    >>> assert not is_ea(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_ea(value):
    if not is_ea(value):
        raise ValidationError(_("Enter a valid 'ea' (Event Action)."))

def is_el(value):
    """
    >>> assert is_el("Label")
    >>> assert not is_el(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_el(value):
    if not is_el(value):
        raise ValidationError(_("Enter a valid 'el' (Event Label)."))

is_ev = is_integer

def validate_ev(value):
    if not is_ev(value):
        raise ValidationError(_("Enter a valid 'ev' (Event Value)."))

def is_ti(value):
    """
    >>> assert is_ti("OD564")
    >>> assert not is_ti(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_ti(value):
    if not is_ti(value):
        raise ValidationError(_("Enter a valid 'ti' (Transaction ID)."))

def is_ta(value):
    """
    >>> assert is_ta("Member")
    >>> assert not is_ta(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_ta(value):
    if not is_ta(value):
        raise ValidationError(_("Enter a valid 'ta' (Transaction Affiliation)."))

is_tr = is_currency

def validate_tr(value):
    if not is_tr(value):
        raise ValidationError(_("Enter a valid 'tr' (Transaction Revenue)."))

is_ts = is_currency

def validate_ts(value):
    if not is_ts(value):
        raise ValidationError(_("Enter a valid 'ts' (Transaction Shipping)."))

is_tt = is_currency

def validate_tt(value):
    if not is_tt(value):
        raise ValidationError(_("Enter a valid 'tt' (Transaction Tax)."))

def is_in(value):
    """
    >>> assert is_in("Shoe")
    >>> assert not is_in(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_in(value):
    if not is_in(value):
        raise ValidationError(_("Enter a valid 'in' (Item Name)."))

is_ip = is_currency

def validate_ip(value):
    if not is_ip(value):
        raise ValidationError(_("Enter a valid 'ip' (Item Price)."))

is_iq = is_integer

def validate_iq(value):
    if not is_iq(value):
        raise ValidationError(_("Enter a valid 'iq' (Item Quantity)."))

def is_ic(value):
    """
    >>> assert is_ic("SKU47")
    >>> assert not is_ic(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_ic(value):
    if not is_ic(value):
        raise ValidationError(_("Enter a valid 'ic' (Item Code)."))

def is_iv(value):
    """
    >>> assert is_iv("Blue")
    >>> assert not is_iv(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_iv(value):
    if not is_iv(value):
        raise ValidationError(_("Enter a valid 'iv' (Item Category)."))

def is_cu(value):
    """
    >>> assert is_cu("EUR")
    >>> assert not is_cu(None)
    """
    return value in iso4217.codes

def validate_cu(value):
    if not is_cu(value):
        raise ValidationError(_("Enter a valid 'cu' (Currency Code)."))

is_prpr = is_currency

def validate_prpr(value):
    if not is_prpr(value):
        raise ValidationError(_("Enter a valid 'pr[\d+]pr' (Product Price)."))

is_prqt = is_integer

def validate_prqt(value):
    if not is_prqt(value):
        raise ValidationError(_("Enter a valid 'pr[\d+]qt' (Product Quantity)."))

is_prps = is_integer

def validate_prps(value):
    if not is_prps(value):
        raise ValidationError(_("Enter a valid 'pr[\d+]ps' (Product Position)."))

is_prcm = is_integer

def validate_prcm(value):
    if not is_prcm(value):
        raise ValidationError(_("Enter a valid 'pr[\d+]cm[index]' (Product Custom Metric)."))

def is_pa(value):
    """
    >>> assert is_pa("detail")
    >>> assert not is_pa(None)
    """
    return value in ("detail", "click", "add", "remove", "checkout", "checkout_option", "purchase", "refund")

def validate_pa(value):
    if not is_pa(value):
        raise ValidationError(_("Enter a valid 'pa' (Product Action)."))

is_cos = is_integer

def validate_cos(value):
    if not is_cos(value):
        raise ValidationError(_("Enter a valid 'cos' (Checkout Step)."))

is_ilpips = is_integer

def validate_ilpips(value):
    if not is_ilpips(value):
        raise ValidationError(_("Enter a valid 'il[\d+]pi[\d+]ps' (Product Impression Position)."))

is_ilpipr = is_currency

def validate_ilpipr(value):
    if not is_ilpipr(value):
        raise ValidationError(_("Enter a valid 'il[\d+]pi[\d+]pr' (Product Impression Price)."))

is_ilpicm = is_integer

def validate_ilpicm(value):
    if not is_ilpicm(value):
        raise ValidationError(_("Enter a valid 'il[\d+]pi[\d+]cm' (Product Impression Custom Metric)."))

def is_sn(value):
    """
    >>> assert is_sn("facebook")
    >>> assert not is_sn(None)
    """
    return isinstance(value, str) and len(value) <= 50

def validate_sn(value):
    if not is_sn(value):
        raise ValidationError(_("Enter a valid 'sn' (Social Network)."))

def is_sa(value):
    """
    >>> assert is_sa("like")
    >>> assert not is_sa(None)
    """
    return isinstance(value, str) and len(value) <= 50

def validate_sa(value):
    if not is_sa(value):
        raise ValidationError(_("Enter a valid 'sa' (Social Action)."))

def is_st(value):
    """
    >>> assert is_st("http://foo.com")
    >>> assert not is_st(None)
    """
    return isinstance(value, str) and len(value) <= 2048

def validate_st(value):
    if not is_st(value):
        raise ValidationError(_("Enter a valid 'st' (Social Action Target)."))

def is_utc(value):
    """
    >>> assert is_utc("category")
    >>> assert not is_utc(None)
    """
    return isinstance(value, str) and len(value) <= 150

def validate_utc(value):
    if not is_utc(value):
        raise ValidationError(_("Enter a valid 'utc' (User timing category)."))

def is_utv(value):
    """
    >>> assert is_utv("lookup")
    >>> assert not is_utv(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_utv(value):
    if not is_utv(value):
        raise ValidationError(_("Enter a valid 'utv' (User timing variable name)."))

is_utt = is_integer

def validate_utt(value):
    if not is_utt(value):
        raise ValidationError(_("Enter a valid 'utt' (User timing time)."))

def is_utl(value):
    """
    >>> assert is_utl("label")
    >>> assert not is_utl(None)
    """
    return isinstance(value, str) and len(value) <= 500

def validate_utl(value):
    if not is_utl(value):
        raise ValidationError(_("Enter a valid 'utl' (User timing label)."))

is_plt = is_integer

def validate_plt(value):
    if not is_plt(value):
        raise ValidationError(_("Enter a valid 'plt' (Page Load Time)."))

is_dns = is_integer

def validate_dns(value):
    if not is_dns(value):
        raise ValidationError(_("Enter a valid 'dns' (DNS Time)."))

is_pdt = is_integer

def validate_pdt(value):
    if not is_pdt(value):
        raise ValidationError(_("Enter a valid 'pdt' (Page Download Time)."))

is_rrt = is_integer

def validate_rrt(value):
    if not is_rrt(value):
        raise ValidationError(_("Enter a valid 'rrt' (Redirect Response Time)."))

is_tcp = is_integer

def validate_tcp(value):
    if not is_tcp(value):
        raise ValidationError(_("Enter a valid 'tcp' (TCP Connect Time)."))

is_srt = is_integer

def validate_srt(value):
    if not is_srt(value):
        raise ValidationError(_("Enter a valid 'srt' (Server Response Time)."))

def is_exd(value):
    """
    >>> assert is_exd("DatabaseError")
    >>> assert not is_exd(None)
    """
    return isinstance(value, str) and len(value) <= 150

def validate_exd(value):
    if not is_exd(value):
        raise ValidationError(_("Enter a valid 'exd' (Exception Description)."))

is_exf = is_boolean

def validate_exf(value):
    if not is_exf(value):
        raise ValidationError(_("Enter a valid 'exf' (Is Exception Fatal?)."))

def is_cd_(value):
    """
    >>> assert is_cd_("Sports")
    >>> assert not is_cd_(None)
    """
    return isinstance(value, str) and len(value) <= 150

def validate_cd_(value):
    if not is_cd_(value):
        raise ValidationError(_("Enter a valid 'cd[1-9][0-9]*' (Custom Dimension)."))

is_cm_ = is_integer

def validate_cm_(value):
    if not is_cm_(value):
        raise ValidationError(_("Enter a valid 'cm[1-9][0-9]*' (Custom Metric)."))

def is_xid(value):
    """
    >>> assert is_xid("Qp0gahJ3RAO3DJ18b0XoUQ")
    >>> assert not is_xid(None)
    """
    return isinstance(value, str) and len(value) <= 40

def validate_xid(value):
    if not is_xid(value):
        raise ValidationError(_("Enter a valid 'xid' (Experiment ID)."))
