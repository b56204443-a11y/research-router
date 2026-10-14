# Contributing

Please keep module discovery inexpensive and preserve the original authors' credit.

For a new or refreshed module:

1. Record a public source repository, pinned commit and applicable redistribution terms.
2. Preserve its licenses, copyright notices and third-party attribution. Resolve ambiguous terms before inclusion.
3. Add or update its catalog entry and `ORIGIN.md`; record changes to adapted files.
4. Regenerate the module catalog documentation and distributed SHA-256 snapshot using `scripts/update_metadata.py`.
5. Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`.

The snapshot generator does not grant a license or review scientific correctness.
Keep credentials, personal paths, downloaded papers, datasets, model weights and build caches out of commits.
Tests should verify routing and installation behavior; do not call paid external APIs in CI.

Use Issues for a reproducible failure or a specific module request. Include the Python version,
operating system and error text after removing credentials. A Pull Request should explain the
module's purpose, source and observable behavior changed.
