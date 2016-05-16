# Translation

Translation files are found in the `po/` directory.

## i18n not released yet

Kano OS is not fully i18n-aware and locales are not installed for end users, yet. You can translate this application, but as of now, users will still see the default English message strings.

## How to add a new translation

In this example, we're going to add a French translation:

    # install your target locale `fr_FR.utf8` with:
    sudo dpkg-reconfigure locales
    
    cd po/
    # create messages.pot
    make messages
    
    # create fr.po from messages.pot:
    msginit -l fr_FR.utf8
    
    # now use your favourite editor to translate fr.po
    
    # build locale files:
    make
    
    cd ..

    # prepare for testing as described in README.md
    # then change this in /usr/share/xgreeters/kano-greeter-devel.desktop
    Exec=dash -c "LC_ALL=fr_FR.utf8 /path/to/repo/bin/kano-greeter"
    
    # run test as in described in README.md

## How to make sure your code is i18n-aware

Add the gettext `_()` macro to all the user-visible message strings in your Python. List the Python source files that contain message strings in `PYPOTFILES`.

If you added new message strings or made changes to existing ones, do `make messages` to keep the template file up-to-date.

After that, merge the existing translations with `make update` and ask your translators to update their translations.

## gettext explained (in 20 seconds)

* User-visible strings in the source are marked with a macro of your choice. Usually, it's `_()`.
* `xgettext` extracts these message strings from your sources and puts them into a template file.
* This template file, usually named `messages.pot`, contains all user-visible strings of the project, but no translations.
* Translators use `msginit` to copy the template file into a new *portable object* file for their language (explained above).
* The translations are put into `<lang>.po`. It's a plain-text file format, you can use any text editor.
* More convenient, specialized `.po`-editors and web-based tools such as Pootle exist, as well.
* If your template file changes, use `msgmerge` to merge your existing translations with the new template, then re-translate the updated messages. Beware of `msgmerge`'s "fuzzy" matches.
* `msgfmt` converts a `.po` file into a binary *message object* file.
* You don't link these `.mo` files with your application binary.
* The `.mo` files are bundled alongside with your software as part of the distribution package.
* During installation, the `.mo` files are copied into the system's locale directory, usually `/usr/share/locale`.
* On startup, your application will look for the message object file that it needs for the current system locale.
* The locale even allows you to provide region-specific translations, e.g. "colour" for en_UK vs "color" for en_US.
* At runtime, all user-visible strings are being replaced with the translations.
* If no message object was found for the system locale, the original strings will be shown. 

## To-Do

Pootle or Transifex integration.
