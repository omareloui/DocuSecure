# TODO

- [x] Authentication
- [x] Authorization
- [x] Store the docs
- [x] Process docs
- [x] ElasticSearch
- [x] Logs and Filebeat
- [x] CRUD
- [x] Bulk upload => multithreading
- [x] [Required endpoints](TASK.md#external-api-documentation)
- [?] PKI
- [x] Documentation
- [x] Unit test

## Nice-To-Haves

- [x] More file parsers for more mimetypes
- [x] Store the secrets in a .env file
- [x] Don't depend on the content-type for the file mimetype
- [x] Serve the files from Caddy
- [ ] On invalid mimetypes the file is stored anyway
- [ ] Categories the document
- [ ] Generate keywords from document
- [x] Refactor the code
  - [x] add more logs
  - [x] move auth to a new app
- [x] Store the file metadata in ES to view (link, size, and date)

## Performance Improvements

- [ ] Process the file from request stream instead of from disk
- [ ] Get the file path and url before saving the file
