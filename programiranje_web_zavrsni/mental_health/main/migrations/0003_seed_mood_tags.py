from django.db import migrations

DEFAULT_MOOD_TAGS = [
    "sreća",
    "radost",
    "mirnoća",
    "zahvalnost",
    "motivacija",
    "ambicioznost",
    "samopouzdanje",
    "uzbuđenje",
    "ponos",
    "umor",
    "ravnodušnost",
    "dosada",
    "zbunjenost",
    "tuga",
    "usamljenost",
    "frustracija",
    "ljutnja",
    "strah",
    "anksioznost",
    "stres",
    "preopterećenost",
    "krivnja",
    "sram",
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