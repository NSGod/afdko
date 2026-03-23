"""
Shell completion script generator for afdko command.

Generates completion scripts for bash, zsh, fish, and PowerShell.
"""

import sys
from typing import List, Tuple


SUPPORTED_SHELLS = ['bash', 'zsh', 'fish', 'powershell']


def get_commands() -> List[Tuple[str, str]]:
    """Extract full command names and descriptions from invoker.

    Returns list of (name, description) tuples, excluding abbreviations.
    """
    from afdko.invoker import ALL_COMMANDS
    commands = []
    seen_targets = set()

    for name, (target, desc, _) in ALL_COMMANDS.items():
        # Skip abbreviations (they have desc=None)
        # Skip duplicate targets (same function, different name)
        if desc is not None and target not in seen_targets:
            commands.append((name, desc))
            seen_targets.add(target)

    return sorted(commands)


def generate_bash(commands: List[Tuple[str, str]]) -> str:
    """Generate bash completion script."""
    cmd_list = ' '.join(name for name, _ in commands)

    return f'''# bash completion for afdko
# Save this file or add to your ~/.bashrc:
#   eval "$(afdko completion bash)"

_afdko_completion() {{
    local cur="${{COMP_WORDS[COMP_CWORD]}}"
    local prev="${{COMP_WORDS[COMP_CWORD-1]}}"

    # Only complete the first argument (the command)
    if [ "$COMP_CWORD" -eq 1 ]; then
        local commands="{cmd_list}"
        COMPREPLY=($(compgen -W "$commands" -- "$cur"))
    fi
}}

complete -F _afdko_completion afdko
'''


def generate_zsh(commands: List[Tuple[str, str]]) -> str:
    """Generate zsh completion script."""
    # Build command list with descriptions
    cmd_lines = '\n        '.join(
        f"'{name}:{desc}'" for name, desc in commands
    )

    return f'''#compdef afdko
# zsh completion for afdko
# Save to a directory in your $fpath, e.g.:
#   afdko completion zsh > /usr/local/share/zsh/site-functions/_afdko
# Or add to ~/.zshrc:
#   eval "$(afdko completion zsh)"

_afdko() {{
    local -a commands
    commands=(
        {cmd_lines}
    )

    _arguments '1: :->command' '*::arg:->args'

    case $state in
        command)
            _describe 'afdko command' commands
            ;;
    esac
}}

_afdko "$@"
'''


def generate_fish(commands: List[Tuple[str, str]]) -> str:
    """Generate fish completion script."""
    # Generate one complete line per command
    complete_lines = '\n'.join(
        f'complete -c afdko -f -n "__fish_use_subcommand" '
        f'-a {name} -d "{desc}"'
        for name, desc in commands
    )

    return f'''# fish completion for afdko
# Save to ~/.config/fish/completions/afdko.fish:
#   afdko completion fish > ~/.config/fish/completions/afdko.fish

{complete_lines}
'''


def generate_powershell(commands: List[Tuple[str, str]]) -> str:
    """Generate PowerShell completion script."""
    # Build command array
    cmd_list = ', '.join(f"'{name}'" for name, _ in commands)

    return rf'''# PowerShell completion for afdko
# Add to your PowerShell profile:
#   afdko completion powershell | Out-String | Invoke-Expression
# Or open profile with:
#   notepad $profile

Register-ArgumentCompleter -Native -CommandName afdko -ScriptBlock {{
    param($wordToComplete, $commandAst, $cursorPosition)

    # Get the current line and cursor position
    $line = $commandAst.ToString()

    # Only complete if we're completing the first argument
    $words = $line -split '\s+'
    if ($words.Count -le 2) {{
        $commands = @({cmd_list})

        $commands | Where-Object {{ $_ -like "$wordToComplete*" }} |
            ForEach-Object {{
            [System.Management.Automation.CompletionResult]::new(
                $_,
                $_,
                'ParameterValue',
                $_
            )
        }}
    }}
}}
'''


def print_help() -> None:
    """Print help message."""
    print("Usage: afdko completion <shell>")
    print()
    print("Generate shell completion script for afdko commands.")
    print()
    print("Supported shells:")
    print("  bash       Bourne Again Shell")
    print("  zsh        Z Shell")
    print("  fish       Friendly Interactive Shell")
    print("  powershell PowerShell")
    print()
    print("Examples:")
    print("  # bash - add to ~/.bashrc or ~/.bash_profile")
    print('  eval "$(afdko completion bash)"')
    print()
    print("  # zsh - save to a directory in $fpath")
    print("  afdko completion zsh > "
          "/usr/local/share/zsh/site-functions/_afdko")
    print()
    print("  # fish - save to completions directory")
    print("  afdko completion fish > ~/.config/fish/completions/afdko.fish")
    print()
    print("  # PowerShell - add to profile")
    print('  afdko completion powershell | Out-String | Invoke-Expression')


def main() -> int:
    """Main entry point for completion command."""
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help', 'help'):
        print_help()
        return 0

    shell = sys.argv[1].lower()

    if shell not in SUPPORTED_SHELLS:
        print(f"Error: Unsupported shell '{shell}'", file=sys.stderr)
        print(f"Supported shells: {', '.join(SUPPORTED_SHELLS)}",
              file=sys.stderr)
        print("Run 'afdko completion --help' for more information.",
              file=sys.stderr)
        return 1

    # Get commands and generate completion script
    commands = get_commands()

    if shell == 'bash':
        script = generate_bash(commands)
    elif shell == 'zsh':
        script = generate_zsh(commands)
    elif shell == 'fish':
        script = generate_fish(commands)
    elif shell == 'powershell':
        script = generate_powershell(commands)
    else:
        # Should never reach here due to validation above
        return 1

    print(script, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
