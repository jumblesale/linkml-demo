from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from jinja2 import Template
from linkml_runtime.utils.schemaview import ClassDefinition, ClassDefinitionName, SchemaView, SlotDefinition
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum
from linkml.generators.pythongen import PythonGenerator


@dataclass
class SchemaItem:
    class_name: str
    api_resource_name: Optional[str]
    has_write_model: bool
    has_read_model: bool


def _template(template_file: str) -> Template:
    template_path = Path(__file__).parent / "templates" / f"{template_file}.jinja2"
    template_str = template_path.read_text()
    return Template(template_str)

def _render_sql_alchemy(schema_path: Path):
    generator = SQLAlchemyGenerator(schema=schema_path)

    Path("bookstore/generated/entity.py").write_text(
        generator.generate_sqla(template=TemplateEnum.DECLARATIVE_2X)
    )

def _render_model(schema_path: Path):
    generator = PythonGenerator(schema_path)
    Path("bookstore/generated/domain.py").write_text(generator.serialize())

@dataclass
class DTOSlot:
    name: str
    python_type: str
    required: bool


@dataclass
class DTO:
    name: str
    write_slots: list[DTOSlot]
    read_slots: list[DTOSlot]

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
        if slot.range in class_names or slot.range in enum_names:
            base_type = "str"
        else:
            range_name = python_generator._roll_up_type(slot.range)
            base_type = primitive_types.get(range_name, "str")

        if slot.multivalued:
            base_type = f"list[{base_type}]"
        if not slot.required:
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
                required=slot.required is True,
            ))
        return dto_slots

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
            write_slots=write_slots,
            read_slots=read_slots,
        ))
    template = _template("dto")
    Path("bookstore/generated/dto.py").write_text(template.render(
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
    _render_model(schema_path=schema_path)
    _render_dtos(schema_view=schema_view)
    api_class_names = {
        class_name
        for class_name, _ in _api_schema_classes(schema_view=schema_view)
    }
    schema_items = []
    for class_name, class_definition in _schema_classes(schema_view=schema_view):
        api_resource_name = (
            None if "api_resource_name" not in class_definition.annotations.keys() 
            else class_definition.annotations["api_resource_name"].value
        )
        schema_items.append(SchemaItem(
            class_name=class_name,
            api_resource_name=api_resource_name,
            has_write_model=class_name in api_class_names,
            has_read_model=class_name in api_class_names,
        ))
    template = _template("schema")
    Path("bookstore/generated/schema.py").write_text(
        template.render(
            import_path="bookstore.generated",
            classes=schema_items
        ))
    

if __name__ == "__main__":
    schema_path = Path(__file__).parent.parent / "schema" / "bookstore.yaml"
    render(schema_path=schema_path)
