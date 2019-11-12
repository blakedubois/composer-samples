import uuid
import random

with open("records.tsv", "w") as f:
    for x in range(0, 10000):
        r = random.choices([
            "Foo",
            "Bar",
            "Bazz",
            "Ran",
            "Xxy"
        ])

        price = random.choices([
            10000, 20000, 25000, 40000
        ])

        f.write(f"{uuid.uuid4()},{x},{r[0]},{price[0]}")
        f.write("\n")
