# Persian localization

## Native foundation

Blender 4.5.9 has a native `fa_IR` language setting, identifies Persian among the localization languages, includes `locale/po/fa.po`, and flags Persian for RTL pre-processing in its gettext tools. The inspected catalog is 96,978 bytes and includes source strings and translations; this size is not a coverage percentage and does not prove all Blender UI strings are translated. No modified Persian catalog is included in this prototype.

The language menu uses the existing native preferences and translation catalog. It does not register a parallel runtime dictionary or claim that untranslated areas are localized. Missing strings should continue to use Blender's source-language fallback.

## Glossary workflow

The starter glossary in [`terminology/fa-glossary.csv`](terminology/fa-glossary.csv) is a terminology review list, not an imported translation catalog. Before adding translations to Blender:

1. Confirm the source context in the pinned revision and check Blender's current Persian Weblate terminology.
2. Have a fluent Persian technical reviewer approve the wording and distinguish UI labels from descriptive prose.
3. Modify the upstream gettext catalog with Blender's localization workflow, preserving contexts, plurals, metadata, and translator attribution.
4. Run Blender's catalog validation/build tools, inspect fuzzy/obsolete entries and Unicode, and verify source-language fallback.
5. Test the compiled catalog in the actual application, including mixed scripts, abbreviations, paths, numeric values, text entry, menus, and dialogs.

## RTL and text input

RTL translation preparation and widget direction are separate. Blender's Persian catalog is preprocessed by its localization tooling, but this is not a promise that every widget is correctly bidi-aware. Do not mirror the entire application or reverse technical control order. Verify Persian shaping alongside Latin words and identifiers, digits, punctuation, filesystem paths, search fields, text entry, and menu width at multiple UI scales. Report clipping or cursor-direction problems as limitations rather than hiding them with a global layout flip.

## Current scope

- The prototype language menu points to the existing `fa_IR` locale and `en_US` English UI.
- No new Persian UI translation strings are currently integrated.
- No language-switch, restart-persistence, shaping, or high-DPI runtime test has been run because a Blender executable is unavailable.
- The glossary requires a Persian technical review before it is treated as a project-wide standard.
