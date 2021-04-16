# gcp-cloud-run-fastapi

ローカルでの実行

```bash
uvicorn app.main:APP --reload
```

cloudbuildローカルでのデバッグ
```
cloud-build-local --config=$PWD/config/cloudbuild.yml --substitutions _TAG_NAME=latest .
```

Docker
```
docker build -t gcp-cloudrun-fastapi .
docker run -p 8080:8080 --rm -it gcp-cloudrun-fastapi
```

GCRへのPush
```
gcloud --project=adtech-sandbox builds submit \
--config config/cloudbuild.yml \
--substitutions="_TAG_NAME=latest" .
```
