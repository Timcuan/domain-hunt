# Penguin-OS 🐧

**Abstract Chain Interface** - A terminal-style website inspired by Pudgy Penguin aesthetics and CLI design.

## 🚀 Features

- **Terminal-Style UX**: Inspired by `ethos.vision` with CLI aesthetics
- **Multi-Page Structure**: Separate HTML files for different sections
- **Animated Boot Sequence**: Simulated OS installation with typing effects
- **Virtual Desktop**: Interactive modules for farming, airdrops, and chat
- **Responsive Design**: Works on desktop and mobile devices
- **No Frameworks**: Pure HTML + TailwindCSS + Vanilla JS

## 📁 File Structure

```
penguin-os/
├── index.html          # Landing page with boot sequence
├── install.html        # Simulated OS installer
├── desktop.html        # Virtual Penguin OS desktop
├── docs.html          # Documentation and guides
├── js/
│   └── main.js        # Main JavaScript utilities
├── assets/
│   └── pengu.txt      # ASCII penguin mascot
└── README.md          # This file
```

## 🎨 Design Theme

- **Background**: Pure black `#000000`
- **Text**: Neon cyan `#00FFFF`
- **Accent**: Pudgy blue `#0077FF`
- **Font**: Monospace (Fira Code, Courier New)
- **Style**: Terminal/CLI aesthetic

## 🛠️ Setup

1. **Clone or download** the project files
2. **Open** `index.html` in your web browser
3. **Navigate** through the different pages using the CLI-styled buttons

## 📱 Pages Overview

### `index.html` - Landing Page
- Animated boot sequence
- ASCII penguin mascot
- CLI-styled navigation buttons
- System information display

### `install.html` - OS Installer
- Simulated installation process
- Progress bar with real-time updates
- Typing animations for log messages
- Links to desktop after completion

### `desktop.html` - Virtual OS
- Interactive window modules:
  - 🐧 **Farm**: Staking interface with APY display
  - 🎁 **Airdrop**: Wallet connection simulation
  - 💻 **Codes**: Terminal command snippets
  - 💬 **Chat**: Real-time messaging interface
- Toggle-able windows
- System status bar

### `docs.html` - Documentation
- Markdown-style layout
- Tokenomics information for $POS
- Developer API documentation
- GitHub integration links

## 🎯 Key Features

### Typing Effects
- Animated text appearing character by character
- Blinking cursor effects
- Simulated terminal boot sequence

### Interactive Elements
- CLI-styled buttons with hover effects
- Toggle-able desktop windows
- Simulated chat with typing placeholders

### Responsive Design
- Mobile-friendly layout
- Grid-based responsive components
- Consistent terminal theme across devices

## 🚀 Usage

1. **Start at the landing page** (`index.html`)
2. **Choose your path**:
   - `--install` → Simulate OS installation
   - `--launch` → Access virtual desktop
   - `--docs` → View documentation
3. **Explore the desktop** with interactive modules
4. **Read the docs** for detailed information

## 🎨 Customization

### Colors
Modify the CSS variables in each HTML file:
```css
.text-cyan-300    /* Main text color */
.text-blue-400    /* Accent color */
.border-cyan-500  /* Border color */
```

### Content
- Update ASCII art in `assets/pengu.txt`
- Modify installation messages in `install.html`
- Customize desktop modules in `desktop.html`

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Penguin-OS** - Where terminal meets blockchain! 🐧✨