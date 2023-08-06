
![](https://img.shields.io/github/issues/QuantumNovice/ModifiedCamClay) ![](https://img.shields.io/github/stars/QuantumNovice/ModifiedCamClay) ![](https://img.shields.io/github/license/QuantumNovice/ModifiedCamClay) ![](https://img.shields.io/badge/Maintained%3F-yes-green.svg) 

### Tested Platforms

![](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![](https://img.shields.io/badge/Linux_Mint-87CF3E?style=for-the-badge&logo=linux-mint&logoColor=white) ![](https://img.shields.io/badge/Alpine_Linux-0D597F?style=for-the-badge&logo=alpine-linux&logoColor=white) ![](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white) ![](https://img.shields.io/badge/Windows_XP-003399?style=for-the-badge&logo=windows-xp&logoColor=white) ![](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) 

# Modified Cam Clay ![](http://ForTheBadge.com/images/badges/made-with-python.svg)
The MCC model was created with triaxial load conditions in mind. The creation of the constitutive model representing the fluctuation of void ratio e (volumetric strain) as a function of the logarithm of the effective mean stress was based on experimental data on soft clays. 

# Installation

```bash
pip install modifiedcamclay
```
## Usage

### Drained Loading
```python
import modified_cam_clay as mcc


axial_strain, deviator_stress, label = mcc.drained(p_0, M, kappa, lmbda, e0)

mcc.plot(axial_strain, deviator_stress, label)
```


### Drained Loading
```python

import modified_cam_clay as mcc


axial_strain, deviator_stress, label = mcc.undrained(p_0, M, kappa, lmbda, e0, nu)


mcc.plot(axial_strain, deviator_stress, label)
```


## Results

![Drained](presentation/drained.png)
![Undrained](presentation/undrained.png)


### Tricks and Tips
```python
query_object = mcc.undrained(p_0, M, kappa, lmbda, e0, nu)
plot(*query_object)
```

## Cite Us

```bibtex
@software{Haseeb2022,
  author = {Syed Haseeb Shah, Tariq Khan and Saad MairajUddin, Abd Ullah},
  doi = {10.13140/RG.2.2.17604.71046},
  month = {4},
  title = {Modified Cam Clay in Python},
  url = {https://github.com/QuantumNovice/ModifiedCamClay},
  version = {1.0.1},
  year = {2022}
}
```
## About the Authors

We are a small group working from University of Engineering & Technology, Peshawar. Feel free to reach out to use at our slack, discord, gitub or email.

# Social
![](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white) ![](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)
