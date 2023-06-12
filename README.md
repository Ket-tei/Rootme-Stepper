# Rootme-Stepper
This tool allows you to find out which Root-me challenges combinations will allow you to reach a particular points step.



## Installation

```bash
git clone https://github.com/Log-s/Rootme-Stepper.git
cd Rootme-Stepper
python3 -m pip install -r requirements.txt
```



## Usage

```plain
usage: rootmeStepper.py [-h] [-d] [-a  | -e ] username goal

Offers rootme challenges combinations to reach a goal

positional arguments:
  username              The rootme username. You can find it in your profile's URL
  goal                  The goal to reach

options:
  -h, --help            show this help message and exit
  -d , --depth          The maximum number of challenges to combine. Default is 3, higher than 4 may take a long time
  -a , --add-categories 
                        The categories to include, separated by commas. Default is all categories
  -e , --exclude-categories 
                        The categories to exclude, separated by commas. Default is all categories
```

## Examples

```
$ python3 rootmeStepper.py Log_s 9000 -a app-script,web-client,cracking
[*] Log_s : 8740
[*] Goal : 9000

[+] Found 18 combinations

==========================

[+] 1
	[*] 55	: [app-script] Javascript - Jail
	[*] 75	: [cracking] PE x86 - RunPE
	[*] 130	: [cracking] White-Box Cryptography #2

...

[+] 18
	[*] 75	: [web-client] XS Leaks
	[*] 75	: [cracking] PE x86 - RunPE
	[*] 110	: [cracking] Ringgit
```

```
$ python3 rootmeStepper.py Log_s 9000 -e realist,app-system,cryptanalysis,forensic
[*] Log_s : 8740
[*] Goal : 9000

[+] Found 33 combinations

==========================

[+] 1
	[*] 55	: [app-script] Javascript - Jail
	[*] 75	: [cracking] PE x86 - RunPE
	[*] 130	: [cracking] White-Box Cryptography #2

...

[+] 33
	[*] 55	: [web-server] PHP - Unserialize Pop Chain
	[*] 75	: [web-client] XS Leaks
	[*] 130	: [cracking] White-Box Cryptography #2
```

```
$ python3 rootmeStepper.py Log_s 9000 -d 2                                                                       
[*] Log_s : 8740
[*] Goal : 9000

[+] Found 22 combinations

==========================

[+] 1
	[*] 120	: [app-system] ELF ARM - Heap buffer overflow - Wilderness
	[*] 140	: [app-system] ELF ARM64 - Multithreading

...

[+] 22
	[*] 120	: [realist] I’m a Bl4ck H4t
	[*] 140	: [realist] SamBox v4
```

## Future updates

A future update will introduce an auto-correction of slightly misslepelled caterogies names.