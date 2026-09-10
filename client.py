class AvroSchemaResolver:
    """
    Apache Avro Binary Encoder and Schema Evolution Engine.
    Resolves differences between writer and reader schemas dynamically.
    """
    def encode(self, schema, record):
        buf = bytearray()
        for field in schema["fields"]:
            fname = field["name"]
            val = record.get(fname, field.get("default"))
            ftype = field["type"]
            if ftype == "int":
                buf.extend(int(val).to_bytes(4, "little"))
            elif ftype == "string":
                encoded = val.encode("utf-8")
                buf.extend(len(encoded).to_bytes(2, "little") + encoded)
        return bytes(buf)

    def decode_with_schema_evolution(self, writer_schema, reader_schema, data):
        offset = 0
        writer_data = {}
        for field in writer_schema["fields"]:
            fname = field["name"]
            ftype = field["type"]
            if ftype == "int":
                val = int.from_bytes(data[offset:offset+4], "little")
                offset += 4
            elif ftype == "string":
                slen = int.from_bytes(data[offset:offset+2], "little")
                offset += 2
                val = data[offset:offset+slen].decode("utf-8")
                offset += slen
            writer_data[fname] = val

        result = {}
        for r_field in reader_schema["fields"]:
            rf_name = r_field["name"]
            if rf_name in writer_data:
                result[rf_name] = writer_data[rf_name]
            else:
                result[rf_name] = r_field.get("default")
        return result
