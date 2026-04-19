# Serenity Maze — متاهة الـ 15 دقيقة

Interactive 15-minute sleep preparation experience generator for digital sleep books.

## Overview

This project generates:
- **Interactive HTML page** — Arabic RTL dark-themed UI with countdown timer, anxiety assessment, and personalized calm messaging
- **PDF package** — Includes QR code, feature documentation, and implementation guide
- **QR code image** — Links to the HTML experience

## Features

- ⏱️ 15-minute countdown timer
- 🙏 Interactive anxiety assessment with personalized responses
- 🎨 Dark theme optimized for nighttime viewing
- 🌍 Arabic right-to-left (RTL) layout with Tajawal font
- 🎁 Reward section with sleep audio suggestions
- 📱 Mobile-responsive design
- 📊 Professional PDF documentation

## Requirements

```
reportlab>=4.0
qrcode[pil]>=8.0
pillow>=10.0
```

## Usage

```bash
python serenity_maze_generator.py
```

This generates:
- `output/serenity-maze.html` — Interactive experience
- `output/sleep-qr-pack.pdf` — Documentation and QR code
- `output/qr.png` — Scannable QR code image

## Deployment

1. Upload `serenity-maze.html` to your web host
2. Update QR code URL to point to the live hosted page
3. Regenerate QR code with final URL
4. Include PDF in your digital product offerings

## Color Palette

- **Primary**: Deep navy (#0b132b)
- **Accent**: Warm gold (#c5a059)
- **Calm**: Soft teal (#87d6d1)
- **Success**: Soft green (#8de0a8)

## License

All rights reserved.
