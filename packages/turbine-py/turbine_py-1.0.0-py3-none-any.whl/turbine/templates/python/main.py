import hashlib
import sys
import typing as t
import json

from turbine.runtime import Record, Runtime


def anonymize(records: t.List[Record]) -> t.List[Record]:
    updated = []
    for record in records:
        try:
            record_value_from_json = json.loads(record.value)
            hashed_email = hashlib.sha256(
                record_value_from_json["payload"]["customer_email"].encode("utf-8")
            ).hexdigest()
            record_value_from_json["payload"]["customer_email"] = hashed_email
            updated.append(
                Record(
                    key=record.key,
                    value=record_value_from_json,
                    timestamp=record.timestamp,
                )
            )
        except Exception as e:
            print("Error occurred while parsing records: " + str(e))
            updated.append(
                Record(
                    key=record.key,
                    value=record_value_from_json,
                    timestamp=record.timestamp,
                )
            )
    return updated


class App:
    @staticmethod
    async def run(turbine: Runtime):
        try:
            # To configure your data stores as resources on the Meroxa Platform
            # use the Meroxa Dashboard, CLI, or Meroxa Terraform Provider.
            # For more details refer to: https://docs.meroxa.com/

            # Identify an upstream data store for your data app
            # with the `resources` function.
            # Replace `source_name` with the resource name the
            # data store was configured with on Meroxa.
            source = await turbine.resources("source_name")

            # Specify which upstream records to pull
            # with the `records` function.
            # Replace `collection_name` with a table, collection,
            # or bucket name in your data store.
            records = await source.records("collection_name")

            # Specify which secrets in environment variables should be passed
            # into the Process.
            # Replace 'PWD' with the name of the environment variable.
            secrets = turbine.register_secrets("PWD")

            # Specify what code to execute against upstream records
            # with the `process` function.
            # Replace `anonymize` with the name of your function code.
            anonymized = await turbine.process(records, anonymize, secrets)

            # Identify a downstream data store for your data app
            # with the `resources` function.
            # Replace `destination_name` with the resource name the
            # data store was configured with on Meroxa.
            destination_db = await turbine.resources("destination_name")

            # Specify where to write records downstream
            # using the `write` function.
            # Replace `collection_archive` with a table, collection,
            # or bucket name in your data store.
            # If you need additional connector configurations, replace '{}'
            # with the key and value, i.e. {"incrementing.field.name":"id"}
            await destination_db.write(anonymized, "collection_archive", {})
        except Exception as e:
            print(e, file=sys.stderr)
