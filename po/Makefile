APPNAME=terminal-quest
ORG="Kano Computing Ltd."

MSGLANGS=$(notdir $(wildcard *po))
MSGOBJS=$(addprefix ../locale/,$(MSGLANGS:.po=/LC_MESSAGES/$(APPNAME).mo))

.PHONY: clean_locales messages

build: $(MSGOBJS)

update: $(MSGLANGS)

clean_locales:
	rm -rf ../locale

clean: clean_locales
	rm -f messages.pot

define generate-pypotfiles
grep "env python" -rl --exclude=*.py --exclude=Makefile .. > PYPOTFILES
find .. -name *.py >> PYPOTFILES
endef

define run-xgettext
xgettext -f PYPOTFILES -L Python --force-po -o messages.pot \
    --keyword=N_ --package-name=$(APPNAME) --copyright-holder=$(ORG)
endef

messages:
	$(generate-pypotfiles)
	$(run-xgettext)

messages.pot:
	$(generate-pypotfiles)
	$(run-xgettext)

%.po: messages.pot
	msgmerge -N -U $*.po messages.pot
	touch $*.po

../locale/%/LC_MESSAGES/$(APPNAME).mo: clean_locales
	mkdir -p $(dir $@)
	msgfmt -c -o $@ $*.po
