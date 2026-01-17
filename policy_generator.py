import os
from dataclasses import dataclass
from typing import Callable, Dict, Any


def get_yes_no(prompt):
    """Prompt the user with a yes/no question."""
    while True:
        response = input(prompt).strip().lower()
        if response in {"yes", "y"}:
            return True
        if response in {"no", "n"}:
            return False
        print("Please enter 'yes' or 'no'.")


def get_int(prompt, default):
    """Prompt the user for an integer with a default value."""
    while True:
        response = input(f"{prompt} [{default}]: ").strip()
        if not response:
            return default
        if response.isdigit():
            return int(response)
        print("Please enter a valid number.")


@dataclass
class PolicyTemplate:
    """Represents a policy template with its configuration."""
    name: str
    filename: str
    input_collector: Callable[[], Dict[str, Any]]
    template_generator: Callable[[Dict[str, Any]], str]


def collect_password_policy_inputs():
    """Collect user inputs for password policy."""
    return {
        'min_length': get_int("Minimum password length", 8),
        'require_special': get_yes_no("Require special characters? (yes/no): "),
        'expiration': get_int("Password expiration days", 90)
    }


def generate_password_policy_text(inputs):
    """Generate password policy text from inputs."""
    special_char_text = 'include at least one special character' if inputs['require_special'] else 'not require special characters'

    return f"""Password Policy Template

1. Purpose
This policy establishes password requirements to protect organizational systems, based on NIST SP 800-63 guidelines and ISO 27001 controls.

2. Policy
- Passwords must be at least {inputs['min_length']} characters long.
- Passwords must {special_char_text}.
- Passwords expire every {inputs['expiration']} days.

3. Scope
This policy applies to all employees, contractors, and systems.

4. Responsibilities
- Users must create and maintain passwords in accordance with this policy.
- Administrators must enforce password settings in systems.

5. Enforcement
Violations may result in disciplinary action and/or revocation of access.
"""


def collect_access_control_policy_inputs():
    """Collect user inputs for access control policy."""
    roles_input = input("Roles defined (comma separated, e.g., admin,user,guest): ").strip()
    roles = [r.strip() for r in roles_input.split(",") if r.strip()] or ["admin", "user", "guest"]

    return {
        'roles': roles,
        'mfa_required': get_yes_no("Require multi-factor authentication? (yes/no): ")
    }


def generate_access_control_policy_text(inputs):
    """Generate access control policy text from inputs."""
    roles_list = "\n".join(f"- {role}" for role in inputs['roles'])
    mfa_text = 'required' if inputs['mfa_required'] else 'not required'

    return f"""Access Control Policy Template

1. Purpose
This policy establishes access control requirements based on NIST SP 800-63 guidelines and ISO 27001 controls.

2. Roles
{roles_list}

3. Policy
- Access is granted based on the principle of least privilege.
- Multi-factor authentication is {mfa_text}.
- Roles must be assigned and reviewed regularly.

4. Scope
This policy applies to all systems and data.

5. Enforcement
Violations may result in disciplinary action and/or revocation of access.
"""


def write_policy_file(directory, filename, content):
    """Write policy content to a file."""
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Policy template generated at {filepath}")
    return filepath


def generate_policy(policy_template, output_directory):
    """Generate a policy using the provided template configuration."""
    inputs = policy_template.input_collector()
    policy_text = policy_template.template_generator(inputs)
    write_policy_file(output_directory, policy_template.filename, policy_text)


# Policy registry: maps user-friendly names to policy templates
POLICY_REGISTRY = {
    'password': PolicyTemplate(
        name='Password Policy',
        filename='Password_Policy_Template.md',
        input_collector=collect_password_policy_inputs,
        template_generator=generate_password_policy_text
    ),
    'access control': PolicyTemplate(
        name='Access Control Policy',
        filename='Access_Control_Policy_Template.md',
        input_collector=collect_access_control_policy_inputs,
        template_generator=generate_access_control_policy_text
    )
}

# Valid policy type aliases for user input
POLICY_ALIASES = {
    'password': 'password',
    'password policy': 'password',
    'access control': 'access control',
    'access control policy': 'access control'
}


def get_policy_choice():
    """Prompt user to select a policy type and return the normalized choice."""
    valid_options = ', '.join(f"'{key}'" for key in POLICY_REGISTRY.keys())

    while True:
        choice = input(f"Choose a policy type ({valid_options}): ").strip().lower()
        normalized_choice = POLICY_ALIASES.get(choice)

        if normalized_choice:
            return normalized_choice

        print(f"Invalid choice. Please enter {valid_options}.")


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "generated_policies")
    os.makedirs(output_dir, exist_ok=True)

    policy_choice = get_policy_choice()
    policy_template = POLICY_REGISTRY[policy_choice]
    generate_policy(policy_template, output_dir)


if __name__ == "__main__":
    main()
