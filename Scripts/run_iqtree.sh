#!/bin/bash
# Using GTR+ASC because MFP crashed initially
iqtree2 -s ../results/snippy_final_core/core.aln -m GTR+ASC -B 1000 -T AUTO --redo