from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('restaurant', '0003_remove_booking_comment_remove_booking_guest_number_and_more')]
    operations = [migrations.AddConstraint(model_name='booking', constraint=models.UniqueConstraint(fields=('reservation_date', 'reservation_slot'), name='unique_booking_date_slot'))]
