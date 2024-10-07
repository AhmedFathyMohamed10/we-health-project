import json
from django.core.management.base import BaseCommand
from mic_api.models import ProcedureCode  # Import your model
from django.db import transaction


class Command(BaseCommand):
    help = "Imports procedures from a JSON file into the PostgreSQL database"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Path to the JSON file to be imported"
        )

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]

        # Load the JSON data
        with open(json_file, "r") as file:
            data = json.load(file)

        # Import the data into the database
        try:
            with transaction.atomic():
                for entry in data:
                    ProcedureCode.objects.create(
                        procedure_code_category=entry.get(
                            "Procedure_Code_Category", ""
                        ),
                        cpt_codes=entry.get("CPT_Codes", 0),
                        procedure_code_descriptions=entry.get(
                            "Procedure_Code_Descriptions", ""
                        ),
                        code_status=entry.get("Code_Status", ""),
                        operative_procedure=entry.get("Operative_Procedure", ""),
                        procedure_description=entry.get("Procedure_Description", ""),
                    )
            self.stdout.write(
                self.style.SUCCESS("Successfully imported data into PostgreSQL")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
