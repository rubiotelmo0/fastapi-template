# Template Docs

This folder contains starter documentation assets for the template:

- `bruno_collection/`: example Bruno requests for the sample `items` CRUD endpoints plus the derived `items/summary` endpoint.
- `uml/architecture.puml`: a small PlantUML diagram showing routers calling CRUD directly and reserving `business_logic/` for higher-level workflows.

When you replace the sample `Item` entity with your own domain, update these files so the docs stay aligned with the code and the intended layer responsibilities.
