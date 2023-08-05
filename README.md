# ml_training

this environment use belows
- pyenv
- venv


# set up for ubuntu

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src
echo '' >> ~/.bashrc
echo '##pyenv' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

open new bash shell

```
cd ~/ml_training
pyenv install 3.10.12
pyenv local 3.10.12
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

if you want to exit venv, type below
```
deactivate
```

# usage
