# Security policy

## Reporting a vulnerability

Please do not open a public issue for a security problem. Use GitHub's private reporting instead:
open the **Security** tab of the repository and choose **Report a vulnerability**.

I will reply as soon as I can and credit you in the fix if you would like.

## API keys

Mini Duet reads your Anthropic API key from the `ANTHROPIC_API_KEY` environment variable and never writes it to disk.

- If you ever commit a key by mistake, **revoke it in the Anthropic Console right away** and create a new one. Deleting the commit is not enough.
- Keep `.env` files out of Git. The included `.gitignore` already does this.

