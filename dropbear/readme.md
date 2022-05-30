# How to build this code

Install the [GBDK 2020 (v4.0.6)](https://github.com/gbdk-2020/gbdk-2020) then run:

```sh
"{path where you installed the GBDK}/bin/lcc" -c -o ./main.o ./main.c
"{path where you installed the GBDK}/bin/lcc" -o ./main.gb ./main.o
```

to compile to a GB rom
