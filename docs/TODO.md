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
- [ ] Documentation
- [ ] Unit test

## Nice-To-Haves

- [ ] Classify the docs from document content
- [ ] Generate keywords from document content
- [ ] Pagination
- [ ] More file parsers for more mimetypes
- [ ] Store the secrets in a .env file
- [x] Refactor the code
  - [x] add more logs
  - [x] move auth to a new app
- [x] Store the file metadata in ES to view (link, size, and date)

## Performance Improvements

- [ ] Process the file from request stream instead of from disk
- [ ] Get the file path and url before saving the file
