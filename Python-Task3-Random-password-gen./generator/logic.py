import string
import secrets

AMBIGUOUS_CHARS = frozenset('0OIl1')

CHAR_SETS = {
    'uppercase': string.ascii_uppercase,
    'lowercase': string.ascii_lowercase,
    'numbers': string.digits,
    'symbols': string.punctuation,
}

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 64
MIN_CHAR_TYPES = 2


def _build_pool(selected_types, exclude_ambiguous):
    pool = ''
    for char_type in selected_types:
        chars = CHAR_SETS.get(char_type, '')
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pool += chars
    return pool


def _guarantee_representation(password_chars, selected_types, exclude_ambiguous, length):
    guaranteed = []
    for char_type in selected_types:
        chars = CHAR_SETS.get(char_type, '')
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS_CHARS)
        if chars:
            guaranteed.append(secrets.choice(chars))

    for i, ch in enumerate(guaranteed):
        pos = secrets.randbelow(length)
        while pos < len(password_chars) and password_chars[pos] in guaranteed[:i]:
            pos = secrets.randbelow(length)
        if pos < len(password_chars):
            password_chars[pos] = ch

    return password_chars


def generate_password(length=16, selected_types=None, exclude_ambiguous=False):
    if selected_types is None:
        selected_types = []

    if len(selected_types) < MIN_CHAR_TYPES:
        return None, 'Select at least 2 character types.'

    if length < MIN_PASSWORD_LENGTH:
        return None, f'Password length must be at least {MIN_PASSWORD_LENGTH} characters.'

    if length > MAX_PASSWORD_LENGTH:
        return None, f'Password length must not exceed {MAX_PASSWORD_LENGTH} characters.'

    pool = _build_pool(selected_types, exclude_ambiguous)

    if not pool:
        return None, 'No characters available after filtering.'

    password_chars = [secrets.choice(pool) for _ in range(length)]
    password_chars = _guarantee_representation(
        password_chars, selected_types, exclude_ambiguous, length
    )

    password = ''.join(password_chars)
    return password, None


def calculate_strength(password, selected_types):
    length = len(password)
    diversity = len(selected_types)

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if length >= 20:
        score += 1
    if diversity >= 2:
        score += 1
    if diversity >= 3:
        score += 1
    if diversity >= 4:
        score += 1

    if score <= 2:
        return 'Weak', 20, '#f7768e'
    elif score <= 4:
        return 'Medium', 50, '#ff9e64'
    elif score <= 5:
        return 'Strong', 75, '#9ece6a'
    else:
        return 'Very Secure', 100, '#73daca'


def estimate_crack_time(password, selected_types):
    pool_size = 0
    for char_type in selected_types:
        chars = CHAR_SETS.get(char_type, '')
        pool_size += len(chars)

    if pool_size == 0 or len(password) == 0:
        return 'Instant'

    entropy = len(password) * (pool_size.bit_length())
    guesses_per_second = 1e10
    seconds = (pool_size ** len(password)) / guesses_per_second

    if seconds < 1:
        return 'Instant'
    elif seconds < 60:
        return f'{int(seconds)} seconds'
    elif seconds < 3600:
        return f'{int(seconds // 60)} minutes'
    elif seconds < 86400:
        return f'{int(seconds // 3600)} hours'
    elif seconds < 31536000:
        return f'{int(seconds // 86400)} days'
    elif seconds < 31536000 * 1000:
        return f'{int(seconds // 31536000)} years'
    elif seconds < 31536000 * 1e6:
        return f'{int(seconds // (31536000 * 1000))} thousand years'
    elif seconds < 31536000 * 1e9:
        return f'{int(seconds // (31536000 * 1e6))} million years'
    else:
        return 'Billions of years+'


def validate_params(length, selected_types):
    errors = []

    if not isinstance(length, int) or length < MIN_PASSWORD_LENGTH:
        errors.append(f'Length must be at least {MIN_PASSWORD_LENGTH}.')

    if length > MAX_PASSWORD_LENGTH:
        errors.append(f'Length must not exceed {MAX_PASSWORD_LENGTH}.')

    if not isinstance(selected_types, list) or len(selected_types) < MIN_CHAR_TYPES:
        errors.append(f'Select at least {MIN_CHAR_TYPES} character types.')

    valid_types = set(CHAR_SETS.keys())
    if isinstance(selected_types, list):
        invalid = set(selected_types) - valid_types
        if invalid:
            errors.append(f'Invalid character types: {", ".join(invalid)}.')

    return errors
