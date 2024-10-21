from rest_framework import serializers
from .models import ProcedureCode


class ProcedureCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureCode
        fields = "__all__"
        read_only_fields = [
            "procedure_code_category",
            "cpt_codes",
            "procedure_code_descriptions",
            "code_status",
            "operative_procedure",
            "procedure_description",
        ]

    # Custom validation logic to prevent updates
    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            "Editing existing procedure codes is not allowed."
        )

    # Ensure procedure_code_category is uppercase
    def validate_procedure_code_category(self, value):
        if not value.isupper():
            raise serializers.ValidationError(
                "Procedure code category must be in uppercase."
            )
        return value

    # Optional validation for new entries
    def validate(self, data):
        # Ensure no fields are empty for POST requests
        required_fields = [
            "procedure_code_category",
            "cpt_codes",
            "procedure_code_descriptions",
            "code_status",
            "operative_procedure",
            "procedure_description",
        ]

        for field in required_fields:
            if not data.get(field):  # Check if any required field is missing or empty
                raise serializers.ValidationError(
                    f"{field.replace('_', ' ').capitalize()} is required and cannot be empty."
                )

        # Check if the procedure already exists based on CPT code
        if ProcedureCode.objects.filter(cpt_codes=data.get("cpt_codes")).exists():
            raise serializers.ValidationError(
                "A procedure with this CPT code already exists."
            )

        return data
