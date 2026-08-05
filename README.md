# 🐛 Worm-AI CLI — GrokApi Edition

**Worm-AI CLI** is a sleek command-line interface (CLI) for interacting with Grok models through an **unofficial reverse-engineered API wrapper**.
It features jailbreak injection, a customizable terminal UI, and a lightweight design for fast and flexible LLM interaction.

> ⚡ Lightweight. Powerful. Terminal-native.
> Built with ❤️ by [@kafyasfngl](https://github.com/kafyasfngl)

---

## 🚀 Features

* 🔗 **Unofficial Grok API wrapper** (reverse-engineered backend)
* 🧠 **Jailbreak system** built-in for unrestricted responses
* 🎨 Fully **customizable terminal UI** — colors, banners, prompt style
* ⚙️ Modular design for easy backend or UI replacement

---

## 🧩 Backend / API

Worm-AI uses a **reverse-engineered Grok API wrapper** originally developed here:

> [https://github.com/realasfngl/Grok-Api](https://github.com/realasfngl/Grok-Api)

This wrapper acts as a proxy-like interface, allowing the CLI to access Grok endpoints **without official API credentials**.

> ⚠️ **Disclaimer / Legal Notice**
>
> * This project is **unofficial** and not affiliated with xAI or Grok.
> * For research, educational, and local testing purposes **only**.
> * Avoid misuse, heavy scraping, or violating API provider terms.

---

## 📦 Requirements

* Python **3.8+**
* `pip` installed

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/kafyasfngl/worm-ai
cd worm-ai
pip install -r requirements.txt
python3 main.py
```

---


## 💬 Usage

Run the CLI:

```bash
python3 main.py
```

Then start chatting:

```
> Who created SpaceX?
```

---

## 🎨 Customizable CLI UI

You can change the terminal experience to your style:

* **Banner color** & ASCII logo
* **Prompt symbol**
* **Typing animation speed**


---

## 🔒 Security Notes

* Do **not** commit encrypted folders like `pyarmor_runtime_000000/` to public repos.
* Store private configs or endpoints in a `.env` file and add it to `.gitignore`.
* Obfuscate sensitive modules using [PyArmor](https://pyarmor.readthedocs.io/en/latest/).

---

## 👨‍💻 Credits

**Author:** [@kafyasfngl](https://github.com/kafyasfngl)
**Thanks to:** [@neo](https://github.com/realasfngl)
**Telegram:** [t.me/xsocietyforums](https://t.me/xsocietyforums)

---

### 🌐 Project URL

> [https://github.com/kafyasfngl/worm-ai](https://github.com/kafyasfngl/worm-ai)

## Implementation branch
Branch: implement/overpowered-suggestions — contains scaffolding and stubs for metrics, training, RAG, and CI examples.

See docs/IMPLEMENTATION_PLAN.md and docs/ROADMAP.md for next steps.
