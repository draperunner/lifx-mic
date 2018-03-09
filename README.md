## Setup

Ubuntu:

```bash
sudo apt-get install portaudio19-dev python-all-dev
```

Mac:

```bash
brew install portaudio
sudo pip install virtualenv
```

Then install Python dependencies

Ubuntu & Mac:

```bash
virtualenv venv -p python3
source venv/bin/activate
python install -r requirements.txt
```
