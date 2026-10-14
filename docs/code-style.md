# Code style and quality checks

Every rule in this project is enforced by a tool, so style is never a matter of opinion in a
review. This document explains what each tool does, where it is configured and why each rule
exists.

## Overview

| Tool                                          | Responsibility                                   | Config                 |
| --------------------------------------------- | ------------------------------------------------ | ---------------------- |
| [Prettier](https://prettier.io/)              | How code looks: spacing, quotes, line breaks     | `prettier.config.ts`   |
| [ESLint](https://eslint.org/)                 | Whether code is correct, safe and consistent     | `eslint.config.ts`     |
| [TypeScript](https://www.typescriptlang.org/) | Type errors, via `astro check`                   | `tsconfig.json`        |
| [commitlint](https://commitlint.js.org/)      | Commit message format                            | `commitlint.config.ts` |
| [Lefthook](https://lefthook.dev/)             | Runs all of the above as git hooks               | `lefthook.yml`         |
| [EditorConfig](https://editorconfig.org/)     | Basic editor settings (indentation, line ending) | `.editorconfig`        |

Prettier and ESLint never overlap: Prettier owns formatting, ESLint owns everything else.
`eslint-config-prettier` switches off every ESLint rule that would fight Prettier.

## Prettier

Prettier rewrites files into one canonical format, so formatting never shows up in a diff or a
review. Only the options that differ from Prettier's defaults are set:

| Option               | Value                   | Why                                                                        |
| -------------------- | ----------------------- | -------------------------------------------------------------------------- |
| `printWidth`         | `100`                   | Readable on a laptop screen without wrapping lines too eagerly.            |
| `singleQuote`        | `true`                  | Single quotes in TS/JS. JSX attributes keep double quotes, like HTML.      |
| `plugins`            | Astro, Tailwind CSS     | Format `.astro` files and sort Tailwind classes in a fixed, logical order. |
| `tailwindStylesheet` | `src/styles/global.css` | Tells the class sorter where the Tailwind v4 theme lives.                  |

Defaults kept on purpose: 2-space indentation, semicolons, trailing commas everywhere (cleaner
diffs) and LF line endings.

Ignored: everything in `.gitignore`, plus `pnpm-lock.yaml` (generated).

## ESLint

The config is built in layers. Each layer adds rules for a specific concern.

### Shared configs

| Config                                     | Applies to | What it checks                                                                                                                                    |
| ------------------------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@eslint/js` recommended                   | All files  | Common JavaScript bugs (unreachable code, duplicate keys, ...).                                                                                   |
| `typescript-eslint` strict type-checked    | All files  | The strictest official TypeScript rules. Uses type information to catch bugs such as unhandled promises, unsafe `any` and unnecessary conditions. |
| `typescript-eslint` stylistic type-checked | All files  | Consistent TypeScript idioms (e.g. `??` over `\|\|` for defaults, `interface` over `type` for objects).                                           |
| `eslint-plugin-astro` recommended          | `.astro`   | Astro-specific mistakes.                                                                                                                          |
| `eslint-plugin-astro` jsx-a11y strict      | `.astro`   | Accessibility in Astro templates.                                                                                                                 |
| `@eslint-react` strict type-checked        | `.tsx`     | React correctness: keys, state usage, unsafe patterns, deprecated APIs.                                                                           |
| `eslint-plugin-react-hooks` recommended    | `.tsx`     | The Rules of Hooks and complete dependency arrays.                                                                                                |
| `eslint-plugin-jsx-a11y-x` strict          | `.tsx`     | Accessibility in React: alt text, keyboard support for click handlers, valid ARIA.                                                                |

### Project rules

| Rule                                         | Why                                                                                           |
| -------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `simple-import-sort/imports` and `/exports`  | Imports always in the same order, sorted automatically. No merge conflicts over import order. |
| `@typescript-eslint/consistent-type-imports` | Type-only imports use `import type`, so they are erased from the build.                       |
| `@stylistic/jsx-self-closing-comp`           | `<div />` instead of `<div></div>` for empty elements.                                        |
| `curly: all`                                 | Every `if`/`else`/loop body has braces, so adding a line never silently changes the logic.    |
| `eqeqeq: always`                             | `===` only. `==` converts types in surprising ways.                                           |
| `no-console`                                 | No leftover debug output.                                                                     |
| `object-shorthand`                           | `{ name }` instead of `{ name: name }`.                                                       |
| `prefer-const`                               | `const` unless the variable is reassigned, so reassignment is always intentional and visible. |
| `prefer-template`                            | Template literals instead of string concatenation.                                            |

Warnings fail the lint (`--max-warnings 0`): a warning that is allowed to stay is a warning
nobody reads.

### Why these plugins

- **`@eslint-react`** instead of the older `eslint-plugin-react`: it supports ESLint 10, uses
  type information and covers modern React (hooks, React 19 APIs).
- **`eslint-plugin-jsx-a11y-x`** instead of `eslint-plugin-jsx-a11y`: a maintained fork with the
  same rules that supports ESLint 10. The Astro plugin uses it too.

## TypeScript

`tsconfig.json` extends Astro's `strictest` preset: `strict` mode plus
`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`,
`noImplicitReturns`, `noUnusedLocals`, `noUnusedParameters` and `noFallthroughCasesInSwitch`.

TypeScript is pinned to 6.0.x because `typescript-eslint` and `astro check` do not support
TypeScript 7 yet.

## Git hooks

Lefthook installs the hooks automatically when `pnpm install` runs (the `prepare` script).

| Hook         | Runs                                                              | Purpose                                    |
| ------------ | ----------------------------------------------------------------- | ------------------------------------------ |
| `pre-commit` | `eslint --fix`, then `prettier --write`, on the staged files only | Every commit is linted and formatted.      |
| `commit-msg` | `commitlint`                                                      | Every commit message follows the format.   |
| `pre-push`   | Branch name check, then `pnpm check`                              | Nothing broken or misnamed reaches GitHub. |

Branch names must match `<type>/<issue>-<short-description>`, e.g. `feat/12-hero-section`. The
types are the same as the commit types.

Hooks run on your machine and could be skipped with `--no-verify`. That is never allowed
(see `CLAUDE.md`), and CI runs the same checks on GitHub where they cannot be skipped
(`.github/workflows/`).

## Editor setup

Open the project in VS Code and install the recommended extensions when prompted
(`.vscode/extensions.json`). `.vscode/settings.json` then formats on save with Prettier, applies
ESLint fixes on save and uses the project's TypeScript version.
