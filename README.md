# Untapped-Society-API
### Dependancies: 
- flask: host server
- peewee: ORM
- postgreSQL: database
## Data Model
#### User
##### unique information
- username
- password
- type: Job seeker/Company

#### Job Seeker Information
- ref to user(job seeker)
- education
- name
- DOB
- email
- location
- resume
- language
- ethnicity/nationality
- skillset
- industry
- payrange

#### Company Information
- ref to user(company): this is the user that has admin auth
- name
- tagline
- description
- address
- industry
- website
- linkedin
- twitter
- github
- facebook
- instagram
- pinterest
- youtube
- employer: people authorized to post job with this company

#### Job Application
- ref to user(job seeker)
- ref to position
- note

#### Job Position
- ref to user(company)
- title
- description
- location
- type
- function
- career level
- education (option)
- compensation (option)
- start date
- 30 days expire: boolean, true if automatically expires in 30 days
- remote: boolean, true if the position can be remote

---

## Routes
#### User interaction
- /user/login
- /user/logout
- /user/create
- /user/delete : can work on it later.
- /user/update

#### Jobseeker profile
- /profile/create : create a profile for a jobseeker
- /profile/update : update profile


