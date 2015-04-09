#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function

"""
Print the hierarchy below Term, GO:0030663
>>> python {SCR} GO:0030663

- GO:0030663	level-05	depth-07	COPI-coated vesicle membrane [cellular_component]
-- GO:0012508	level-05	depth-08	Golgi to ER transport vesicle membrane [cellular_component]
-- GO:0012509	level-05	depth-08	inter-Golgi transport vesicle membrane [cellular_component]


Write the hierarchy below Term, GO:0030663 into a file
>>> python {SCR} GO:0030663 --o=hier_GO_0030663.rpt

  WROTE: hier_GO_0030663.rpt

Print the hierarchy for biological process, molecular_function, and cellular_component:
>>> python {SCR} --o=hier_BP_MF_CC.rpt

Print hierarchy for BP, MF, CC only printing the first 2 levels.
>>> python {SCR} --max_depth=2
>>> python {SCR} --max_depth=2 --dash_len=2 --num_child

Print hierarchy
-  26894 GO:0008150	level-00	depth-00	biological_process [biological_process]
--    30 GO:0001906	level-01	depth-01	cell killing [biological_process]
--   555 GO:0002376	level-01	depth-01	immune system process [biological_process]
-- 11208 GO:0065007	level-01	depth-01	biological regulation [biological_process]

>>> python {SCR} 

This program prints the hierarchy for all GO terms, if no argument is provided.
If a GO term is provided as an argument, then the hierarchy of all children 
for that term is printed.

""".format(SCR=__file__)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from goatools.obo_parser import GODag


if __name__ == "__main__":

    import argparse
    p = argparse.ArgumentParser(__doc__,
                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('go_ids', type=str, nargs='*',
                 help='GO Term, e.g. GO:0070458')
    p.add_argument('--o', default=None, type=str,
                 help="Specifies the name of the output file")
    p.add_argument('--no_indent', default=False,
                 help="Do not indent GO terms", action='store_true')
    p.add_argument('--obo', default="go-basic.obo", type=str,
                 help="Location and name of the obo file")
    p.add_argument('--dash_len', default=1, type=int,
                 help="Printed width of the dashes column")
    p.add_argument('--max_depth', default=None, type=int,
                 help="max depth for printing relative to GO Term")
    p.add_argument('--num_child', default=None, action='store_true',
                 help="Print total number of children for each GO")

    args = p.parse_args()

    obo_dag = GODag(obo_file=args.obo)

    file_out = sys.stdout if args.o is None else open(args.o, 'w')
    lenprt = args.dash_len if not args.no_indent else None

    if args.go_ids:
      for go_id in args.go_ids:
        obo_dag.write_hier(
            go_id, 
            file_out, 
            len_dash=lenprt,
            max_depth=args.max_depth,
            num_child=args.num_child)
    else:
      obo_dag.write_hier_all(
          file_out, 
          len_dash=lenprt,
          max_depth=args.max_depth,
          num_child=args.num_child)

    if args.o is not None:
      file_out.close()
      sys.stdout.write("  WROTE: {}\n".format(args.o))

