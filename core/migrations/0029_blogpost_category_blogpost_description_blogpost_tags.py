

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0028_savedpost'),


    ]


    operations = [


        migrations.AddField(


            model_name='blogpost',


            name='category',


            field=models.CharField(blank=True, max_length=100, verbose_name='دسته\u200cبندی'),


        ),


        migrations.AddField(


            model_name='blogpost',


            name='description',


            field=models.TextField(blank=True, verbose_name='خلاصه مقاله'),


        ),


        migrations.AddField(


            model_name='blogpost',


            name='tags',


            field=models.CharField(blank=True, max_length=200, verbose_name='برچسب\u200cها'),


        ),


    ]


