Blind files
===========

Generates a mapping from file names to blind but memorable file names.  This
script assumes that you have a directory that contains files and / or
subdirectories with samples from an experiment.  The names of these files and
directories reveal which group the samples belong to, but the contents of the
files do not.

The script will move these files to a new directory, renaming them so that the
new file names do not reveal which group the samples belong to.  It will also
generate a mapping file to indicate how the new files map to the original
files.

Installing
----------

Run `pip3 install blind_files`.

Running
-------

This script takes an input dir, and generates a directory containing a script,
`blind.sh`, that can be used to blind the files in the input dir.  It also
generates a mapping csv, `mapping.csv`, that can be used after the user has
done the analysis to see how the original names map to blinded names.

The script has two modes of operation:

### Using a delimiter
In the first mode of operation, you can specify a delimiter to use such that
all the text before the delimiter in each file name will be replaced.  For
example:

```sh
blind_files \
   --mode delimiter \
   --delimiter _foo \
   --input-dir input_dir \
   --output-dir output_dir \
   --mapping-dir mapping_dir
```

In this case, if `input_dir` contains the following files:

```
sample_1_foo.txt
sample_1_foo-bar.csv
sample_2_foo.txt
hello.txt
```

Then after running `mapping_dir/blind.sh`, `output_dir` will contain

```
golf_elbow_foo.txt
golf_elbow_foo-bar.csv
co-producer_reputation_foo.txt
hello.txt
```

In `mapping_dir` you will also find a file `mapping.csv` with the contents:

```
original,blinded
sample_1,golf_elbow
sample_2,co-producer_reputation
```

#### Limitations
This will only replace names at the top level of the input directory.  If you
have a more complex nested directory structure, where the identifer names may
be buried in the directory tree, use identifier list approach described below.

### Using a list of identifiers
In the second mode of operation, you can specify list of identifiers that
should be blinded whenever they are encountered in the input directory tree.
For example, if `identifiers.txt` contains the following:

```
group_a_1
group_b_1
```

then running

```sh
blind_files \
   --mode identifiers \
   --identifiers identifiers.txt \
   --input-dir input_dir \
   --output-dir output_dir \
   --mapping-dir mapping_dir
```

In this case, if `input_dir` contains the following files:

```
group_a_1/group_a_1/foo.txt
group_b_1/group_b_1/foo.txt
hello.txt
```

Then after running `mapping_dir/blind.sh`, `output_dir` will contain

```
head_bottle/head_bottle/foo.txt
eponym_curtain/eponym_curtain/foo.txt
hello.txt
```

In `mapping_dir` you will also find a file `mapping.csv` with the contents:

```
original,blinded
group_a_1,head_bottle
group_b_1,eponym_curtain
```

#### Limitations
No identifier can be a substring of any other identifier.  For example, it is
not allowed to have identifiers `sample_1` and `sample_11`.  However,
`sample_01` and `sample_11` would be fine.

General limitations
-------------------
- This script should work on any platform, but has only been tested on Mac OS.
- This script should handle symlinks by simply moving the symlink, without
  following it, but this behavior has not been tested.

Credits
-------
This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter-pypackage).

nounlist from [here](http://www.desiquintans.com/downloads/nounlist/nounlist.txt).
