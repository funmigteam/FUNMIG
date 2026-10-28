

from django.db import migrations


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0033_reaction'),


    ]


    operations = [


        migrations.DeleteModel(


            name='Reaction',


        ),


    ]


