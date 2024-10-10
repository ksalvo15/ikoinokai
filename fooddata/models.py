from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Receipt(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class DataRecord(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    day = models.CharField(max_length=255, null=True, blank=True)
    lunch_item = models.CharField(max_length=255, null=True, blank=True)
    total_paying_people = models.IntegerField(null=True, blank=True)
    senior_people = models.IntegerField(null=True, blank=True)
    non_seniors = models.IntegerField(null=True, blank=True)
    children_people = models.IntegerField(null=True, blank=True)
    eleven_scripts = models.IntegerField(null=True, blank=True)
    nine_scripts = models.IntegerField(null=True, blank=True)
    eight_scripts = models.IntegerField(null=True, blank=True)
    six_scripts = models.IntegerField(null=True, blank=True)
    person_free_bday = models.IntegerField(null=True, blank=True)
    nine_lunch_sale = models.IntegerField(null=True, blank=True)
    lunch_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volunteer_people = models.IntegerField(null=True, blank=True)
    total_people = models.IntegerField(null=True, blank=True)
    amount_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    money_collected = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    script_money_collected = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    diff = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    script_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #protein = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.date} - {self.day} - {self.lunch_item} - {self.total_paying_people} - {self.senior_people} - {self.non_seniors} - {self.children_people} - {self.eleven_scripts} - {self.nine_scripts} - {self.eight_scripts} - {self.six_scripts} - {self.person_free_bday} - {self.nine_lunch_sale} - {self.lunch_sale} - {self.volunteer_people} - {self.total_people} - {self.amount_cost} - {self.money_collected} - {self.script_money_collected} - {self.diff} - {self.script_sale}'# - {self.protein}'


    #document = models.ForeignKey(Document, on_delete=models.CASCADE)
    #date = models.IntegerField(null=True, blank=True)
    #data = models.IntegerField(null=True, blank=True)
    #other_stuff = models.CharField(max_length=255, null=True, blank=True)

    def get_date(self):
        # Convert serial date to Python datetime
        return excel_serial_to_datetime(self.date)
    

    #def __str__(self):
    #    return f'{self.get_date()} - {self.data} - {self.other_stuff}'

