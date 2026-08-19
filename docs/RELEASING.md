# Releasing GuessNova

1. Ensure `main` CI is green.
2. Update `CHANGELOG.md` and the version in `pyproject.toml` and `src/guessnova/__init__.py`.
3. Run the complete local check suite.
4. Create a signed or annotated tag such as `v1.0.1`.
5. Push the tag.
6. The release workflow builds source and wheel artifacts and attaches them to the GitHub Release.
7. Verify installation from the built wheel in a clean Python 3.13 environment.

Do not publish secrets, local state files, developer `.env` files, or private user data in release artifacts.
