from rest_framework import serializers
from .models import ProcedureCode


class ProcedureCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureCode
        fields = "__all__"

    # Custom validation logic to prevent updates
    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            "Editing existing procedure codes is not allowed."
        )

    # Optional validation for new entries
    def validate(self, data):
        if self.instance:
            raise serializers.ValidationError(
                "Modifying existing records is forbidden."
            )

        # Add any custom validation rules here for new data if needed
        if ProcedureCode.objects.filter(cpt_codes=data.get("cpt_codes")).exists():
            raise serializers.ValidationError(
                "A procedure with this CPT code already exists."
            )

        # Check for empty fields (if necessary)
        required_fields = [
            "procedure_code_category",
            "cpt_codes",
            "procedure_code_descriptions",
            "code_status",
            "operative_procedure",
            "procedure_description",
        ]
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(
                    f"{field.replace('_', ' ').capitalize()} is required and cannot be empty."
                )

        return data
