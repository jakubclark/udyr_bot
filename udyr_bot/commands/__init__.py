from .base_commands import get_github_url, get_help_text, get_random_quote

commands = {
    '!quote': get_random_quote,
    '!help': get_help_text,
    '!github': get_github_url
}
