# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Nothing yet

## [0.0.9]

### Added

- Handle `com_error` in a number of places. Still need to reduce duplication of this error-handling code
- Update to upstream dependency `docxrev` fixes `gradedoc close` hang [#18](https://github.com/blakeNaccarato/gradedoc/issues/18)

### Dependencies

- docxrev updated to ~> 0.2.3
- dynaconf updated to ~> 3.1.8
- rich updated to ~> 12.3.0

## [0.0.8]

- Clarify "Caller was rejected by the callee," error message

## [0.0.7]

- Clarify error message
- Fix bug involving document path reuse

## [0.0.6]

- Clarify error message
- Fix bug involving document path reuse

## [0.0.5]

- Make missing feedback code error friendlier

## [0.0.4]

- Fix bug involving relative paths
- Switch example AutoHotkey scripts to Windows Terminal to leverage `rich` formatting

## [0.0.3]

- Make headings flexible
- Search current working directory for DOCX files by default
- Use `rich` for prettier tracebacks
- Pin dependencies

## [0.0.2]

- Implement CLI
- Implement AutoHotkey scripts for common actions
- Expect `docx_dir` to be supplied in config file only
- Implement example within the package

## [0.0.1]

- Migrate `grade-me380`

[Unreleased]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.9...HEAD
[0.0.9]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.8...0.0.9
[0.0.8]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.7...0.0.8
[0.0.7]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.6...0.0.7
[0.0.6]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.5...0.0.6
[0.0.5]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.4...0.0.5
[0.0.4]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/blakeNaccarato/gradedoc/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/blakeNaccarato/gradedoc/releases/tag/0.0.1
