# 🔒 Secure Password Generator

A modern, visually appealing, and cryptographically secure password generator built with **Python** and **CustomTkinter**.

This application helps users create strong, random passwords with customizable options and provides real-time feedback on password strength using entropy calculation.

## Features

- **Cryptographically Secure**: Uses `secrets` module (recommended over `random` for security).
- **Customizable Options**:
  - Adjustable password length (8–64 characters)
  - Include/exclude uppercase, lowercase, digits, and special characters
- **Real-Time Strength Meter**: Visual progress bar and color-coded strength rating based on entropy (bits).
- **One-Click Copy**: Copy generated password directly to clipboard.
- **Beautiful Dark Theme UI**: Built with CustomTkinter for a sleek, modern look.
- **Error Handling**: Clear messages if invalid combinations are selected.

## Strength Levels (Based on Entropy)

| Entropy (bits) | Rating       | Color     |
|----------------|--------------|-----------|
| < 40           | Very Weak    | Red       |
| 40–59          | Weak         | Orange    |
| 60–79          | Medium       | Yellow    |
| 80–99          | Strong       | Light Green |
| ≥ 100          | Very Strong  | Bright Green |
