### build sdk folder skipping cuda dockerfiles:
    python scripts/sdk-builder.py

### build sdk folder with cuda dockerfiles: 
    python scripts/sdk-builder.py --cuda

### threaded:
    python scripts/sdk-builder.py --threaded

### override build-dir:
    python scripts/sdk-builder.py --dir sdk_test

### build a single function:
    python scripts/sdk-builder.py --dir sdk_test/category/fn/v1/

### override registry:
    python scripts/sdk-builder.py --registry wbox.hyko.ai
    