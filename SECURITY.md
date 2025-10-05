# Security Policy

## Reporting Security Vulnerabilities

**AIQ CRM Insight Scout** is a hackathon project focused on Agentic AI for CRM systems. Security is important, but as a prototype, it may contain vulnerabilities. Report issues responsibly.

### How to Report

- **Do Not** report vulnerabilities via GitHub Issues or public channels.
- Email the maintainer at [your-email@example.com] or open a private discussion on GitHub.
- Provide details: Description, steps to reproduce, impact, and affected version (e.g., v1.0).

For NVIDIA API-related issues, refer to NVIDIA's security guidelines: [NVIDIA Security Vulnerability Submission Form](https://www.nvidia.com/en-us/about-nvidia/security-bulletin/).

### Supported Versions

- **v1.0**: Actively maintained (hackathon prototype).
- Older versions: Not supported.

### Disclosed Vulnerabilities

No known vulnerabilities at this time.

## Security Considerations for Deployment

- **API Keys**: Never commit `.env` files; use environment variables securely.
- **Data Privacy**: The project processes sample CRM documents (e.g., contracts, compliance checklists). In production, ensure compliance with laws like CCPA and GDPR.
- **Dependencies**: Review `requirements.txt` for vulnerabilities using tools like `pip-audit`.
- **Local Deployment Only**: Designed for localhost (http://localhost:8000/); do not expose publicly without authentication.
- **NVIDIA NIM API**: Secure your `NVIDIA_API_KEY`; limit usage to prevent quota exhaustion.

## Why This Matters for CRM

In CRM systems, security is critical for handling sensitive data (e.g., contracts, customer info). This project demonstrates basic safeguards, but for production, implement:
- Authentication (e.g., FastAPI dependencies).
- Input validation to prevent injection attacks.
- Logging without exposing PII.

Follow the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md) when reporting issues.

For general questions, use GitHub Issues.