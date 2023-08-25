#!/usr/bin/env python3

__author__ = "Venkata Kolagotla"
__created__ = "2023-08-24 19:16"
__last_updated__ = "2023-08-25 12:44"
__copyright__ = "Copyright 2023"
__credits__ = ["Venkata Kolagotla"]
__license__ = "Apache License, Version 2.0"
__version__ = "0.1.0"
__maintainer__ = "Venkata Kolagotla"
__email__ = "vkolagotla@pm.me"
__status__ = "Development"
__description__ = "Get external IP address and details"
__usage__ = "Place the script at ~/.config/argos/ with name extip.1m.py"


import requests
import subprocess
from typing import Dict, Optional

# Dictionary of all country codes and respective flag emojis
country_flags: Dict[str, str] = {
    "AF": "🇦🇫",  # Afghanistan
    "AL": "🇦🇱",  # Albania
    "DZ": "🇩🇿",  # Algeria
    "AD": "🇦🇩",  # Andorra
    "AO": "🇦🇴",  # Angola
    "AG": "🇦🇬",  # Antigua and Barbuda
    "AR": "🇦🇷",  # Argentina
    "AM": "🇦🇲",  # Armenia
    "AU": "🇦🇺",  # Australia
    "AT": "🇦🇹",  # Austria
    "AZ": "🇦🇿",  # Azerbaijan
    "BS": "🇧🇸",  # Bahamas
    "BH": "🇧🇭",  # Bahrain
    "BD": "🇧🇩",  # Bangladesh
    "BB": "🇧🇧",  # Barbados
    "BY": "🇧🇾",  # Belarus
    "BE": "🇧🇪",  # Belgium
    "BZ": "🇧🇿",  # Belize
    "BJ": "🇧🇯",  # Benin
    "BT": "🇧🇹",  # Bhutan
    "BO": "🇧🇴",  # Bolivia
    "BA": "🇧🇦",  # Bosnia and Herzegovina
    "BW": "🇧🇼",  # Botswana
    "BR": "🇧🇷",  # Brazil
    "BN": "🇧🇳",  # Brunei
    "BG": "🇧🇬",  # Bulgaria
    "BF": "🇧🇫",  # Burkina Faso
    "BI": "🇧🇮",  # Burundi
    "KH": "🇰🇭",  # Cambodia
    "CM": "🇨🇲",  # Cameroon
    "CA": "🇨🇦",  # Canada
    "CV": "🇨🇻",  # Cape Verde
    "CF": "🇨🇫",  # Central African Republic
    "TD": "🇹🇩",  # Chad
    "CL": "🇨🇱",  # Chile
    "CN": "🇨🇳",  # China
    "CO": "🇨🇴",  # Colombia
    "KM": "🇰🇲",  # Comoros
    "CG": "🇨🇬",  # Congo
    "CD": "🇨🇩",  # Democratic Republic of Congo
    "CR": "🇨🇷",  # Costa Rica
    "HR": "🇭🇷",  # Croatia
    "CU": "🇨🇺",  # Cuba
    "CY": "🇨🇾",  # Cyprus
    "CZ": "🇨🇿",  # Czech Republic
    "CI": "🇨🇮",  # Côte d'Ivoire
    "DK": "🇩🇰",  # Denmark
    "DJ": "🇩🇯",  # Djibouti
    "DM": "🇩🇲",  # Dominica
    "DO": "🇩🇴",  # Dominican Republic
    "EC": "🇪🇨",  # Ecuador
    "EG": "🇪🇬",  # Egypt
    "SV": "🇸🇻",  # El Salvador
    "GQ": "🇬🇶",  # Equatorial Guinea
    "ER": "🇪🇷",  # Eritrea
    "EE": "🇪🇪",  # Estonia
    "ET": "🇪🇹",  # Ethiopia
    "FJ": "🇫🇯",  # Fiji
    "FI": "🇫🇮",  # Finland
    "FR": "🇫🇷",  # France
    "GA": "🇬🇦",  # Gabon
    "GM": "🇬🇲",  # Gambia
    "GE": "🇬🇪",  # Georgia
    "DE": "🇩🇪",  # Germany
    "GH": "🇬🇭",  # Ghana
    "GR": "🇬🇷",  # Greece
    "GD": "🇬🇩",  # Grenada
    "GT": "🇬🇹",  # Guatemala
    "GN": "🇬🇳",  # Guinea
    "GW": "🇬🇼",  # Guinea-Bissau
    "GY": "🇬🇾",  # Guyana
    "HT": "🇭🇹",  # Haiti
    "HN": "🇭🇳",  # Honduras
    "HU": "🇭🇺",  # Hungary
    "IS": "🇮🇸",  # Iceland
    "IN": "🇮🇳",  # India
    "ID": "🇮🇩",  # Indonesia
    "IR": "🇮🇷",  # Iran
    "IQ": "🇮🇶",  # Iraq
    "IE": "🇮🇪",  # Ireland
    "IL": "🇮🇱",  # Israel
    "IT": "🇮🇹",  # Italy
    "JM": "🇯🇲",  # Jamaica
    "JP": "🇯🇵",  # Japan
    "JO": "🇯🇴",  # Jordan
    "KZ": "🇰🇿",  # Kazakhstan
    "KE": "🇰🇪",  # Kenya
    "KI": "🇰🇮",  # Kiribati
    "KP": "🇰🇵",  # North Korea
    "KR": "🇰🇷",  # South Korea
    "KW": "🇰🇼",  # Kuwait
    "KG": "🇰🇬",  # Kyrgyzstan
    "LA": "🇱🇦",  # Laos
    "LV": "🇱🇻",  # Latvia
    "LB": "🇱🇧",  # Lebanon
    "LS": "🇱🇸",  # Lesotho
    "LR": "🇱🇷",  # Liberia
    "LY": "🇱🇾",  # Libya
    "LI": "🇱🇮",  # Liechtenstein
    "LT": "🇱🇹",  # Lithuania
    "LU": "🇱🇺",  # Luxembourg
    "MG": "🇲🇬",  # Madagascar
    "MW": "🇲🇼",  # Malawi
    "MY": "🇲🇾",  # Malaysia
    "MV": "🇲🇻",  # Maldives
    "ML": "🇲🇱",  # Mali
    "MT": "🇲🇹",  # Malta
    "MH": "🇲🇭",  # Marshall Islands
    "MR": "🇲🇷",  # Mauritania
    "MU": "🇲🇺",  # Mauritius
    "MX": "🇲🇽",  # Mexico
    "FM": "🇫🇲",  # Micronesia
    "MD": "🇲🇩",  # Moldova
    "MC": "🇲🇨",  # Monaco
    "MN": "🇲🇳",  # Mongolia
    "ME": "🇲🇪",  # Montenegro
    "MA": "🇲🇦",  # Morocco
    "MZ": "🇲🇿",  # Mozambique
    "MM": "🇲🇲",  # Myanmar
    "NA": "🇳🇦",  # Namibia
    "NR": "🇳🇷",  # Nauru
    "NP": "🇳🇵",  # Nepal
    "NL": "🇳🇱",  # Netherlands
    "NZ": "🇳🇿",  # New Zealand
    "NI": "🇳🇮",  # Nicaragua
    "NE": "🇳🇪",  # Niger
    "NG": "🇳🇬",  # Nigeria
    "NO": "🇳🇴",  # Norway
    "OM": "🇴🇲",  # Oman
    "PK": "🇵🇰",  # Pakistan
    "PW": "🇵🇼",  # Palau
    "PS": "🇵🇸",  # Palestine
    "PA": "🇵🇦",  # Panama
    "PG": "🇵🇬",  # Papua New Guinea
    "PY": "🇵🇾",  # Paraguay
    "PE": "🇵🇪",  # Peru
    "PH": "🇵🇭",  # Philippines
    "PL": "🇵🇱",  # Poland
    "PT": "🇵🇹",  # Portugal
    "QA": "🇶🇦",  # Qatar
    "RO": "🇷🇴",  # Romania
    "RU": "🇷🇺",  # Russia
    "RW": "🇷🇼",  # Rwanda
    "KN": "🇰🇳",  # Saint Kitts and Nevis
    "LC": "🇱🇨",  # Saint Lucia
    "VC": "🇻🇨",  # Saint Vincent and the Grenadines
    "WS": "🇼🇸",  # Samoa
    "SM": "🇸🇲",  # San Marino
    "ST": "🇸🇹",  # Sao Tome and Principe
    "SA": "🇸🇦",  # Saudi Arabia
    "SN": "🇸🇳",  # Senegal
    "RS": "🇷🇸",  # Serbia
    "SC": "🇸🇨",  # Seychelles
    "SL": "🇸🇱",  # Sierra Leone
    "SG": "🇸🇬",  # Singapore
    "SK": "🇸🇰",  # Slovakia
    "SI": "🇸🇮",  # Slovenia
    "SB": "🇸🇧",  # Solomon Islands
    "SO": "🇸🇴",  # Somalia
    "ZA": "🇿🇦",  # South Africa
    "SS": "🇸🇸",  # South Sudan
    "ES": "🇪🇸",  # Spain
    "LK": "🇱🇰",  # Sri Lanka
    "SD": "🇸🇩",  # Sudan
    "SR": "🇸🇷",  # Suriname
    "SZ": "🇸🇿",  # Eswatini
    "SE": "🇸🇪",  # Sweden
    "CH": "🇨🇭",  # Switzerland
    "SY": "🇸🇾",  # Syria
    "TW": "🇹🇼",  # Taiwan
    "TJ": "🇹🇯",  # Tajikistan
    "TZ": "🇹🇿",  # Tanzania
    "TH": "🇹🇭",  # Thailand
    "TL": "🇹🇱",  # Timor-Leste
    "TG": "🇹🇬",  # Togo
    "TO": "🇹🇴",  # Tonga
    "TT": "🇹🇹",  # Trinidad and Tobago
    "TN": "🇹🇳",  # Tunisia
    "TR": "🇹🇷",  # Turkey
    "TM": "🇹🇲",  # Turkmenistan
    "TV": "🇹🇻",  # Tuvalu
    "UG": "🇺🇬",  # Uganda
    "UA": "🇺🇦",  # Ukraine
    "AE": "🇦🇪",  # United Arab Emirates
    "GB": "🇬🇧",  # United Kingdom
    "US": "🇺🇸",  # United States
    "UY": "🇺🇾",  # Uruguay
    "UZ": "🇺🇿",  # Uzbekistan
    "VU": "🇻🇺",  # Vanuatu
    "VA": "🇻🇦",  # Vatican City
    "VE": "🇻🇪",  # Venezuela
    "VN": "🇻🇳",  # Vietnam
    "YE": "🇾🇪",  # Yemen
    "ZM": "🇿🇲",  # Zambia
    "ZW": "🇿🇼",  # Zimbabwe
}


def get_public_ip() -> str:
    """Get public IP address.

    Parameters
    ----------
    None

    Returns
    -------
    str: Public IP address as a string.
    """
    response = requests.get("https://api64.ipify.org?format=json")
    data = response.json()
    return data["ip"]


def get_ip_details(ip: str) -> Optional[dict]:
    """Get IP details.

    Parameters
    ----------
    ip: str
        IP address as a string.

    Returns
    -------
    dict: IP details as a dictionary.
    """
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    return data


def is_vpn_active() -> bool:
    """Check if VPN is active.

    Parameters
    ----------
    None

    Returns
    -------
    bool: True if VPN is active, False otherwise.
    """
    try:
        output = subprocess.check_output(
            ["nmcli", "-t", "-f", "TYPE,DEVICE", "con"]
        ).decode("utf-8")
        return any(line.startswith("vpn:") for line in output.splitlines())
    except subprocess.CalledProcessError:
        return False


def main() -> None:
    """Main function."""
    # Get public IP address
    ip_address: str = get_public_ip()

    # Check if the IP details are available
    ip_details = get_ip_details(ip_address)
    if ip_details is None:
        print("Waiting for IP...")
        return

    country_code: str = ip_details.get("countryCode", "")
    city: str = ip_details.get("city", "")
    lat: float = ip_details.get("lat", "")
    lon: float = ip_details.get("lon", "")
    zip_code: str = ip_details.get("zip", "")
    region: str = ip_details.get("regionName", "")
    country: str = ip_details.get("country", "")
    isp: str = ip_details.get("isp", "")
    mobile: bool = ip_details.get("mobile", False)
    proxy: bool = ip_details.get("proxy", False)

    # Get flag emoji from dictionary
    flag_emoji: str = country_flags.get(country_code, "🌐")

    # Check if VPN is active
    vpn_active: bool = is_vpn_active()
    if vpn_active:
        vpn_status: str = "\033[32m ON🔒"  # Green color for locked emoji
    else:
        vpn_status = "\033[31m OFF🔓"  # Red color for unlocked emoji

    # Reset color after the emoji
    reset_color: str = "\033[0m"

    # Color for country code and city
    if vpn_active:
        country_code_color: str = "\033[32m"  # Green
        city_color: str = "\033[32m"  # Green
    else:
        country_code_color = "\033[31m"  # Red
        city_color = "\033[31m"  # Red

    # Output for top bar
    print(f"{flag_emoji}({city_color}{city}{reset_color})")
    print("---")
    print(f"Public IP: {reset_color}\033[33m{ip_address}\033[0m")
    print(f"Latitude: {reset_color}\033[33m{lat}\033[0m")
    print(f"Longitude: {reset_color}\033[33m{lon}\033[0m")
    print(f"Zipcode: {reset_color}\033[33m{zip_code}\033[0m")
    print(f"Region: {reset_color}\033[33m{region}\033[0m")
    print(f"Country: {reset_color}\033[33m{country}\033[0m")
    print(f"ISP: {reset_color}\033[33m{isp}\033[0m")
    print(
        f"Connection Type: {reset_color}\033[33m{'Cellular' if mobile else 'Non Cellular'}\033[0m"
    )
    print(f"Proxy: {reset_color}\033[33m{'Yes' if proxy else 'No'}\033[0m")
    print("VPN Status:", vpn_status, reset_color)
    print("---")
    # option to refresh the data
    print("Refresh | refresh=true")


if __name__ == "__main__":
    main()
