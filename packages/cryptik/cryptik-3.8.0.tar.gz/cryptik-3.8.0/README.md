## About ##

a [cli](https://en.wikipedia.org/wiki/Command-line_interface)-based application for displaying the current price of a cryptocurrency. cryptik supports multiple exchanges and multiple currencies.

Please see the project wiki for supported currencies and supported exchanges or to request new currencies/exchanges.


## Requirements ##

- python3


## Install

- download cryptik: 

```
# set release tag as desired.
release=3.1.1
wget https://gitlab.com/drad/cryptik/-/archive/${release}/cryptik-${release}.tar.bz2 \
  && tar -xjf cryptik-${release}.tar.bz2 \
  && rm cryptik-${release}.tar.bz2 \
  && chmod u+x cryptik-${release}/cryptik.py
```


## Setup ##

Although a virtual environment is not required, we strongly recommend it to keep cryptic's requirements separated from other python apps you may have. You can create a virtual environment with the following: 

- install virtualenv: `pacman -S virtualenv`
- setup virtualenv for cryptic (in cryptic root): `python3 -m virtualenv .venv`
- activate virtualenv: `source .venv/bin/activate`
- install requirements: `pip install -r requirements.txt`

We recommend copying the config file to `~/.config/cryptik`:
```
mkdir ~/.config/cryptik \
  && cp cryptik-${release}/example/config.toml ~/.config/cryptik/
```
> ignore this step if you already have a `config.toml` file setup

- modify the config file as needed
	- note: no changes are required; however, the app can be customized to your taste.
- create app symlink (optional): `ln -sf -t ~/bin/ "$HOME/apps/cryptik/cryptik-${release}/cryptik.py"`
  - note: replace ${release} with the version you downloaded
  - note: the above symlink assumes you perform the download step (above) in the ~/apps/cryptik directory and that ~/bin is in your $PATH


## Usage ##
- call cryptik from command line: `cryptik.py -e BITSTAMP -t BTC`
	- show full response: `cryptik.py -d full`
- list all available exchanges: `cryptik.py -l`
- get help on cryptik: `cryptik.py -h`
- example conky usage (note: this will show prices from two exchanges):
```
CRYPTIK
  ${texeci 600 cryptik.py -e KRAKEN -t BTC}
  ${texeci 600 cryptik.py -e BITSTAMP -t BTC}
```

## Example Response
* direct call:
```
$ cryptik.py -e BITSTAMP -t BTC
BTMP:BTC $9711.24 @12:33
```
