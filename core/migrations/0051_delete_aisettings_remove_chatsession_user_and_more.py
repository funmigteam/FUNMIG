                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_teamportfolioproject'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AISettings',
        ),
        migrations.RemoveField(
            model_name='chatsession',
            name='user',
        ),
        migrations.RemoveField(
            model_name='paymentrequest',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='token_expiry',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='tokens_balance',
        ),
        migrations.AlterField(
            model_name='teamportfolio',
            name='projects',
            field=models.TextField(default='FUNMIG|شبکه اجتماعی، وبلاگ، چت و ابزارهای ارتباطی در یک محصول\nپنل مدیریت فان میگ|مدیریت کاربران، محتوا، پرداخت، بنرها، اعلامیه ها و پشتیبانی\nسیستم محتوای دیجیتال|تولید، مدیریت و انتشار محتوای متنی و رسانه ای', verbose_name='نمونه کارها (هر خط: عنوان|توضیح)'),
        ),
        migrations.AlterField(
            model_name='teamportfolio',
            name='services',
            field=models.TextField(default='طراحی و توسعه وب اپلیکیشن|ساخت پنل های مدیریتی، شبکه اجتماعی، مارکت پلیس و ابزارهای اختصاصی\nاتوماسیون و ابزارهای دیجیتال|طراحی فرایندهای سریع، داشبوردهای عملیاتی و ابزارهای اختصاصی\nطراحی تجربه کاربری|طراحی مسیر کاربر، رابط کاربری، هویت بصری و بهینه سازی نرخ تبدیل\nزیرساخت و نگهداری|استقرار، مانیتورینگ، امنیت، بهینه سازی سرعت و پشتیبانی فنی', verbose_name='خدمات (هر خط: عنوان|توضیح)'),
        ),
        migrations.AlterField(
            model_name='teamportfolio',
            name='stats',
            field=models.TextField(default='24/7|پشتیبانی\n+10|ماژول محصولی\nUX|تمرکز روی تجربه کاربر\nPWA|آماده نصب روی موبایل', verbose_name='آمار (هر خط: عدد|عنوان)'),
        ),
        migrations.AlterField(
            model_name='teamportfolio',
            name='subtitle',
            field=models.CharField(default='طراحی، توسعه و رشد محصول دیجیتال با تمرکز روی تجربه اجتماعی و ابزارهای کاربردی', max_length=220, verbose_name='زیرعنوان'),
        ),
        migrations.AlterField(
            model_name='teamportfolio',
            name='tools',
            field=models.TextField(default='Django\nChannels\nNginx\nNSSM\nSQLite/PostgreSQL\nPWA\nHTML/CSS/JavaScript', verbose_name='تکنولوژی ها (هر خط یک مورد)'),
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.DeleteModel(
            name='ChatSession',
        ),
        migrations.DeleteModel(
            name='PaymentRequest',
        ),
    ]
