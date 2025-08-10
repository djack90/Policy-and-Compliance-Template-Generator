import os

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

def generate_password_policy(directory):
    min_length = get_int("Minimum password length", 8)
    require_special = get_yes_no("Require special characters? (yes/no): ")
    expiration = get_int("Password expiration days", 90)

    policy_text = f"""Password Policy Template

1. Purpose
This policy establishes password requirements to protect organizational systems, based on NIST SP 800-63 guidelines and ISO 27001 controls.

2. Policy
- Passwords must be at least {min_length} characters long.
- Passwords must {'include at least one special character' if require_special else 'not require special characters'}.
- Passwords expire every {expiration} days.

3. Scope
This policy applies to all employees, contractors, and systems.

4. Responsibilities
- Users must create and maintain passwords in accordance with this policy.
- Administrators must enforce password settings in systems.

5. Enforcement
Violations may result in disciplinary action and/or revocation of access.
"""

    filename = os.path.join(directory, "Password_Policy_Template.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(policy_text)
    print(f"Password policy template generated at {filename}")

def generate_access_control_policy(directory):
    roles_input = input("Roles defined (comma separated, e.g., admin,user,guest): ").strip()
    roles = [r.strip() for r in roles_input.split(",") if r.strip()] or ["admin", "user", "guest"]
    mfa_required = get_yes_no("Require multi-factor authentication? (yes/no): ")

    roles_list = "\n".join(f"- {role}" for role in roles)
    policy_text = f"""Access Control Policy Template

1. Purpose
This policy establishes access control requirements based on NIST SP 800-63 guidelines and ISO 27001 controls.

2. Roles
{roles_list}

3. Policy
- Access is granted based on the principle of least privilege.
- Multi-factor authentication is {'required' if mfa_required else 'not required'}.
- Roles must be assigned and reviewed regularly.

4. Scope
This policy applies to all systems and data.

5. Enforcement
Violations may result in disciplinary action and/or revocation of access.
"""

    filename = os.path.join(directory, "Access_Control_Policy_Template.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(policy_text)
    print(f"Access control policy template generated at {filename}")

def main():
    output_dir = os.path.join(os.path.dirname(__file__), "generated_policies")
    os.makedirs(output_dir, exist_ok=True)

    while True:
        choice = input("Choose a policy type ('password' or 'access control'): ").strip().lower()
        if choice in {"password", "password policy"}:
            generate_password_policy(output_dir)
            break
        if choice in {"access control", "access control policy"}:
            generate_access_control_policy(output_dir)
            break
        print("Invalid choice. Please enter 'password' or 'access control'.")

if __name__ == "__main__":
    main()
