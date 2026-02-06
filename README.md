# Piplup

Simple API that receives an image via POST request and save it to $HOME/Images/

## Installation

1. Install dependencies

```bash
uv sync
```

2. Run

```bash
uv run piplup
```

3. Add service to systemd

```bash
mkdir -p ~/.config/systemd/user
cp ./piplup.service ~/.config/systemd/user/piplup.service
sed -i "s/USER/$USER/g; s|/path/to/piplup|$PWD|g" ~/.config/systemd/user/piplup.service
```

4. Enable and start service

```bash
systemctl --user enable --now piplup.service
```

Submit your images to http://api_ip:6969/upload
