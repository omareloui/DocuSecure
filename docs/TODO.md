# TODO

- [x] Authentication
- [x] Authorization
- [x] Store the docs
- [x] Process docs
- [x] ElasticSearch
- [x] Logs and Filebeat
- [x] CRUD
- [x] Bulk upload => multithreading
- [ ] Documentation
- [ ] [Required endpoints](TASK.md#external-api-documentation)
- [ ] PKI

## Nice-To-Haves

- [ ] Classify the docs
- [ ] Pagination
- [ ] More file parsers for more mimetypes
- [x] Refactor the code
  - [x] add more logs
  - [x] move auth to a new app
- [x] Store the file metadata in ES to view (link, size, and date)
- [ ] Unit test

## Performance Improvements

- [ ] Process the file from request stream instead of from disk
- [ ] Get the file path and url before saving the file
