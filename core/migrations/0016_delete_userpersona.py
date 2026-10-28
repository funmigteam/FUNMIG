

from django.db import migrations


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0015_userpersona'),


    ]


    operations = [


        migrations.DeleteModel(


            name='UserPersona',


        ),


    ]


