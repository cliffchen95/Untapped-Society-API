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
- ref to user
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
