from django.db import models


class ProcedureCode(models.Model):
    procedure_code_category = models.CharField(max_length=100)
    cpt_codes = models.CharField(max_length=100)
    procedure_code_descriptions = models.TextField()
    code_status = models.CharField(max_length=50)
    operative_procedure = models.TextField()
    procedure_description = models.TextField()

    def __str__(self):
        return f"{self.procedure_code_category} - {self.cpt_codes}"
