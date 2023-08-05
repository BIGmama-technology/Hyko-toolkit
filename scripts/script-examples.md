### sdk skipping cuda dockerfiles:
    python scripts/sdk-builder.py

### sdk with cuda dockerfiles: 
    python scripts/sdk-builder.py --cuda

### threaded:
    python scripts/sdk-builder.py --threaded

### override build-dir:
    python scripts/sdk-builder.py --threaded --dir sdk_test

### override registry:
    python scripts/sdk-builder.py --threaded --dir sdk_test --registry wbox.hyko.ai
    