from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from jinja2 import Template
from linkml_runtime.utils.schemaview import SchemaView
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum
from linkml.generators.pythongen import PythonGenerator

class SQLAlchemySchemaView(SchemaView):
    def class_slots(self, class_name, imports=True):
        slots = super().class_slots(class_name, imports=imports)

        return [
            slot_name
            for slot_name in slots
            if not self.get_slot(slot_name).annotations.get("computed")
        ]

class ComputedSQLAlchemyGenerator(SQLAlchemyGenerator):
    def __post_init__(self):
        # Don't let SQLAlchemyGenerator replace our SchemaView.
        super().__post_init__()
        self.schemaview = SQLAlchemySchemaView(self.schema)

@dataclass
class SchemaItem:
    class_name: str
    api_resource_name: Optional[str]

def _template(template_file: str) -> Template:
    template_path = Path(__file__).parent / "templates" / f"{template_file}.jinja2"
    template_str = template_path.read_text()
    return Template(template_str)

def _render_sql_alchemy(schema_path: Path):
    schemaview = SQLAlchemySchemaView(schema_path)

    generator = ComputedSQLAlchemyGenerator(
        schema_path,
        schemaview=schemaview,
    )

    with open("bookstore/generated/entity.py", "w") as f:
        f.write(generator.generate_sqla(template=TemplateEnum.DECLARATIVE_2X))

def _render_entity(schema_path: Path):
    generator = PythonGenerator(schema_path)
    output_path = Path("bookstore/generated/model.py")

    output_path.write_text(generator.serialize())

def render(schema_path: Path):
    schema_view = SchemaView(schema_path)
    _render_sql_alchemy(schema_path=schema_path)
    _render_entity(schema_path=schema_path)
    schema_items = []
    for class_name, class_obj in schema_view.all_classes().items():
        api_resource_name = (
            None if "api_resource_name" not in class_obj.annotations.keys() 
            else class_obj.annotations["api_resource_name"].value
        )
        schema_items.append(SchemaItem(
            class_name=class_name,
            api_resource_name=api_resource_name,
        ))
    template = _template("schema")
    with open("bookstore/generated/schema.py", "w") as f:
        f.write(template.render(
            import_path="bookstore.generated",
            classes=schema_items
        ))
    

if __name__ == "__main__":
    schema_path = Path(__file__).parent.parent / "schema" / "bookstore.yaml"
    render(schema_path=schema_path)
