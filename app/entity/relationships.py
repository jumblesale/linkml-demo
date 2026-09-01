from bookstore.generated.schema import (
    RelationshipMetadata,
    SchemaClassAddressable,
)


def reverse_relationships_for(
    schema_class: type[SchemaClassAddressable],
) -> list[tuple[type[SchemaClassAddressable], str, str]]:
    """
    For a given schema class, find all reverse relationships.
    Returns tuples of (source_class, forward_ref_name, reverse_field_name).
    
    Example: For Author, returns (Book, "author", "books_published")
    meaning Book.author points to Author, and Author.books_published is the reverse.
    """
    result = []
    for candidate in SchemaClassAddressable.__subclasses__():
        for forward_name, metadata in candidate.relationships.items():
            if metadata.target_class_name != schema_class.__name__:
                continue
            # Find the reverse relationship name on the target schema class
            reverse_name = next(
                (
                    name
                    for name, rel_meta in schema_class.relationships.items()
                    if rel_meta.target_class_name == candidate.__name__
                ),
                None,
            )
            if reverse_name:
                result.append((candidate, forward_name, reverse_name))
    return result
