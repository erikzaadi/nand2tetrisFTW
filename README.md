# Configure vim for the Nand2Tetris Course

## Getting started:

Download the software package from the nand2tetris site

Copy the `runtools` directory to the extracted directory

## Plugins

https://github.com/zirrostig/vim-jack-syntax

https://github.com/suoto/vim-hdl

## Helpers

While editing a project:
```sh
:set makeprg=../runtools/test.sh\ %
```

In shell, to test an entire directory:

```sh
./runtools/test.sh ./0<X> 
```

Will exit with 0 if all comparisons work as they should

