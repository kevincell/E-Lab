from django.db import migrations

def migrate_categories_to_courses(apps, schema_editor):
    Module = apps.get_model('core', 'Module')
    Course = apps.get_model('core', 'Course')
    User = apps.get_model('core', 'User')

    # Get unique categories
    categories = Module.objects.values_list('category', flat=True).distinct()
    
    for category in categories:
        if not category:
            continue
            
        # Create course
        name = category.replace('_', ' ').title()
        course, created = Course.objects.get_or_create(
            slug=category,
            defaults={'name': name}
        )
        
        # Link modules
        Module.objects.filter(category=category).update(course=course)
        
        # Update faculty who managed these modules
        faculty = User.objects.filter(managed_modules__category=category).distinct()
        for fac in faculty:
            fac.managed_courses.add(course)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_add_course_quiz_openended_models'),
    ]

    operations = [
        migrations.RunPython(migrate_categories_to_courses, migrations.RunPython.noop),
    ]
