"""
Embedded wordlist for educational hash checking.
This is a SMALL sample wordlist for demonstration purposes only.
In production, use large password dumps responsibly.
"""

COMMON_PASSWORDS = [
    # Top 100 most common passwords (educational sample)
    "123456", "password", "12345678", "qwerty", "123456789",
    "12345", "1234", "111111", "1234567", "dragon",
    "123123", "baseball", "abc123", "football", "monkey",
    "letmein", "shadow", "master", "666666", "qwertyuiop",
    "123321", "mustang", "1234567890", "michael", "654321",
    "pussy", "superman", "1qaz2wsx", "7777777", "fuckyou",
    "121212", "000000", "qazwsx", "123qwe", "killer",
    "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh",
    "hunter", "buster", "soccer", "harley", "batman",
    "andrew", "tigger", "sunshine", "iloveyou", "fuckme",
    "2000", "charlie", "robert", "thomas", "hockey",
    "ranger", "daniel", "starwars", "klaster", "112233",
    "george", "asshole", "computer", "michelle", "jessica",
    "pepper", "1111", "zxcvbn", "555555", "11111111",
    "131313", "freedom", "777777", "pass", "fuck",
    "maggie", "159753", "aaaaaa", "ginger", "princess",
    "joshua", "cheese", "amanda", "summer", "love",
    "ashley", "nicole", "chelsea", "biteme", "matthew",
    "access", "yankees", "987654321", "dallas", "austin",
    "thunder", "taylor", "matrix", "mobilemail", "mom",
    "monitor", "monitoring", "montana", "moon", "moscow",
    # Additional common patterns
    "password1", "password123", "admin", "admin123", "root",
    "toor", "pass123", "test", "guest", "default",
    "changeme", "welcome", "welcome1", "hello", "secret",
    "letmein1", "passw0rd", "p@ssword", "p@ssw0rd", "qwerty123",
    # Names + numbers
    "john1990", "john1991", "john1992", "jane1990", "jane1991",
    "mike1990", "mike1991", "admin@123", "root@123", "pass@123",
    # Keyboard patterns
    "qwe123", "qweasd", "asdf1234", "zxcv1234", "1q2w3e",
    "1q2w3e4r", "q1w2e3r4", "1qaz2wsx", "zaq1xsw2", "!@#$%^&*",
    # Weak PINs
    "0000", "0001", "0002", "1234", "4321", "9999", "8888",
    # Company defaults
    "cisco", "cisco123", "juniper", "netgear", "linksys",
    "administrator", "admin1234", "password!", "welcome1!",
]

# Extended educational patterns
EDUCATIONAL_PATTERNS = [
    # Date patterns
    "01011990", "31121990", "01012000", "31122000",
    "1990", "1991", "1992", "1993", "1994", "1995",
    "2020", "2021", "2022", "2023", "2024", "2025",
    # Sports teams
    "liverpool", "chelsea", "arsenal", "mancity", "manutd",
    "realmadrid", "barcelona", "bayern", "juventus",
    # Movies/shows
    "starwars", "batman", "superman", "spiderman", "ironman",
    "marvel", "dc comics", "game of thrones", "breaking bad",
    # Tech terms
    "google", "facebook", "twitter", "instagram", "amazon",
    "apple", "microsoft", "linux", "windows", "android",
    # Generic
    "letmein", "welcome", "changeme", "secret", "admin",
    "password", "guest", "test", "demo", "sample",
]


def get_all_words():
    """Return combined wordlist for hash checking."""
    return list(set(COMMON_PASSWORDS + EDUCATIONAL_PATTERNS))
