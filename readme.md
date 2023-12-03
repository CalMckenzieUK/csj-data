# CSJ Helper

Basic UI on top of CSJ dataset which allows users to more quicky find vacancies they are interested in. Can also be used to show insight into the data generally, including elements like most common application processes (eg. jobs requiring interviews, personal statements, CVs; and which behaviours are the most common; which jobs can be applied for via CSJ itself vs the job-holder's website.)



# Desired features

- [x] Shows all high-level basic CSJ vacancy data
- [ ] Data stored in db, rather than df in app (ETL pipeline req)
- [x] Table can be sorted & filtered based on user preference
- [x] Table contains URL linking to another page w/ vacancy details
- [ ] Essential criteria for postings aggregated and shown as selection box including count of vacancies requiring criteria
- [ ] User can select essential criteria they meet and be shown jobs they would be a good fit for
- [x] .gitignore and .env files required as app grows
- [x] Tidy data about jobs to make filtering/sorting easier (eg. salary should only contain lowest figure, closing date should contain only datetime)
- [ ] Show whether jobs require personal statement/cv/behaviours etc and be filtered accordingly
- [ ] Option to get ask for support to allign CV with application requirements
