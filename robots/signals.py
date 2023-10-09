from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.core.mail import send_mail
from R4C import settings
from orders.models import Order
from robots.models import Robot

robot_available = Signal()


@receiver(post_save, sender=Robot)
def notify_customers(sender, instance, created, **kwargs):
    if created:
        robot_available.send(sender=instance.__class__, robot_serial=instance.serial)


@receiver(robot_available)
def handle_robot_available(sender, **kwargs):
    robot_serial = kwargs.get('robot_serial')
    # Обработка доступности робота и отправка уведомления клиентам
    waiting_orders = Order.objects.filter(robot_serial=robot_serial)
    for order in waiting_orders:
        customer_email = order.customer.email  # Получаем email клиента
        robot_model = order.robot_serial.split('-')[0]  # Получаем модель робота
        robot_version = order.robot_serial.split('-')[1]  # Получаем версию робота
        print(robot_model, robot_version)
        # Формируем сообщение
        message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {robot_model}, версии" \
                  f" {robot_version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант" \
                  f" - пожалуйста, свяжитесь с нами"
        # Отправляем письмо
        send_mail('Робот доступен в наличии', message, settings.EMAIL_HOST_USER, [customer_email])

