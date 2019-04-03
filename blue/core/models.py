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


class Item(models.Model):
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
    A model used to store user's statistics as a formula
    such as a sum of counters
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    formula = models.TextField()
    description = models.CharField(max_length=256)
    note = models.TextField(default=None, blank=True)

    def result(self):
        """
        This method is used to calculate the result of a formula
        a formula can contain a sum of Items or Statistics
        """
        formula_register_ids = self.parse_formula().get("register_ids")
        formula_statistics_ids = self.parse_formula().get("statistics_ids")
        return calculate_statistics(formula_register_ids, formula_statistics_ids)

    def parse_formula(self):
        """
        here we return a list of ids of Registers
        and a list of ids of Statistics starting from the formula
        """
        splitted = self.formula.split(";")
        if len(splitted) == 2:
            return {"register_ids": splitted[0].split(","), "statistics_ids": splitted[1].split(",")}
        return {"register_ids": splitted[0].split(","), "statistics_ids": []}

    def __str__(self):
        return self.description


def calculate_register_amount(register_id):
    """
    A function to calculate the sum of a Register's child Items
    """
    return Item.objects.filter(register=register_id).aggregate(Sum('amount')).get("amount__sum")


def calculate_registers_sum(ids):
    """
    A function used to calculate a sum of Register totals
    """
    sum = 0
    for element in ids:
        sum += calculate_register_amount(element)
    return sum


def calculate_statistics(register_ids, statistics_ids, total=0):
    """
    This function is used to calculate a single Statistics result
    """
    total += calculate_registers_sum(register_ids)
    for element in statistics_ids:
        formula_register_ids = Statistics.objects.filter(id=element).first().parse_formula().get("register_ids")
        formula_statistics_ids = Statistics.objects.filter(id=element).first().parse_formula().get("statistics_ids")
        total += calculate_statistics(formula_register_ids, formula_statistics_ids, total)
    return total
