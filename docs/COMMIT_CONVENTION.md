# Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries
- `ci`: Changes to CI configuration files and scripts

## Scope
The scope should be the name of the module affected (as perceived by the person reading the changelog).

Examples:
- `feat(axe)`: New feature in the Axe tool
- `fix(lighthouse)`: Bug fix in the Lighthouse tool
- `docs(readme)`: Documentation changes in README
- `style(global)`: Global style changes

## Description
- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize first letter
- No dot (.) at the end

## Examples

```
feat(axe): add support for Firefox on Linux

fix(lighthouse): resolve Chrome launch issues on Windows

docs(readme): update installation instructions

style(global): format Python files according to PEP 8

refactor(axe): extract URL detection into separate module

test(lighthouse): add unit tests for URL validation

chore(deps): update Python dependencies

ci(actions): add GitHub Actions workflow
```

## Breaking Changes
When introducing breaking changes, add `BREAKING CHANGE:` in the commit body or footer:

```
feat(axe): change URL detection API

BREAKING CHANGE: The URL detection function now returns a tuple instead of a string
```
