#!/usr/bin/env python
"""Pre-generation hook for MCP Server Cookie Cutter.

This hook validates user inputs BEFORE the project is generated.
If validation fails, the project generation is aborted and the user
must re-run cookiecutter with valid inputs.
"""

import re
import sys


def validate_email(email):
    """Validate email address format.
    
    Args:
        email: The email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic email regex pattern
    # Matches: user@domain.com, user.name+tag@example.co.uk, etc.
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def validate_project_name(name):
    """Validate project name.
    
    Args:
        name: The project name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Project name should not be empty
    if not name or not name.strip():
        return False
    return True


def validate_port(port):
    """Validate server port number.
    
    Args:
        port: The port number as a string
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        port_num = int(port)
        # Valid port range is 1-65535
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


def main():
    """Main validation function."""
    # Get cookiecutter variables
    email = '{{ cookiecutter.email }}'
    project_name = '{{ cookiecutter.project_name }}'
    server_port = '{{ cookiecutter.server_port }}'
    
    # Track validation errors
    errors = []
    
    # Validate email
    if not validate_email(email):
        errors.append(f'❌ Invalid email address: "{email}"')
        errors.append('   Email must be in format: user@domain.com')
    
    # Validate project name
    if not validate_project_name(project_name):
        errors.append(f'❌ Invalid project name: "{project_name}"')
        errors.append('   Project name cannot be empty')
    
    # Validate port
    if not validate_port(server_port):
        errors.append(f'❌ Invalid port number: "{server_port}"')
        errors.append('   Port must be a number between 1 and 65535')
    
    # If there are errors, print them and exit
    if errors:
        print('\n' + '=' * 60)
        print('🚫 VALIDATION FAILED')
        print('=' * 60)
        for error in errors:
            print(error)
        print('\n💡 Please run cookiecutter again with valid inputs.')
        print('=' * 60)
        sys.exit(1)
    
    # All validations passed
    print('\n✅ All inputs validated successfully!')


if __name__ == '__main__':
    main()