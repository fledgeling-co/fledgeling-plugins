# F25-060 — restore catalogue version parity

Pinned upstream65119b6 and pre-child HEAD877cd1c both declare generate-investor-portal1.3.0
in its canonical plugin manifest but1.2.0 in the marketplace. A read-only audit of every plugin
found exactly this one mismatch. `child060-catalogue-baseline.log` records the actual mandatory
node gate exiting1 on it; F25-050 did not introduce it.

Change only that marketplace version to the already-existing1.3.0 and its generated catalogue
value. No plugin source, description, source path or other release version is changed by this
child. `child060-catalogue-green1.log` and green2 record the actual node catalogue gate exit0:
53skills,9groups,53icons. The gate generated only these fields and the pending F25-050
version/README fields; index staging keeps this child's one-row changes separate.

`tests/arm_catalogue_parity.py` temporarily puts1.2.0 back into this isolated worktree's actual
marketplace, invokes the real gate, requires the exact investor-portal mismatch and exit1, and
restores original bytes in finally. The JSON receipt records both hashes and successful restore.
The tested tree also contains pending F25-050 source/docs at0.16.1; this receipt is not a claim
that the preceding historical checkout had the same tree. No primary checkout/cache/install/
push/deployment was touched. Author evidence only; fresh review belongs to the conductor.
