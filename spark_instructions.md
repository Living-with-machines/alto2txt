## Process publications via Spark

When running via Spark ensure that:

* `xml_in_dir` and `txt_out_dir` are on a file system accessible to all Spark worker nodes.
* Provide a log file location, using the `-l` flag, that is accessible to all Spark worker nodes.
* The code is available as a package on all Spark worker nodes.

For example, the code can be run on Urika requesting as follows...

Install the code as a package:

```bash
python setup.py install
```

Run `spark-submit`:

```bash
spark-submit ./extract_publications_text.py \
    -p spark \
    -n 144 \
    -l /mnt/lustre/at003/at003/<username>/log.out     \
    /mnt/lustre/at003/at003/shared/findmypast/BNA/    \
    /mnt/lustre/at003/at003/<username>/fmp-lancs-txt
```

For Urika, it is recommended that the value of 144 be used for
`NUM_CORES`. This, with the number of cores per node, determines the
number of workers/executors and nodes. As Urika has 36 cores per node,
this would request 144/36 = 4 workers/executors and nodes.