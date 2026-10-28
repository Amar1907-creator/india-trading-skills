# Security Policy

## Supported versions

Only the latest release on `main` receives fixes.

## What this project does and doesn't do

- It **does not** ask for, store or send broker logins, API keys, passwords or OTPs.
- It **does not** place orders or connect to trading accounts.
- Scripts only make read-only HTTPS requests for public market prices (Yahoo Finance).
- `india-portfolio-review` reads holdings you provide (or that a connected broker connector returns) and keeps
  them on your computer. Holdings files are git-ignored.

If you find code that breaks any of these, treat it as a security issue.

## Reporting a vulnerability

Please **do not open a public issue**. Use
[GitHub's private vulnerability reporting](https://github.com/Amar1907-creator/india-trading-skills/security/advisories/new) instead, and include:

- what the problem is and which file it's in
- steps to reproduce
- what impact you think it has

You'll get a reply as soon as possible, and you'll be credited in the fix unless you prefer not to be.

## Scam warning

This project is free and has no paid version, tip service, Telegram channel or WhatsApp group. Anyone claiming
otherwise is not connected to this project.
