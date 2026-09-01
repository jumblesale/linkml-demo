from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from jinja2 import Template
from linkml_runtime.utils.schemaview import ClassDefinition, ClassDefinitionName, SchemaView, SlotDefinition
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum
from linkml.generators.pythongen import PythonGenerator


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
MODULE_NAME = "bookstore"
MODULE_PATH = REPOSITORY_ROOT / MODULE_NAME


@dataclass
class SchemaItem:
    class_name: str
    api_resource_name: Optional[str]
    is_addressable: bool
    relationships: list["RelationshipItem"]


@dataclass
class RelationshipItem:
    name: str
    target_class_name: str
    multivalued: bool
    minimum_cardinality: int | None


def _template(template_file: str) -> Template:
    template_path = Path(__file__).parent / "templates" / f"{template_file}.jinja2"
    template_str = template_path.read_text()
    return Template(template_str)

def _render_sql_alchemy(schema_path: Path):
    generator = SQLAlchemyGenerator(schema=schema_path)
    (MODULE_PATH / "generated/entity.py").write_text(
        generator.generate_sqla(template=TemplateEnum.DECLARATIVE)
    )


@dataclass
class UniqueKeyItem:
    name: str
    slot_names: list[str]


@dataclass
class ConstraintItem:
    class_name: str
    unique_keys: list[UniqueKeyItem]


def _render_constraints(schema_view: SchemaView):
    constraints = []
    for class_name, class_definition in _schema_classes(schema_view):
        if not class_definition.unique_keys:
            continue
        unique_keys = [
            UniqueKeyItem(
                name=f"uq_{class_name.lower()}_{key_name}",
                slot_names=list(unique_key.unique_key_slots),
            )
            for key_name, unique_key in class_definition.unique_keys.items()
        ]
        constraints.append(ConstraintItem(
            class_name=class_name,
            unique_keys=unique_keys,
        ))
    template = _template("constraints")
    (MODULE_PATH / "generated/constraints.py").write_text(template.render(
        import_path=f"{MODULE_PATH.name}.generated",
        constraints=constraints,
    ))

def _render_model(schema_path: Path):
    generator = PythonGenerator(schema_path)
    (MODULE_PATH / "generated/domain.py").write_text(generator.serialize())

@dataclass
class DTOSlot:
    name: str
    python_type: str
    required: bool


@dataclass
class DTOModel:
    name: Literal["Read", "Create"]
    slots: list[DTOSlot]


@dataclass
class DTO:
    name: str
    models: list[DTOModel]

def _render_dtos(schema_view: SchemaView):
    python_generator = PythonGenerator(schema_view.schema)
    class_names = schema_view.all_classes().keys()
    enum_names = schema_view.all_enums().keys()

    primitive_types = {
        "boolean": "bool",
        "decimal": "float",
        "double": "float",
        "float": "float",
        "integer": "int",
        "date": "date",
        "datetime": "datetime",
        "string": "str",
        "uri": "str",
        "uriorcurie": "str",
    }

    def _python_type(slot: SlotDefinition) -> str:
        match slot.range:
            case range_name if range_name in enum_names:
                enum_definition = schema_view.get_enum(range_name)
                values = ", ".join(
                    repr(value)
                    for value in enum_definition.permissible_values.keys()
                )
                base_type = f"Literal[{values}]"
            case range_name if range_name in class_names:
                base_type = "str"
            case range_name:
                range_name = python_generator._roll_up_type(range_name)
                base_type = primitive_types.get(range_name, "str")

        if slot.multivalued:
            base_type = f"list[{base_type}]"
        if not slot.required and (slot.minimum_cardinality or 0) < 1:
            base_type = f"{base_type} | None"
        return base_type

    def _slots_with_annotation(
        class_definition: ClassDefinition,
        annotation: str,
    ) -> list[DTOSlot]:
        dto_slots = []
        for slot_name in schema_view.class_slots(class_definition.name):
            slot = schema_view.get_slot(slot_name)
            if slot is None or slot.annotations is None:
                continue
            annotation_value = slot.annotations.get(annotation)
            if annotation_value is None or annotation_value.value is not True:
                continue

            dto_slots.append(DTOSlot(
                name=slot.name,
                python_type=_python_type(slot),
                required=(
                    slot.required is True
                    or (slot.minimum_cardinality or 0) > 0
                ),
            ))
        return sorted(dto_slots, key=lambda slot: not slot.required)

    dtos = []
    for class_name, class_definition in _api_schema_classes(schema_view=schema_view):
        write_slots = _slots_with_annotation(
            class_definition=class_definition,
            annotation="write_model"
        )
        read_slots = _slots_with_annotation(
            class_definition=class_definition,
            annotation="read_model"
        )
        dtos.append(DTO(
            name=class_name,
            models=[
                DTOModel(name="Create", slots=write_slots),
                DTOModel(name="Read", slots=read_slots),
            ],
        ))
    template = _template("dto")
    (MODULE_PATH / "generated/dto.py").write_text(template.render(
        dtos=dtos
    ))


def _schema_classes(
    schema_view: SchemaView
) -> list[tuple[ClassDefinitionName, ClassDefinition]]:
    return schema_view.all_classes().items()


def _api_schema_classes(
    schema_view: SchemaView,
) -> list[tuple[ClassDefinitionName, ClassDefinition]]:
    return [
        (class_name, class_definition)
        for class_name, class_definition in _schema_classes(schema_view)
        if class_definition.annotations
        and class_definition.annotations.get("api_resource_name")
    ]


def render(schema_path: Path):
    schema_view = SchemaView(schema_path)
    _render_sql_alchemy(schema_path=schema_path)
    _render_constraints(schema_view=schema_view)
    _render_model(schema_path=schema_path)
    _render_dtos(schema_view=schema_view)
    api_class_names = {
        class_name
        for class_name, _ in _api_schema_classes(schema_view=schema_view)
    }
    schema_items = []
    class_names = {str(class_name) for class_name, _ in _schema_classes(schema_view)}
    for class_name, class_definition in _schema_classes(schema_view=schema_view):
        api_resource_name = (
            None if "api_resource_name" not in class_definition.annotations.keys() 
            else class_definition.annotations["api_resource_name"].value
        )
        relationships = []
        for slot_name in schema_view.class_slots(class_name):
            slot = schema_view.get_slot(slot_name)
            if slot is None or str(slot.range) not in class_names:
                continue
            relationships.append(RelationshipItem(
                name=slot.name,
                target_class_name=str(slot.range),
                multivalued=slot.multivalued is True,
                minimum_cardinality=slot.minimum_cardinality,
            ))
        schema_items.append(SchemaItem(
            class_name=class_name,
            api_resource_name=api_resource_name,
            is_addressable=class_name in api_class_names,
            relationships=relationships,
        ))
    template = _template("schema")
    (MODULE_PATH / "generated/schema.py").write_text(
        template.render(
            import_path=f"{MODULE_PATH.name}.generated",
            classes=schema_items,
        ))
    

if __name__ == "__main__":
    schema_path = REPOSITORY_ROOT / "schema" / f"{MODULE_PATH.name}.yaml"
    render(schema_path=schema_path)
