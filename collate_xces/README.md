# Collate XCES files into a flat TXT

Run the script as:

```sh
python3 collate.py $INPUTFILE
```

Where `$INPUTFILE` is the path to a file containing a list of XML files conforming to [the XCES schema](http://www.xces.org/) (eg. the output of ILSP focused crawler).

The script writes a file `$INPUTFILE.collated.txt`, which contains all of the non-boilerplate text content from the XML files.
