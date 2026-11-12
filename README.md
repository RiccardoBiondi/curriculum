|**Author**|**Project**|**Build Status**|**CV Versions**|
|:--------:|:---------:|:--------------:|:-------------:|
| Riccardo Biondi | Personal CV | [![Project CI](https://github.com/RiccardoBiondi/curriculum/workflows/Ubuntu%20CI/badge.svg)](https://github.com/RiccardoBiondi/curriculum/actions/workflows/CI.yml) | [**ITA**](https://github.com/RiccardoBiondi/curriculum/blob/master/cv_ita.pdf) <br> [**ENG**](https://github.com/RiccardoBiondi/curriculum/blob/master/cv_eng.pdf)| 


# Curruculum

Simple repository to store and keep track of my personal cv and publication list. 

The repo contains:

- CV Files.
- Script to automatically retrieve the publication list.
- Script to automatically retrieve research metrics. (TODO)

## Usage

It is possible to build the CV by `make` command, according to the following rules:

```bash

make ita                                Make Italian Version

make eng                                Make English Version

make all                                Retrieve Publication list and build ita and eng cvs

make gen-bib                            Retrieve Publication List from scholar


make clean                              Clean build files
```


