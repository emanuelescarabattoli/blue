from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Register(models.Model):
    """
    This model represent a header of a list of accounting rows
    with some metadata such as title and note
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    note = models.TextField(default=None, blank=True)

    def __str__(self):
        return self.description


class RegisterRow(models.Model):
    """
    This model is used to register an accounting row
    linked to a register
    """

    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=256)
    period = models.CharField(max_length=256, default=None, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(default=None, blank=True)

    def __str__(self):
        return self.description


class Statistics(models.Model):
    """
    A model used to store user's statistics
    a statistics is made by a list of registers and a list of other formulas
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    note = models.TextField(default=None, blank=True)

    def __str__(self):
        return self.description


class StatisticsRowRegister(models.Model):
    """
    A model used to store a statistics row
    linked to a register
    """

    parent_statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.parent_statistics.description} - {self.register.description}"


class StatisticsRowStatistics(models.Model):
    """
    A model used to store a statistics row
    linked to a statistics
    """

    parent_statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE)
    statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE, related_name="child_statistics")

    def __str__(self):
        return f"{self.parent_statistics.description} - {self.statistics.description}"


def calculate_statistics_result(statistics_id):
    """
    This method is used to calculate the result of a statistics
    """
    register_ids = StatisticsRowRegister.objects.filter(parent_statistics=statistics_id).values_list("register__id", flat=True)
    statistics_ids = StatisticsRowStatistics.objects.filter(parent_statistics=statistics_id).values_list("statistics__id", flat=True)
    return calculate_statistics(register_ids, statistics_ids)


def calculate_register_amount(register_id):
    """
    A function to calculate the sum of a register's rows
    """
    return RegisterRow.objects.filter(register=register_id).aggregate(Sum("amount")).get("amount__sum")


def calculate_registers_sum(register_ids):
    """
    A function used to calculate a sum of register totals
    """
    sum = 0
    for register_id in register_ids:
        amount = calculate_register_amount(register_id)
        if amount is None:
            amount = 0
        sum += amount
    return sum


def calculate_statistics(register_ids, statistics_ids, total=0):
    """
    This function is used to calculate a single statistics result
    """
    for statistics_id in statistics_ids:
        child_register_ids = StatisticsRowRegister.objects.filter(parent_statistics=statistics_id).values_list("register", flat=True)
        child_statistics_ids = StatisticsRowStatistics.objects.filter(parent_statistics=statistics_id).values_list("statistics", flat=True)
        total += calculate_statistics(child_register_ids, child_statistics_ids, total)
    return total + calculate_registers_sum(register_ids)
