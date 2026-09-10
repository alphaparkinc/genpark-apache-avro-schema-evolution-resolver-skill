from client import AvroSchemaResolver

def main():
    print("=== Testing Apache Avro Schema Evolution Resolver ===")
    avro = AvroSchemaResolver()
    writer_s = {"fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]}
    reader_s = {"fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}, {"name": "active", "type": "int", "default": 1}]}

    bin_data = avro.encode(writer_s, {"id": 10, "name": "Alice"})
    rec = avro.decode_with_schema_evolution(writer_s, reader_s, bin_data)
    print("Resolved Record under evolved schema:", rec)

    assert rec["id"] == 10 and rec["name"] == "Alice" and rec["active"] == 1
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
