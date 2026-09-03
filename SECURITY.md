# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| v1.0.0+ | ✅ Active support  |
| < v1.0  | ❌ End of life      |

## Reporting a Vulnerability

If you discover a security vulnerability in PJ-102-LLM-MeetingKB, please report it privately:

**Email**: security@foreverkol.local (示例)
**GitHub Security Advisories**: https://github.com/foreverkol/PJ-102-LLM-MeetingKB/security/advisories

Please include:
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

## Response Timeline

- **Initial response**: within 48 hours
- **Fix timeline**: within 7 days for critical issues

## Scope

The following are in scope:
- LLM Client code (llm_client.py)
- 12-step pipeline (steps/*.py)
- Version management scripts
- CI/CD workflows

The following are NOT in scope:
- Documentation issues
- Performance optimizations
- Feature requests

## Security Best Practices for Users

- ✅ Keep your `MINIMAX_API_KEY` secret
- ✅ Don't commit `.env` files
- ✅ Use HTTPS for API calls
- ✅ Regularly update dependencies
