import js from '@eslint/js';
import eslintReact from '@eslint-react/eslint-plugin';
import stylistic from '@stylistic/eslint-plugin';
import { defineConfig, globalIgnores } from 'eslint/config';
import eslintConfigPrettier from 'eslint-config-prettier/flat';
import astro from 'eslint-plugin-astro';
import jsxA11y from 'eslint-plugin-jsx-a11y-x';
import reactHooks from 'eslint-plugin-react-hooks';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import tseslint from 'typescript-eslint';

export default defineConfig(
  globalIgnores(['dist/', '.astro/']),

  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  astro.configs['flat/recommended'],
  astro.configs['flat/jsx-a11y-strict'],
  {
    // The Astro parser does not support `projectService` yet; `project` gives the same type info.
    files: ['**/*.astro'],
    languageOptions: { parserOptions: { projectService: false, project: true } },
  },

  {
    files: ['**/*.tsx'],
    extends: [
      eslintReact.configs['strict-type-checked'],
      reactHooks.configs.flat.recommended,
      jsxA11y.configs.strict,
    ],
  },

  // Turns off every rule that would conflict with Prettier, so must come after the shared configs.
  eslintConfigPrettier,

  {
    plugins: {
      '@stylistic': stylistic,
      'simple-import-sort': simpleImportSort,
    },
    rules: {
      '@stylistic/jsx-self-closing-comp': 'error',
      '@typescript-eslint/consistent-type-imports': 'error',
      curly: ['error', 'all'],
      eqeqeq: ['error', 'always'],
      'no-console': 'error',
      'object-shorthand': 'error',
      'prefer-const': 'error',
      'prefer-template': 'error',
      'simple-import-sort/exports': 'error',
      'simple-import-sort/imports': 'error',
    },
  },
);
