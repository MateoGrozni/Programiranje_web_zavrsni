from django.db import migrations

DEFAULT_MOOD_TAGS = [
    "Sreća",
    "Radost",
    "Mirnoća",
    "Zahvalnost",
    "Motivacija",
    "Ambicioznost",
    "Samopouzdanje",
    "Uzbuđenje",
    "Ponos",
    "Umor",
    "Ravnodušnost",
    "Dosada",
    "Zbunjenost",
    "Tuga",
    "Usamljenost",
    "Frustracija",
    "Ljutnja",
    "Strah",
    "Anksioznost",
    "Stres",
    "Preopterećenost",
    "Krivnja",
    "Sram",
]

def create_default_tags(apps, schema_editor):
    Tag = apps.get_model("main", "Tag")
    for name in DEFAULT_MOOD_TAGS:
        Tag.objects.get_or_create(name=name)

def remove_default_tags(apps, schema_editor):
    Tag = apps.get_model("main", "Tag")
    Tag.objects.filter(name__in=DEFAULT_MOOD_TAGS).delete()

class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_journalentry_options_alter_moodentry_options_and_more"),
    ]

    operations = [
        migrations.RunPython(create_default_tags, remove_default_tags),
    ]