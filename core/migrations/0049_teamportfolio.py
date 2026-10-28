

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0048_blogmedia'),
    ]


    operations = [
        migrations.CreateModel(
            name='TeamPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='تیم فان میگ', max_length=120, verbose_name='عنوان اصلی')),
                ('subtitle', models.CharField(default='طراحی، توسعه و رشد محصول دیجیتال با تمرکز روی تجربه اجتماعی و هوش مصنوعی', max_length=220, verbose_name='زیرعنوان')),
                ('intro', models.TextField(default='ما تیم فان میگ هستیم؛ یک تیم محصول محور که از ایده تا طراحی، توسعه، انتشار و پشتیبانی کنار کسب و کارها می ایستد.', verbose_name='معرفی کوتاه')),
                ('mission', models.TextField(default='ماموریت ما ساخت تجربه هایی است که ساده، سریع، امن و برای کاربران واقعی دوست داشتنی باشند.', verbose_name='ماموریت')),
                ('services', models.TextField(default='طراحی و توسعه وب اپلیکیشن|ساخت پنل های مدیریتی، شبکه اجتماعی، مارکت پلیس و ابزارهای اختصاصی\nهوش مصنوعی و اتوماسیون|اتصال مدل های AI به فرایندهای واقعی، چت بات، تولید محتوا و ابزارهای هوشمند\nطراحی تجربه کاربری|طراحی مسیر کاربر، رابط کاربری، هویت بصری و بهینه سازی نرخ تبدیل\nزیرساخت و نگهداری|استقرار، مانیتورینگ، امنیت، بهینه سازی سرعت و پشتیبانی فنی', verbose_name='خدمات (هر خط: عنوان|توضیح)')),
                ('stats', models.TextField(default='24/7|پشتیبانی\n+10|ماژول محصولی\nAI|یکپارچه با هوش مصنوعی\nPWA|آماده نصب روی موبایل', verbose_name='آمار (هر خط: عدد|عنوان)')),
                ('team_members', models.TextField(default='مدیریت محصول|استراتژی، نقشه راه و هماهنگی تیم\nتوسعه بک اند|Django، API، امنیت و دیتابیس\nتوسعه فرانت اند|رابط کاربری، ریسپانسیو و تجربه سریع\nطراحی و محتوا|هویت بصری، متن محصول و ارتباط با کاربر', verbose_name='اعضای تیم (هر خط: نقش|توضیح)')),
                ('projects', models.TextField(default='FUNMIG|شبکه اجتماعی، وبلاگ، چت و دستیار هوش مصنوعی در یک محصول\nپنل مدیریت فان میگ|مدیریت کاربران، محتوا، پرداخت، بنرها، اعلامیه ها و پشتیبانی\nسیستم محتوای هوشمند|تولید، مدیریت و انتشار محتوای متنی و رسانه ای', verbose_name='نمونه کارها (هر خط: عنوان|توضیح)')),
                ('tools', models.TextField(default='Django\nChannels\nNginx\nNSSM\nSQLite/PostgreSQL\nOpenAI Compatible APIs\nPWA\nHTML/CSS/JavaScript', verbose_name='تکنولوژی ها (هر خط یک مورد)')),
                ('process', models.TextField(default='شناخت نیاز|بررسی هدف، مخاطب، محدودیت ها و اولویت های محصول\nطراحی راه حل|ساخت ساختار، وایرفریم، UI و معماری فنی\nتوسعه و تست|پیاده سازی مرحله ای، تست، بازبینی و آماده سازی انتشار\nاستقرار و رشد|دیپلوی، مانیتورینگ، بهبود سرعت و اضافه کردن قابلیت های بعدی', verbose_name='فرایند همکاری (هر خط: عنوان|توضیح)')),
                ('cta_title', models.CharField(default='آماده ایم محصول بعدی را با شما بسازیم', max_length=160, verbose_name='عنوان دعوت به اقدام')),
                ('cta_text', models.TextField(default='برای همکاری، مشاوره یا توسعه یک محصول اختصاصی با تیم فان میگ در ارتباط باشید.', verbose_name='متن دعوت به اقدام')),
                ('phone', models.CharField(default='+989981502665', max_length=40, verbose_name='شماره تماس')),
                ('telegram_url', models.URLField(default='https://t.me/FUNMIGweb', max_length=255, verbose_name='لینک تلگرام')),
                ('email', models.EmailField(default='admin@funmig.com', max_length=254, verbose_name='ایمیل')),
                ('address', models.CharField(default='مشهد، امامت ۱۸، پلاک ۱۲۶', max_length=255, verbose_name='آدرس')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
            ],
            options={
                'verbose_name': 'پروفایلوی تیم فان میگ',
                'verbose_name_plural': 'پروفایلوی تیم فان میگ',
            },
        ),
    ]

