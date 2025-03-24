from django.db import models

# ------------------------- Car Model ------------------------- #
class Car(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    for_sale = models.BooleanField()

    class Meta:
        db_table = "car"
        ordering = ["-year"]
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# ------------------------- Customer Model ------------------------- #
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    class Meta:
        db_table = "customer"
        ordering = ["last_name", "first_name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()

# ------------------------- Salesperson Model ------------------------- #
class Salesperson(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        db_table = "salesperson"
        ordering = ["last_name"]
        verbose_name = "Salesperson"
        verbose_name_plural = "Salespeople"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()

# ------------------------- Invoice Model ------------------------- #
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)

    class Meta:
        db_table = "invoice"
        ordering = ["-date"]
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.date}"

# ------------------------- Mechanic Model ------------------------- #
class Mechanic(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        db_table = "mechanic"
        ordering = ["last_name"]
        verbose_name = "Mechanic"
        verbose_name_plural = "Mechanics"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()

# ------------------------- Service Model ------------------------- #
class Service(models.Model):
    service_name = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "service"
        ordering = ["service_name"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.service_name

# ------------------------- Service Ticket Model ------------------------- #
class ServiceTicket(models.Model):
    service_ticket_number = models.CharField(max_length=100, unique=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_received = models.DateField()
    comments = models.TextField(blank=True, null=True)
    date_returned = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "service_ticket"
        ordering = ["-date_received"]
        verbose_name = "Service Ticket"
        verbose_name_plural = "Service Tickets"

    def __str__(self):
        return f"Ticket {self.service_ticket_number}"

# ------------------------- Service Mechanic Model ------------------------- #
class ServiceMechanic(models.Model):
    service_ticket = models.ForeignKey(ServiceTicket, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "service_mechanic"
        ordering = ["service_ticket"]
        verbose_name = "Service Mechanic"
        verbose_name_plural = "Service Mechanics"

    def __str__(self):
        return f"{self.mechanic} - {self.service_ticket}"

# ------------------------- Parts Model ------------------------- #
class Parts(models.Model):
    part_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "parts"
        ordering = ["part_number"]
        verbose_name = "Part"
        verbose_name_plural = "Parts"

    def __str__(self):
        return f"Part {self.part_number}: {self.description}"

# ------------------------- Parts Used Model ------------------------- #
class PartsUsed(models.Model):
    part = models.ForeignKey(Parts, on_delete=models.CASCADE)
    service_ticket = models.ForeignKey(ServiceTicket, on_delete=models.CASCADE)
    number_used = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "parts_used"
        ordering = ["service_ticket"]
        verbose_name = "Parts Used"
        verbose_name_plural = "Parts Used"

    def __str__(self):
        return f"{self.number_used} x {self.part} in {self.service_ticket}"
