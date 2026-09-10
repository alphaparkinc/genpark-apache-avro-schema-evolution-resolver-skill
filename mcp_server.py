import sys
import json
import base64
from client import AvroSchemaResolver

def main():
    avro = AvroSchemaResolver()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "encode":
            b = avro.encode(params.get("schema", {}), params.get("record", {}))
            res = {"bytes_b64": base64.b64encode(b).decode()}
        elif method == "decode":
            raw = base64.b64decode(params.get("bytes_b64", "").encode())
            rec = avro.decode_with_schema_evolution(params.get("writer_schema"), params.get("reader_schema"), raw)
            res = {"record": rec}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
