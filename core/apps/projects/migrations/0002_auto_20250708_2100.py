from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('projects', 'Category')
    default_categories = [
        ("Paints & Pigments", "bi-paint-bucket"),
        ("Modeling Clay & Putty", "bi-gem"),
        ("Fabrics & Textiles", "bi-scissors"),
        ("Yarn & Thread", "bi-threads"),
        ("Wood & Lumber", "bi-stack"),
        ("Metal & Wire", "bi-magnet"),
        ("Electronic Components", "bi-cpu"),
        ("Adhesives & Glues", "bi-glue"),
        ("Tools", "bi-wrench-adjustable"),
        ("Fasteners (Screws, Nails)", "bi-tools"),
        ("Beads & Jewelry", "bi-gem"),
        ("Paper & Cardstock", "bi-file-earmark-text"),
        ("3D Printing", "bi-printer"),
        ("General Supplies", "bi-box-seam"),
    ]
    for name, icon in default_categories:
        Category.objects.create(name=name, owner=None, icon_class=icon)

class Migration(migrations.Migration):

    dependencies = [
        # This points to your first migration file
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]