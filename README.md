Rootme-Stepper

-

This tool allows you to find out which Root-me challenges combinations will allow you to reach a particular points step.



# Installation

```bash
git clone https://github.com/Log-s/Rootme-Stepper.git
cd Rootme-Stepper
python3 -m pip install -r requirements.txt
```



# Usage

`python3 rootmeStepper.py <username> <goal> [<depth>]`

- **username** : The user you want to search for. Make sure he is unique (use the username that appear in the URL when checking his profile

- **goal** : The number you want to reach (example : 8000)

- **depth** : The maximum amount of challenges to reach the goal. Default is 3. If you choose more than 4, the calculation time may be extensive

  

  Examples :

  - `python3 rootmeStepper.py Log_s 7000 3`
  - `python3 rootmeStepper.py Log_s 8000`

# Future updates

There will probably be an update to exclude some category, to reduce the number of results.

