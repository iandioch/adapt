# Convert .dix file to .dic

This is a small rough script to translate an [Apertium .dix file](http://wiki.apertium.org/wiki/Dix) into a [.dic file suitable for hunalign](https://github.com/danielvarga/hunalign#dictionary)

You should run the file as so:

```sh
python3 dix2dic.py path/to/dixfile.dix
```

The script will write a new file, `path/to/dixfile.dix.dic`. 
