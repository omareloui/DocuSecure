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
- [ ] Unit test

## Nice-To-Haves

- [x] More file parsers for more mimetypes
- [ ] Store the secrets in a .env file
- [ ] Don't depend on the content type for the file mimetype
- [ ] Serve the files from Caddy
- [ ] Pagination
- [ ] Generate keywords from document content
- [ ] Classify the docs from document content
- [x] Refactor the code
  - [x] add more logs
  - [x] move auth to a new app
- [x] Store the file metadata in ES to view (link, size, and date)

## Performance Improvements

- [ ] Process the file from request stream instead of from disk
- [ ] Get the file path and url before saving the file
